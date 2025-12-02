from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QGraphicsView, QGraphicsScene, 
                             QPushButton, QButtonGroup, QRadioButton,
                             QLabel, QSpinBox, QGroupBox)
from PyQt5.QtCore import Qt, pyqtSignal, QPointF
from PyQt5.QtGui import QPen, QBrush, QColor, QFont, QPainter
import math

class GraphWidget(QWidget):
    graph_changed = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.vertices = {}  # id -> (x, y, cost, type)
        self.edges = []     # [(id1, id2, critical)]
        self.next_vertex_id = 1
        self.current_mode = 'select'  # 'add_vertex', 'add_edge', 'select'
        self.selected_vertex = None
        self.selected_edge = None
        
        self.create_ui()
        self.setup_scene()
    
    def create_ui(self):
        """Crée l'interface du widget graphe"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Barre d'outils
        toolbar = QHBoxLayout()
        
        # Groupe de boutons pour les modes
        mode_group = QButtonGroup(self)
        
        self.btn_select = QRadioButton("Sélection")
        self.btn_select.setChecked(True)
        self.btn_select.toggled.connect(lambda: self.set_mode('select'))
        mode_group.addButton(self.btn_select)
        
        self.btn_add_vertex = QRadioButton("Ajouter Sommet")
        self.btn_add_vertex.toggled.connect(lambda: self.set_mode('add_vertex'))
        mode_group.addButton(self.btn_add_vertex)
        
        self.btn_add_edge = QRadioButton("Ajouter Arête")
        self.btn_add_edge.toggled.connect(lambda: self.set_mode('add_edge'))
        mode_group.addButton(self.btn_add_edge)
        
        self.btn_critical = QRadioButton("Arête Critique")
        self.btn_critical.toggled.connect(lambda: self.set_mode('critical'))
        mode_group.addButton(self.btn_critical)
        
        # Ajouter les boutons à la barre d'outils
        toolbar.addWidget(QLabel("Mode :"))
        toolbar.addWidget(self.btn_select)
        toolbar.addWidget(self.btn_add_vertex)
        toolbar.addWidget(self.btn_add_edge)
        toolbar.addWidget(self.btn_critical)
        toolbar.addStretch()
        
        # Bouton pour effacer
        btn_clear = QPushButton("Effacer Tout")
        btn_clear.clicked.connect(self.clear_scene)
        toolbar.addWidget(btn_clear)
        
        layout.addLayout(toolbar)
        
        # Vue graphique
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        # Use QPainter.Antialiasing enum for render hints
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setDragMode(self.view.RubberBandDrag)
        self.view.setViewportUpdateMode(self.view.FullViewportUpdate)
        layout.addWidget(self.view)
        
        # Info
        self.info_label = QLabel("0 sommets, 0 arêtes")
        layout.addWidget(self.info_label)
    
    def setup_scene(self):
        """Configure la scène graphique"""
        self.scene.setSceneRect(-400, -300, 800, 600)
        # Connecter les événements de souris
        self.scene.mousePressEvent = self.on_scene_click
    
    def set_mode(self, mode):
        """Change le mode d'interaction"""
        self.current_mode = mode
        if mode == 'select':
            self.view.setDragMode(self.view.RubberBandDrag)
        else:
            self.view.setDragMode(self.view.NoDrag)
    
    def on_scene_click(self, event):
        """Gère les clics sur la scène"""
        pos = event.scenePos()
        
        if self.current_mode == 'add_vertex':
            self.add_vertex_at(pos)
        elif self.current_mode == 'add_edge':
            self.handle_edge_creation(pos)
        elif self.current_mode == 'critical':
            self.toggle_edge_critical(pos)
        elif self.current_mode == 'select':
            # La sélection est gérée par Qt
            pass
        
        # Appeler l'événement parent
        QGraphicsScene.mousePressEvent(self.scene, event)
    
    def add_vertex_at(self, pos):
        """Ajoute un sommet à la position donnée"""
        vertex_id = f"V{self.next_vertex_id}"
        self.next_vertex_id += 1
        
        # Créer le sommet (cercle + texte)
        from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsTextItem
        from PyQt5.QtCore import QRectF
        
        # Cercle
        circle = QGraphicsEllipseItem(QRectF(-20, -20, 40, 40))
        circle.setPos(pos)
        circle.setBrush(QBrush(QColor(70, 130, 180)))  # Bleu acier
        circle.setPen(QPen(Qt.black, 2))
        circle.setData(0, vertex_id)  # Stocker l'ID
        
        # Texte (ID)
        text = QGraphicsTextItem(vertex_id)
        text.setPos(pos.x() - 10, pos.y() - 10)
        text.setDefaultTextColor(Qt.white)
        text.setFont(QFont("Arial", 10, QFont.Bold))
        
        self.scene.addItem(circle)
        self.scene.addItem(text)
        
        # Stocker les informations
        self.vertices[vertex_id] = {
            'pos': pos,
            'cost': 1.0,  # Coût par défaut
            'type': 'normal',
            'items': (circle, text)
        }
        
        self.update_info()
        self.graph_changed.emit(self.get_graph_data())
    
    def handle_edge_creation(self, pos):
        """Gère la création d'arêtes"""
        # Chercher si on a cliqué sur un sommet
        item = self.scene.itemAt(pos, self.view.transform())
        if item and hasattr(item, 'data'):
            vertex_id = item.data(0)
            if vertex_id:
                if self.selected_vertex is None:
                    # Premier sommet sélectionné
                    self.selected_vertex = vertex_id
                    item.setBrush(QBrush(QColor(255, 215, 0)))  # Or
                else:
                    # Deuxième sommet : créer l'arête
                    if self.selected_vertex != vertex_id:
                        self.add_edge(self.selected_vertex, vertex_id)
                    
                    # Réinitialiser la sélection
                    if self.selected_vertex in self.vertices:
                        circle, _ = self.vertices[self.selected_vertex]['items']
                        circle.setBrush(QBrush(QColor(70, 130, 180)))
                    self.selected_vertex = None
    
    def add_edge(self, vertex1_id, vertex2_id):
        """Ajoute une arête entre deux sommets"""
        if vertex1_id in self.vertices and vertex2_id in self.vertices:
            # Vérifier si l'arête existe déjà
            for edge in self.edges:
                if (edge[0] == vertex1_id and edge[1] == vertex2_id) or \
                   (edge[0] == vertex2_id and edge[1] == vertex1_id):
                    return
            
            pos1 = self.vertices[vertex1_id]['pos']
            pos2 = self.vertices[vertex2_id]['pos']
            
            # Créer la ligne
            from PyQt5.QtWidgets import QGraphicsLineItem
            line = QGraphicsLineItem(pos1.x(), pos1.y(), pos2.x(), pos2.y())
            line.setPen(QPen(Qt.darkGray, 3))
            line.setData(0, (vertex1_id, vertex2_id))  # Stocker les IDs
            
            self.scene.addItem(line)
            
            # Ajouter à la liste
            self.edges.append((vertex1_id, vertex2_id, False))
            
            self.update_info()
            self.graph_changed.emit(self.get_graph_data())
    
    def toggle_edge_critical(self, pos):
        """Marque/démarque une arête comme critique"""
        item = self.scene.itemAt(pos, self.view.transform())
        if item and isinstance(item, type(self.scene.items()[0])):
            # Vérifier si c'est une arête
            edge_data = item.data(0)
            if edge_data and isinstance(edge_data, tuple):
                v1, v2 = edge_data
                # Trouver l'arête dans la liste
                for i, (ev1, ev2, critical) in enumerate(self.edges):
                    if (ev1 == v1 and ev2 == v2) or (ev1 == v2 and ev2 == v1):
                        # Inverser l'état critique
                        self.edges[i] = (ev1, ev2, not critical)
                        
                        # Changer la couleur
                        if not critical:
                            item.setPen(QPen(QColor(255, 0, 0), 3))  # Rouge
                        else:
                            item.setPen(QPen(Qt.darkGray, 3))  # Gris
                        
                        self.graph_changed.emit(self.get_graph_data())
                        break
    
    def update_info(self):
        """Met à jour le label d'information"""
        self.info_label.setText(f"{len(self.vertices)} sommets, {len(self.edges)} arêtes")
    
    def get_graph_data(self):
        """Retourne les données du graphe au format dict"""
        vertices_list = []
        for v_id, data in self.vertices.items():
            vertices_list.append({
                'id': v_id,
                'x': data['pos'].x(),
                'y': data['pos'].y(),
                'cost': data['cost'],
                'type': data['type']
            })
        
        edges_list = []
        for v1, v2, critical in self.edges:
            edges_list.append({
                'from': v1,
                'to': v2,
                'critical': critical
            })
        
        return {
            'vertices': vertices_list,
            'edges': edges_list
        }
    
    def clear_scene(self):
        """Efface toute la scène"""
        self.scene.clear()
        self.vertices.clear()
        self.edges.clear()
        self.next_vertex_id = 1
        self.selected_vertex = None
        self.update_info()
        self.graph_changed.emit(self.get_graph_data())
    
    def highlight_solution(self, selected_vertices):
        """Met en évidence la solution"""
        # Réinitialiser toutes les couleurs
        for v_id, data in self.vertices.items():
            circle, text = data['items']
            circle.setBrush(QBrush(QColor(70, 130, 180)))  # Bleu normal
        
        # Colorier les sommets sélectionnés
        for v_id in selected_vertices:
            if v_id in self.vertices:
                circle, text = self.vertices[v_id]['items']
                circle.setBrush(QBrush(QColor(50, 205, 50)))  # Vert lime