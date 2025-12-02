import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QSplitter, QTabWidget,
                             QToolBar, QAction, QStatusBar, QMessageBox)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QKeySequence

from gui.graph_widget import GraphWidget
from gui.parameters_widget import ParametersWidget
from gui.results_widget import ResultsWidget
from gui.styles import get_stylesheet

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Surveillance Network Optimizer - Problème 15")
        self.setGeometry(100, 50, 1400, 800)
        
        # Appliquer le style
        self.setStyleSheet(get_stylesheet())
        
        # Initialiser les données
        self.current_graph = None
        self.solution = None
        
        # Créer l'interface
        self.create_ui()
        
        # Connecter les signaux
        self.connect_signals()
        
        # Status bar
        self.statusBar().showMessage("Prêt")
    
    def create_ui(self):
        """Crée toute l'interface utilisateur"""
        # Créer la toolbar
        self.create_toolbar()
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)
        
        # Splitter principal (gauche/droite)
        main_splitter = QSplitter(Qt.Horizontal)
        main_splitter.setHandleWidth(2)
        
        # Partie gauche : Éditeur de graphe (70%)
        self.graph_widget = GraphWidget()
        main_splitter.addWidget(self.graph_widget)
        
        # Partie droite : Paramètres + Résultats (30%)
        right_splitter = QSplitter(Qt.Vertical)
        right_splitter.setHandleWidth(2)
        
        # Panneau des paramètres (50% du panneau droit)
        self.params_widget = ParametersWidget()
        right_splitter.addWidget(self.params_widget)
        
        # Panneau des résultats (50% du panneau droit)
        self.results_widget = ResultsWidget()
        right_splitter.addWidget(self.results_widget)
        
        # Ajuster les tailles
        right_splitter.setSizes([400, 400])
        main_splitter.addWidget(right_splitter)
        main_splitter.setSizes([1000, 400])
        
        main_layout.addWidget(main_splitter)
    
    def create_toolbar(self):
        """Crée la barre d'outils"""
        toolbar = QToolBar("Barre d'outils")
        toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(toolbar)
        
        # Actions
        new_action = QAction("Nouveau", self)
        new_action.setShortcut(QKeySequence.New)
        new_action.triggered.connect(self.new_graph)
        
        open_action = QAction("Ouvrir", self)
        open_action.setShortcut(QKeySequence.Open)
        open_action.triggered.connect(self.open_graph)
        
        save_action = QAction("Sauvegarder", self)
        save_action.setShortcut(QKeySequence.Save)
        save_action.triggered.connect(self.save_graph)
        
        run_action = QAction("Résoudre", self)
        run_action.setShortcut(Qt.Key_F5)
        run_action.triggered.connect(self.solve_problem)
        
        # Ajouter à la toolbar
        toolbar.addAction(new_action)
        toolbar.addAction(open_action)
        toolbar.addAction(save_action)
        toolbar.addSeparator()
        toolbar.addAction(run_action)
    
    def connect_signals(self):
        """Connecte les signaux entre les widgets"""
        # Quand le graphe change, mettre à jour les paramètres
        self.graph_widget.graph_changed.connect(self.params_widget.update_from_graph)
        
        # Quand on clique sur "Résoudre"
        self.params_widget.solve_clicked.connect(self.solve_problem)
        
        # Quand la solution est prête
        # (à connecter quand on aura le worker)
    
    def new_graph(self):
        """Crée un nouveau graphe vide"""
        self.graph_widget.clear_scene()
        self.params_widget.clear()
        self.results_widget.clear()
        self.statusBar().showMessage("Nouveau graphe créé")
    
    def open_graph(self):
        """Ouvre un graphe depuis un fichier"""
        # À implémenter avec QFileDialog
        QMessageBox.information(self, "Info", "Fonctionnalité à implémenter")
    
    def save_graph(self):
        """Sauvegarde le graphe dans un fichier"""
        # À implémenter avec QFileDialog
        QMessageBox.information(self, "Info", "Fonctionnalité à implémenter")
    
    def solve_problem(self):
        """Résout le problème de couverture de sommets"""
        # Récupérer les données du graphe
        graph_data = self.graph_widget.get_graph_data()
        
        # Récupérer les paramètres
        params = self.params_widget.get_parameters()
        
        # Valider qu'on a un graphe
        if not graph_data['vertices']:
            QMessageBox.warning(self, "Avertissement", "Le graphe est vide !")
            return
        
        # Valider qu'on a des coûts
        if not all(v['cost'] > 0 for v in graph_data['vertices']):
            QMessageBox.warning(self, "Avertissement", 
                               "Tous les sommets doivent avoir un coût positif !")
            return
        
        # Afficher "Calcul en cours"
        self.statusBar().showMessage("Résolution en cours...")
        self.results_widget.show_loading()
        
        # Ici on appellera le solveur Gurobi
        # Pour l'instant, on simule
        self.simulate_solution(graph_data, params)
    
    def simulate_solution(self, graph_data, params):
        """Simule une solution (à remplacer par Gurobi)"""
        import time
        import random
        
        # Simulation d'un calcul
        time.sleep(1)
        
        # Solution simulée (sélectionne aléatoirement 50% des sommets)
        vertices = graph_data['vertices']
        selected = random.sample([v['id'] for v in vertices], 
                                max(1, len(vertices)//2))
        
        # Calcul du coût
        total_cost = sum(v['cost'] for v in vertices if v['id'] in selected)
        
        # Mettre à jour l'interface
        self.solution = {
            'total_cost': total_cost,
            'selected_vertices': selected,
            'status': 'optimal',
            'cover_details': {}  # À calculer
        }
        
        self.results_widget.display_solution(self.solution)
        self.graph_widget.highlight_solution(selected)
        self.statusBar().showMessage(f"Solution trouvée ! Coût : {total_cost}€")
        
        # Afficher un message
        QMessageBox.information(self, "Solution", 
                               f"Solution simulée trouvée !\n"
                               f"Coût total : {total_cost}€\n"
                               f"Sommets sélectionnés : {len(selected)}")