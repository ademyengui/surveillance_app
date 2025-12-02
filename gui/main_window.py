import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QSplitter, QTabWidget,
                             QToolBar, QAction, QStatusBar, QMessageBox)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import QFileDialog
from datetime import datetime

from gui.graph_widget import GraphWidget
from gui.parameters_widget import ParametersWidget
from gui.results_widget import ResultsWidget
from gui.styles import get_stylesheet
from solver.worker import SolverWorker
from utils.file_io import save_graph_to_file, load_graph_from_file, export_solution_to_csv

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
        self.solver_worker = None
        
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
        
        export_action = QAction("Exporter Solution", self)
        export_action.triggered.connect(self.export_solution)
        
        # Ajouter à la toolbar
        toolbar.addAction(new_action)
        toolbar.addAction(open_action)
        toolbar.addAction(save_action)
        toolbar.addSeparator()
        toolbar.addAction(run_action)
        toolbar.addAction(export_action)
    
    def connect_signals(self):
        """Connecte les signaux entre les widgets"""
        # Quand le graphe change, mettre à jour les paramètres
        self.graph_widget.graph_changed.connect(self.params_widget.update_from_graph)
        
        # Quand on clique sur "Résoudre"
        self.params_widget.solve_clicked.connect(self.solve_problem)
    
    def new_graph(self):
        """Crée un nouveau graphe vide"""
        self.graph_widget.clear_scene()
        self.params_widget.clear()
        self.results_widget.clear()
        self.solution = None
        self.statusBar().showMessage("Nouveau graphe créé")
    
    def open_graph(self):
        """Ouvre un graphe depuis un fichier"""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Ouvrir un fichier de graphe",
            "",
            "Fichiers JSON (*.json);;Tous les fichiers (*)"
        )
        
        if filename:
            result = load_graph_from_file(filename)
            if result:
                graph_data, parameters, solution, metadata = result
                
                # Note: Vous devrez implémenter set_graph_data dans GraphWidget
                # Pour l'instant, on affiche juste un message
                self.statusBar().showMessage(f"Fichier chargé : {filename}")
                QMessageBox.information(self, "Info", 
                                       f"Fonctionnalité de chargement complète à implémenter\n"
                                       f"Fichier: {filename}")
            else:
                QMessageBox.warning(self, "Erreur", "Impossible de charger le fichier.")
    
    def save_graph(self):
        """Sauvegarde le graphe dans un fichier"""
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Sauvegarder le graphe",
            f"surveillance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            "Fichiers JSON (*.json);;Tous les fichiers (*)"
        )
        
        if filename:
            graph_data = self.graph_widget.get_graph_data()
            parameters = self.params_widget.get_parameters()
            
            save_data = save_graph_to_file(graph_data, parameters, self.solution, filename)
            self.statusBar().showMessage(f"Fichier sauvegardé : {filename}")
    
    def export_solution(self):
        """Exporte les résultats en CSV"""
        if not self.solution:
            QMessageBox.warning(self, "Avertissement", "Aucune solution à exporter.")
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Exporter la solution",
            f"solution_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            "Fichiers CSV (*.csv);;Tous les fichiers (*)"
        )
        
        if filename:
            if export_solution_to_csv(self.solution, filename):
                self.statusBar().showMessage(f"Solution exportée : {filename}")
                QMessageBox.information(self, "Succès", "Solution exportée avec succès !")
            else:
                QMessageBox.warning(self, "Erreur", "Erreur lors de l'export.")
    
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
        # On va mettre à jour les coûts depuis la table
        vertex_params = params.get('vertices', {})
        for vertex in graph_data['vertices']:
            v_id = vertex['id']
            if v_id in vertex_params:
                vertex['cost'] = vertex_params[v_id]['cost']
                vertex['type'] = vertex_params[v_id]['type']
            else:
                vertex['cost'] = 1.0
                vertex['type'] = 'normal'
        
        # Désactiver le bouton pendant le calcul
        self.params_widget.solve_button.setEnabled(False)
        
        # Afficher "Calcul en cours"
        self.statusBar().showMessage("Résolution en cours...")
        self.results_widget.show_loading()
        
        # Créer et lancer le worker
        self.solver_worker = SolverWorker(graph_data, params)
        
        # Connecter les signaux du worker
        self.solver_worker.started.connect(self.on_solver_started)
        self.solver_worker.finished.connect(self.on_solver_finished)
        self.solver_worker.error.connect(self.on_solver_error)
        
        # Lancer le worker
        self.solver_worker.start()
    
    def on_solver_started(self):
        """Début de la résolution"""
        self.statusBar().showMessage("Résolution démarrée...")
    
    def on_solver_finished(self, solution):
        """Fin de la résolution avec succès"""
        # Réactiver le bouton
        self.params_widget.solve_button.setEnabled(True)
        
        # Stocker la solution
        self.solution = solution
        
        # Afficher les résultats
        if solution['status'] == 'optimal':
            self.results_widget.display_solution(solution)
            self.graph_widget.highlight_solution(solution['selected_vertices'])
            
            # Mettre à jour le statut
            time_msg = f" en {solution.get('solve_time', 0):.2f} secondes"
            self.statusBar().showMessage(
                f"✓ Solution optimale trouvée ! Coût : {solution['total_cost']}€" + time_msg
            )
            
            # Afficher un message de succès
            QMessageBox.information(
                self, 
                "Solution Optimale",
                f"Solution trouvée avec succès !\n\n"
                f"• Coût total : {solution['total_cost']:.2f}€\n"
                f"• Sommets sélectionnés : {len(solution['selected_vertices'])}\n"
                f"• Temps de résolution : {solution.get('solve_time', 0):.2f}s"
            )
        else:
            # Afficher un message d'erreur
            self.statusBar().showMessage(f"⚠ {solution.get('message', 'Erreur')}")
            self.results_widget.display_solution(solution)
            
            QMessageBox.warning(
                self,
                "Problème de résolution",
                f"Le solveur a rencontré un problème :\n\n"
                f"Status : {solution['status']}\n"
                f"Message : {solution.get('message', 'Aucun détail')}"
            )
    
    def on_solver_error(self, error_message):
        """Erreur pendant la résolution"""
        self.params_widget.solve_button.setEnabled(True)
        self.statusBar().showMessage(f"❌ Erreur : {error_message}")
        QMessageBox.critical(
            self,
            "Erreur du Solveur",
            f"Une erreur est survenue pendant la résolution :\n\n{error_message}"
        )