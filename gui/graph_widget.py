from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QGraphicsView, QGraphicsScene, 
                             QPushButton, QButtonGroup, QRadioButton,
                             QLabel, QSpinBox, QGroupBox, QGraphicsLineItem,
                             QGraphicsEllipseItem, QGraphicsTextItem,
                             QGraphicsItem, QGraphicsItemGroup, QMenu,
                             QSizePolicy, QMainWindow, QToolBar, QAction)
from PyQt5.QtCore import Qt, pyqtSignal, QPointF, QRectF, QLineF, QEvent
from PyQt5.QtGui import QPen, QBrush, QColor, QFont, QPainter
import math

class VertexItem(QGraphicsItemGroup):
    """Classe personnalisée pour les sommets du graphe"""
    def __init__(self, vertex_id, pos, parent=None):
        super().__init__(parent)
        self.vertex_id = vertex_id
        self.setPos(pos)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.is_movable = True  # Nouveau: contrôle du déplacement
        
        # Créer le cercle
        self.circle = QGraphicsEllipseItem(QRectF(-20, -20, 40, 40), self)
        self.circle.setBrush(QBrush(QColor(70, 130, 180)))  # Bleu acier
        self.circle.setPen(QPen(QColor(30, 60, 90), 2))
        self.circle.setData(0, vertex_id)
        
        # Créer le texte
        self.text = QGraphicsTextItem(vertex_id, self)
        self.text.setDefaultTextColor(Qt.white)
        self.text.setFont(QFont("Arial", 12, QFont.Bold))  # Augmenté de 10 à 12
        # Centrer le texte
        text_rect = self.text.boundingRect()
        self.text.setPos(-text_rect.width()/2, -text_rect.height()/2)
        
        # Ajouter les éléments au groupe
        self.addToGroup(self.circle)
        self.addToGroup(self.text)
        
        # Initialiser l'état
        self.is_selected = False
        self.vertex_type = 'normal'
        self.cost = 1.0
        
    def set_movable(self, movable):
        """Active ou désactive le déplacement du sommet"""
        self.is_movable = movable
        self.setFlag(QGraphicsItem.ItemIsMovable, movable)
        
    def mousePressEvent(self, event):
        """Gère le clic sur le sommet"""
        # Ne pas déplacer si on est en mode ajout d'arête
        if hasattr(self.scene().parent(), 'current_mode'):
            if self.scene().parent().current_mode == 'add_edge':
                event.accept()  # Accepter l'événement mais ne pas déplacer
                return
                
        self.is_selected = True
        self.circle.setBrush(QBrush(QColor(255, 215, 0)))  # Or quand sélectionné
        super().mousePressEvent(event)
        
    def mouseReleaseEvent(self, event):
        """Gère le relâchement de la souris"""
        self.is_selected = False
        # Retour à la couleur normale
        if self.vertex_type == 'selected_solution':
            self.circle.setBrush(QBrush(QColor(50, 205, 50)))  # Vert
        elif self.vertex_type == 'mandatory':
            self.circle.setBrush(QBrush(QColor(220, 20, 60)))  # Rouge
        elif self.vertex_type == 'forbidden':
            self.circle.setBrush(QBrush(QColor(128, 128, 128)))  # Gris
        else:
            self.circle.setBrush(QBrush(QColor(70, 130, 180)))  # Bleu normal
        super().mouseReleaseEvent(event)
        
    def set_type(self, vertex_type):
        """Change le type du sommet (couleur)"""
        self.vertex_type = vertex_type
        if vertex_type == 'selected_solution':
            self.circle.setBrush(QBrush(QColor(50, 205, 50)))  # Vert
        elif vertex_type == 'mandatory':
            self.circle.setBrush(QBrush(QColor(220, 20, 60)))  # Rouge
        elif vertex_type == 'forbidden':
            self.circle.setBrush(QBrush(QColor(128, 128, 128)))  # Gris
        else:
            self.circle.setBrush(QBrush(QColor(70, 130, 180)))  # Bleu normal

class EdgeItem(QGraphicsLineItem):
    """Classe personnalisée pour les arêtes du graphe"""
    def __init__(self, vertex1_id, vertex2_id, v1_pos, v2_pos, parent=None):
        super().__init__(parent)
        self.setLine(QLineF(v1_pos, v2_pos))
        self.vertex1_id = vertex1_id
        self.vertex2_id = vertex2_id
        self.critical = False
        
        # Style par défaut
        self.setPen(QPen(QColor(100, 100, 100), 3, Qt.SolidLine, Qt.RoundCap))
        self.setZValue(-1)  # Mettre en arrière-plan
        
    def set_critical(self, critical):
        """Marque l'arête comme critique ou non"""
        self.critical = critical
        if critical:
            self.setPen(QPen(QColor(220, 20, 60), 3, Qt.DashLine, Qt.RoundCap))
        else:
            self.setPen(QPen(QColor(100, 100, 100), 3, Qt.SolidLine, Qt.RoundCap))
            
    def update_position(self, v1_pos, v2_pos):
        """Met à jour la position de l'arête quand les sommets bougent"""
        self.setLine(QLineF(v1_pos, v2_pos))

class GraphWidget(QWidget):
    graph_changed = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.vertices = {}  # id -> VertexItem
        self.edges = {}     # (id1, id2) -> EdgeItem
        self.next_vertex_id = 1
        self.current_mode = 'select'  # 'add_vertex', 'add_edge', 'critical', 'delete'
        self.temp_edge_start = None
        self.temp_edge_item = None
        self.first_vertex_selected = None  # Pour la création d'arête
        
        self.create_ui()
        self.setup_scene()
        self.setup_resize_handle()
    
    def create_ui(self):
        """Crée l'interface du widget graphe"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        
        # Barre d'outils stylée
        toolbar_widget = QWidget()
        toolbar_widget.setObjectName("graphToolbar")
        toolbar_widget.setStyleSheet("""
            #graphToolbar {
                background-color: #ffffff;
                border-bottom: 2px solid #e5e7eb;
                padding: 8px;
            }
        """)
        toolbar_widget.setMaximumHeight(60)  # Limite la hauteur
        
        toolbar_layout = QHBoxLayout(toolbar_widget)
        toolbar_layout.setSpacing(10)
        toolbar_layout.setContentsMargins(10, 5, 10, 5)
        
        # Groupe de boutons pour les modes
        mode_group = QButtonGroup(self)
        
        # Créer des boutons stylés
        modes = [
            ("Sélection", "select", "#3b82f6"),
            ("Ajouter Sommet", "add_vertex", "#10b981"),
            ("Ajouter Arête", "add_edge", "#8b5cf6"),
            ("Arête Critique", "critical", "#ef4444"),
            ("Supprimer", "delete", "#6b7280")
        ]
        
        self.mode_buttons = {}
        for text, mode, color in modes:
            btn = QRadioButton(text)
            btn.setObjectName(f"mode_{mode}")
            btn.setStyleSheet(f"""
                QRadioButton {{
                    padding: 8px 12px;
                    border-radius: 6px;
                    font-weight: 500;
                }}
                QRadioButton::indicator {{
                    width: 0px;
                    height: 0px;
                }}
                QRadioButton:checked {{
                    background-color: {color};
                    color: white;
                }}
                QRadioButton:hover {{
                    background-color: #f3f4f6;
                }}
            """)
            btn.toggled.connect(lambda checked, m=mode: self.set_mode(m) if (checked and hasattr(self, 'view')) else None)
            mode_group.addButton(btn)
            toolbar_layout.addWidget(btn)
            self.mode_buttons[mode] = btn
        
        self.mode_buttons['select'].setChecked(True)
        
        toolbar_layout.addStretch()
        
        # Bouton pour effacer
        btn_clear = QPushButton("Effacer Tout")
        btn_clear.setStyleSheet("""
            QPushButton {
                background-color: #ef4444;
                color: white;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #dc2626;
            }
        """)
        btn_clear.clicked.connect(self.clear_scene)
        toolbar_layout.addWidget(btn_clear)
        
        # Bouton pour redimensionner
        btn_resize = QPushButton("📐")
        btn_resize.setToolTip("Redimensionner la fenêtre")
        btn_resize.setFixedSize(32, 32)
        btn_resize.setStyleSheet("""
            QPushButton {
                background-color: #f3f4f6;
                border: 1px solid #d1d5db;
                border-radius: 6px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #e5e7eb;
            }
        """)
        btn_resize.clicked.connect(self.show_resize_menu)
        toolbar_layout.addWidget(btn_resize)
        
        layout.addWidget(toolbar_widget)
        
        # Vue graphique - IMPORTANT: Set size policy to expand
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setRenderHint(QPainter.SmoothPixmapTransform)
        self.view.setRenderHint(QPainter.TextAntialiasing)
        self.view.setDragMode(QGraphicsView.RubberBandDrag)
        self.view.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.view.setBackgroundBrush(QBrush(QColor(248, 250, 252)))
        
        # Set size policy to expand in both directions
        self.view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Cadre pour la vue
        self.view.setStyleSheet("""
            QGraphicsView {
                border: 2px solid #e5e7eb;
                border-radius: 8px;
                background-color: #f8fafc;
            }
        """)
        
        # Add view to layout with stretch factor
        layout.addWidget(self.view, 1)  # The '1' means it will stretch
        
        # Barre d'information
        info_widget = QWidget()
        info_widget.setMaximumHeight(40)  # Limite la hauteur
        info_layout = QHBoxLayout(info_widget)
        info_layout.setContentsMargins(10, 5, 10, 5)
        
        self.info_label = QLabel("0 sommets, 0 arêtes")
        self.info_label.setStyleSheet("""
            QLabel {
                color: #6b7280;
                font-weight: 500;
            }
        """)
        
        self.help_label = QLabel("Mode Sélection : Cliquez pour sélectionner, glissez pour déplacer")
        self.help_label.setStyleSheet("""
            QLabel {
                color: #9ca3af;
                font-style: italic;
                font-size: 12px;
            }
        """)
        
        info_layout.addWidget(self.info_label)
        info_layout.addStretch()
        info_layout.addWidget(self.help_label)
        
        layout.addWidget(info_widget)
        
        # Set the main widget to expand
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    
    def setup_scene(self):
        """Configure la scène graphique"""
        self.scene.setSceneRect(-500, -350, 1000, 700)
        # Connecter les événements de souris
        self.scene.mousePressEvent = self.on_scene_click
        self.scene.mouseMoveEvent = self.on_scene_mouse_move
        self.scene.mouseReleaseEvent = self.on_scene_mouse_release
    
    def setup_resize_handle(self):
        """Configure la poignée de redimensionnement"""
        # This will be handled by the main window's resize frame
        pass
    
    def set_mode(self, mode):
        """Change le mode d'interaction"""
        old_mode = self.current_mode
        self.current_mode = mode
        
        # Réinitialiser la sélection d'arête
        if old_mode == 'add_edge' and mode != 'add_edge':
            self.reset_edge_selection()
        
        if mode == 'select':
            self.view.setDragMode(QGraphicsView.RubberBandDrag)
            self.temp_edge_start = None
            if self.temp_edge_item:
                self.scene.removeItem(self.temp_edge_item)
                self.temp_edge_item = None
            
            # Activer le déplacement des sommets
            for vertex in self.vertices.values():
                vertex.set_movable(True)
            
            self.help_label.setText("Mode Sélection : Cliquez pour sélectionner, glissez pour déplacer")
            
        elif mode == 'add_edge':
            self.view.setDragMode(QGraphicsView.NoDrag)
            # Désactiver le déplacement des sommets
            for vertex in self.vertices.values():
                vertex.set_movable(False)
            
            self.help_label.setText("Mode Ajout d'Arête : Cliquez sur un premier sommet (il devient jaune), puis sur un deuxième sommet")
            
        else:
            self.view.setDragMode(QGraphicsView.NoDrag)
            # Désactiver le déplacement des sommets pour les autres modes
            for vertex in self.vertices.values():
                vertex.set_movable(False)
            
            # Mettre à jour l'aide
            help_texts = {
                'add_vertex': "Mode Ajout de Sommet : Cliquez n'importe où pour ajouter un sommet",
                'critical': "Mode Arête Critique : Cliquez sur une arête pour la marquer comme critique (rouge)",
                'delete': "Mode Suppression : Cliquez sur un élément pour le supprimer"
            }
            self.help_label.setText(f"Conseil : {help_texts.get(mode, '')}")
        
        # Mettre à jour les couleurs des sommets
        for vertex in self.vertices.values():
            vertex.set_type(vertex.vertex_type)
    
    def reset_edge_selection(self):
        """Réinitialise la sélection pour la création d'arête"""
        if self.first_vertex_selected:
            # Réinitialiser la couleur du premier sommet sélectionné
            self.first_vertex_selected.circle.setBrush(QBrush(QColor(70, 130, 180)))
            self.first_vertex_selected = None
        
        if self.temp_edge_item:
            self.scene.removeItem(self.temp_edge_item)
            self.temp_edge_item = None
        
        self.temp_edge_start = None
    
    def on_scene_click(self, event):
        """Gère les clics sur la scène"""
        pos = event.scenePos()
        
        if self.current_mode == 'add_vertex':
            self.add_vertex_at(pos)
            
        elif self.current_mode == 'add_edge':
            # Trouver le sommet cliqué
            vertex = self.find_vertex_at(pos)
            
            if vertex:
                if self.first_vertex_selected is None:
                    # Premier sommet sélectionné
                    self.first_vertex_selected = vertex
                    self.temp_edge_start = vertex.scenePos()
                    
                    # Colorier le sommet en jaune
                    vertex.circle.setBrush(QBrush(QColor(255, 215, 0)))
                    
                    # Afficher un message d'aide
                    self.help_label.setText("Maintenant cliquez sur un deuxième sommet pour créer l'arête")
                    
                else:
                    # Deuxième sommet sélectionné
                    if self.first_vertex_selected != vertex:
                        # Créer l'arête
                        self.add_edge(self.first_vertex_selected.vertex_id, vertex.vertex_id)
                    
                    # Réinitialiser la sélection
                    self.reset_edge_selection()
                    self.help_label.setText("Mode Ajout d'Arête : Cliquez sur un premier sommet (il devient jaune), puis sur un deuxième sommet")
        
        elif self.current_mode == 'critical':
            self.toggle_edge_critical(pos)
            
        elif self.current_mode == 'delete':
            self.delete_item_at(pos)
            
        elif self.current_mode == 'select':
            # La sélection normale fonctionne
            pass
        
        # Appeler l'événement parent
        QGraphicsScene.mousePressEvent(self.scene, event)
    
    def on_scene_mouse_move(self, event):
        """Gère le mouvement de la souris (pour l'arête temporaire)"""
        if self.current_mode == 'add_edge' and self.first_vertex_selected:
            pos = event.scenePos()
            
            # Mettre à jour ou créer la ligne temporaire
            if self.temp_edge_item:
                self.scene.removeItem(self.temp_edge_item)
            
            # Créer une ligne temporaire
            self.temp_edge_item = QGraphicsLineItem(
                QLineF(self.temp_edge_start, pos)
            )
            self.temp_edge_item.setPen(QPen(QColor(100, 100, 100), 2, Qt.DashLine))
            self.scene.addItem(self.temp_edge_item)
        
        QGraphicsScene.mouseMoveEvent(self.scene, event)
    
    def on_scene_mouse_release(self, event):
        """Gère le relâchement de la souris"""
        # Pour le mode ajout d'arête, on ne fait rien ici
        # Le traitement est dans on_scene_click
        
        QGraphicsScene.mouseReleaseEvent(self.scene, event)
    
    def add_vertex_at(self, pos):
        """Ajoute un sommet à la position donnée"""
        vertex_id = f"V{self.next_vertex_id}"
        self.next_vertex_id += 1
        
        # Créer l'item de sommet
        vertex = VertexItem(vertex_id, pos)
        
        # Définir si le sommet est déplaçable selon le mode
        vertex.set_movable(self.current_mode == 'select')
        
        self.scene.addItem(vertex)
        
        # Stocker la référence
        self.vertices[vertex_id] = vertex
        
        self.update_info()
        self.graph_changed.emit(self.get_graph_data())
    
    def find_vertex_at(self, pos, radius=40):
        """Trouve le sommet le plus proche d'une position"""
        for vertex in self.vertices.values():
            vertex_pos = vertex.scenePos()
            distance = math.sqrt((vertex_pos.x() - pos.x())**2 + (vertex_pos.y() - pos.y())**2)
            if distance <= radius:
                return vertex
        return None
    
    def add_edge(self, vertex1_id, vertex2_id):
        """Ajoute une arête entre deux sommets"""
        if vertex1_id in self.vertices and vertex2_id in self.vertices:
            # Vérifier si l'arête existe déjà
            edge_key = tuple(sorted([vertex1_id, vertex2_id]))
            if edge_key in self.edges:
                return
            
            v1 = self.vertices[vertex1_id]
            v2 = self.vertices[vertex2_id]
            
            # Créer l'arête
            edge = EdgeItem(vertex1_id, vertex2_id, v1.scenePos(), v2.scenePos())
            self.scene.addItem(edge)
            
            # Stocker la référence
            self.edges[edge_key] = edge
            
            self.update_info()
            self.graph_changed.emit(self.get_graph_data())
    
    def toggle_edge_critical(self, pos):
        """Marque/démarque une arête comme critique"""
        # Trouver l'arête la plus proche
        items = self.scene.items(pos)
        for item in items:
            if isinstance(item, EdgeItem):
                edge_key = tuple(sorted([item.vertex1_id, item.vertex2_id]))
                if edge_key in self.edges:
                    edge = self.edges[edge_key]
                    edge.set_critical(not edge.critical)
                    self.graph_changed.emit(self.get_graph_data())
                    break
    
    def delete_item_at(self, pos):
        """Supprime l'élément à la position donnée"""
        items = self.scene.items(pos)
        for item in items:
            if isinstance(item, VertexItem):
                # Supprimer le sommet et toutes ses arêtes
                vertex_id = item.vertex_id
                
                # Supprimer les arêtes connectées
                edges_to_remove = []
                for edge_key, edge in self.edges.items():
                    if vertex_id in edge_key:
                        self.scene.removeItem(edge)
                        edges_to_remove.append(edge_key)
                
                for edge_key in edges_to_remove:
                    del self.edges[edge_key]
                
                # Supprimer le sommet
                self.scene.removeItem(item)
                del self.vertices[vertex_id]
                
                self.update_info()
                self.graph_changed.emit(self.get_graph_data())
                break
            
            elif isinstance(item, EdgeItem):
                # Supprimer l'arête
                edge_key = tuple(sorted([item.vertex1_id, item.vertex2_id]))
                if edge_key in self.edges:
                    self.scene.removeItem(item)
                    del self.edges[edge_key]
                    
                    self.update_info()
                    self.graph_changed.emit(self.get_graph_data())
                break
    
    def update_info(self):
        """Met à jour le label d'information"""
        critical_count = sum(1 for edge in self.edges.values() if edge.critical)
        self.info_label.setText(
            f"📊 {len(self.vertices)} sommets • {len(self.edges)} arêtes • {critical_count} critiques"
        )
    
    def get_graph_data(self):
        """Retourne les données du graphe au format dict"""
        vertices_list = []
        for v_id, vertex in self.vertices.items():
            pos = vertex.scenePos()
            vertices_list.append({
                'id': v_id,
                'x': pos.x(),
                'y': pos.y(),
                'cost': vertex.cost,
                'type': vertex.vertex_type
            })
        
        edges_list = []
        for (v1_id, v2_id), edge in self.edges.items():
            edges_list.append({
                'from': v1_id,
                'to': v2_id,
                'critical': edge.critical
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
        self.first_vertex_selected = None
        self.temp_edge_start = None
        self.temp_edge_item = None
        self.update_info()
        self.graph_changed.emit(self.get_graph_data())
    
    def highlight_solution(self, selected_vertices):
        """Met en évidence la solution"""
        # Réinitialiser tous les sommets
        for vertex in self.vertices.values():
            vertex.set_type('normal')
        
        # Colorier les sommets sélectionnés
        for v_id in selected_vertices:
            if v_id in self.vertices:
                self.vertices[v_id].set_type('selected_solution')
    
    def load_graph_data(self, graph_data):
        """Charge un graphe depuis des données structurées"""
        # Effacer la scène actuelle
        self.clear_scene()
        
        # Vérifier et charger les sommets
        for vertex_data in graph_data.get('vertices', []):
            if 'id' in vertex_data and 'x' in vertex_data and 'y' in vertex_data:
                pos = QPointF(vertex_data['x'], vertex_data['y'])
                vertex_id = vertex_data['id']
                
                # Créer le sommet
                vertex = VertexItem(vertex_id, pos)
                vertex.cost = vertex_data.get('cost', 1.0)
                vertex_type = vertex_data.get('type', 'normal')
                vertex.set_type(vertex_type)
                
                # Rendre déplaçable selon le mode
                vertex.set_movable(self.current_mode == 'select')
                
                self.scene.addItem(vertex)
                self.vertices[vertex_id] = vertex
                
                # Mettre à jour l'ID suivant
                try:
                    num = int(vertex_id[1:])  # Extraire le numéro de V1, V2, etc.
                    if num >= self.next_vertex_id:
                        self.next_vertex_id = num + 1
                except:
                    pass
        
        # Charger les arêtes
        for edge_data in graph_data.get('edges', []):
            if 'from' in edge_data and 'to' in edge_data:
                v1_id = edge_data['from']
                v2_id = edge_data['to']
                
                if v1_id in self.vertices and v2_id in self.vertices:
                    v1 = self.vertices[v1_id]
                    v2 = self.vertices[v2_id]
                    
                    # Créer l'arête
                    edge = EdgeItem(v1_id, v2_id, v1.scenePos(), v2.scenePos())
                    
                    # Marquer comme critique si nécessaire
                    if edge_data.get('critical', False):
                        edge.set_critical(True)
                    
                    self.scene.addItem(edge)
                    
                    # Stocker la référence
                    edge_key = tuple(sorted([v1_id, v2_id]))
                    self.edges[edge_key] = edge
        
        self.update_info()
        self.graph_changed.emit(self.get_graph_data())
    
    def is_empty(self):
        """Vérifie si le graphe est vide"""
        return len(self.vertices) == 0
    
    def show_resize_menu(self):
        """Affiche le menu de redimensionnement"""
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: white;
                border: 1px solid #d1d5db;
                border-radius: 6px;
                padding: 4px;
            }
            QMenu::item {
                padding: 6px 16px;
                border-radius: 4px;
                color: #374151;
            }
            QMenu::item:selected {
                background-color: #3b82f6;
                color: white;
            }
        """)
        
        sizes = [
            ("Petit (600×400)", 600, 400),
            ("Moyen (800×600)", 800, 600),
            ("Grand (1000×700)", 1000, 700),
            ("Large (1200×800)", 1200, 800),
            ("Maximisé", None, None)
        ]
        
        for text, width, height in sizes:
            action = menu.addAction(text)
            if width is None:
                action.triggered.connect(self.maximize_window)
            else:
                action.triggered.connect(lambda checked, w=width, h=height: self.resize_window(w, h))
        
        menu.exec_(self.mapToGlobal(self.btn_resize.pos()))
    
    def resize_window(self, width, height):
        """Redimensionne la fenêtre principale"""
        main_window = self.window()
        if main_window:
            main_window.resize(width, height)
            
    def maximize_window(self):
        """Maximise la fenêtre"""
        main_window = self.window()
        if main_window:
            if main_window.isMaximized():
                main_window.showNormal()
            else:
                main_window.showMaximized()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Graph Editor - Fully Resizable")
        self.setGeometry(100, 100, 1000, 700)
        
        # Set window flags to allow full resizing
        self.setWindowFlags(Qt.Window | Qt.WindowMinimizeButtonHint | 
                           Qt.WindowMaximizeButtonHint | Qt.WindowCloseButtonHint)
        
        # Create graph widget
        self.graph_widget = GraphWidget()
        self.setCentralWidget(self.graph_widget)
        
        # Add a proper toolbar
        self.toolbar = QToolBar("Main Toolbar")
        self.addToolBar(self.toolbar)
        
        # Add window control buttons
        self.minimize_action = QAction("🗕", self)
        self.minimize_action.triggered.connect(self.showMinimized)
        self.toolbar.addAction(self.minimize_action)
        
        self.maximize_action = QAction("🗖", self)
        self.maximize_action.triggered.connect(self.toggle_maximize)
        self.toolbar.addAction(self.maximize_action)
        
        # Add separator
        self.toolbar.addSeparator()
        
        # Add resize presets
        sizes = [
            ("600×400", 600, 400),
            ("800×600", 800, 600),
            ("1000×700", 1000, 700),
            ("1200×800", 1200, 800)
        ]
        
        for text, width, height in sizes:
            action = QAction(f"{text}", self)
            action.triggered.connect(lambda checked, w=width, h=height: self.resize(w, h))
            self.toolbar.addAction(action)
        
        # Update window state
        self.windowStateChanged.connect(self.update_window_state)
        
        # Set minimum size
        self.setMinimumSize(400, 300)
    
    def toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()
    
    def update_window_state(self, state):
        if self.isMaximized():
            self.maximize_action.setText("🗗")
        else:
            self.maximize_action.setText("🗖")
    
    def resizeEvent(self, event):
        """Handle resize event"""
        super().resizeEvent(event)
        # Update the scene rect based on new size
        width = self.width()
        height = self.height()
        # Adjust scene rect to match window proportions
        self.graph_widget.scene.setSceneRect(-width/2, -height/2, width, height)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())