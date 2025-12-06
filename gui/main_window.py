import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel, 
                             QHBoxLayout, QSplitter, QTabWidget,
                             QToolBar, QAction, QStatusBar, QMessageBox,
                             QFileDialog, QProgressDialog)
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QIcon, QKeySequence
from datetime import datetime
import os

from gui.graph_widget import GraphWidget
from gui.parameters_widget import ParametersWidget
from gui.results_widget import ResultsWidget
from gui.styles import get_stylesheet
from solver.worker import SolverWorker
from utils.file_io import (save_graph_to_file, load_graph_from_file, 
                          export_solution_to_json, export_solution_to_csv,
                          validate_graph_data)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Surveillance Network Optimizer - Problème 15")
        self.setGeometry(100, 50, 1400, 800)
        
        # Appliquer le style
        self.setStyleSheet(get_stylesheet())
        
        # Initialiser les données
        self.current_file = None
        self.solution = None
        self.solver_worker = None
        self.graph_data = None
        
        # Créer l'interface
        self.create_ui()
        
        # Connecter les signaux
        self.connect_signals()
        
        # Status bar
        self.statusBar().showMessage("Prêt • Créez un graphe ou ouvrez un fichier")
    
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
        
        # Groupe Fichier
        new_action = QAction("📄 Nouveau", self)
        new_action.setShortcut(QKeySequence.New)
        new_action.setToolTip("Créer un nouveau graphe (Ctrl+N)")
        new_action.triggered.connect(self.new_graph)
        
        open_action = QAction("📂 Ouvrir...", self)
        open_action.setShortcut(QKeySequence.Open)
        open_action.setToolTip("Ouvrir un fichier JSON (Ctrl+O)")
        open_action.triggered.connect(self.open_graph)
        
        save_action = QAction("💾 Sauvegarder", self)
        save_action.setShortcut(QKeySequence.Save)
        save_action.setToolTip("Sauvegarder le graphe (Ctrl+S)")
        save_action.triggered.connect(self.save_graph)
        
        save_as_action = QAction("💾 Sauvegarder sous...", self)
        save_as_action.setShortcut(QKeySequence.SaveAs)
        save_as_action.setToolTip("Sauvegarder le graphe sous un nouveau nom (Ctrl+Shift+S)")
        save_as_action.triggered.connect(self.save_graph_as)
        
        toolbar.addAction(new_action)
        toolbar.addAction(open_action)
        toolbar.addAction(save_action)
        toolbar.addAction(save_as_action)
        
        toolbar.addSeparator()
        
        # Groupe Solution
        run_action = QAction("⚡ Résoudre", self)
        run_action.setShortcut(Qt.Key_F5)
        run_action.setToolTip("Résoudre le problème (F5)")
        run_action.triggered.connect(self.solve_problem)
        
        export_json_action = QAction("📤 Exporter JSON", self)
        export_json_action.setToolTip("Exporter la solution en JSON")
        export_json_action.triggered.connect(self.export_solution_json)
        
        export_csv_action = QAction("📊 Exporter CSV", self)
        export_csv_action.setToolTip("Exporter la solution en CSV")
        export_csv_action.triggered.connect(self.export_solution_csv)
        
        toolbar.addAction(run_action)
        toolbar.addSeparator()
        toolbar.addAction(export_json_action)
        toolbar.addAction(export_csv_action)
        
        # Info fichier actuel
        toolbar.addSeparator()
        self.file_label = QLabel("Non sauvegardé")
        self.file_label.setStyleSheet("""
            QLabel {
                color: #6b7280;
                font-style: italic;
                padding: 0 10px;
            }
        """)
        toolbar.addWidget(self.file_label)
    
    def connect_signals(self):
        """Connecte les signaux entre les widgets"""
        # Quand le graphe change, mettre à jour les paramètres
        self.graph_widget.graph_changed.connect(self.on_graph_changed)
        
        # Quand on clique sur "Résoudre"
        self.params_widget.solve_clicked.connect(self.solve_problem)
        
        # Quand les résultats veulent exporter
        self.results_widget.export_json_requested.connect(self.export_solution_json)
        self.results_widget.export_csv_requested.connect(self.export_solution_csv)
    
    def on_graph_changed(self, graph_data):
        """Quand le graphe change"""
        self.graph_data = graph_data
        self.params_widget.update_from_graph(graph_data)
        
        # Marquer comme non sauvegardé
        if self.current_file:
            self.file_label.setText(f"*{os.path.basename(self.current_file)}")
        else:
            self.file_label.setText("*Non sauvegardé")
    
    def new_graph(self):
        """Crée un nouveau graphe vide"""
        if self.check_unsaved_changes():
            return
        
        self.graph_widget.clear_scene()
        self.params_widget.clear()
        self.results_widget.clear()
        self.solution = None
        self.current_file = None
        self.file_label.setText("Non sauvegardé")
        self.statusBar().showMessage("Nouveau graphe créé • Prêt à ajouter des sommets")
        
        # Ajouter un exemple si le graphe est vide
        if self.graph_widget.is_empty():
            self.show_welcome_message()
    
    def show_welcome_message(self):
        """Affiche un message de bienvenue avec des exemples"""
        QTimer.singleShot(500, lambda: QMessageBox.information(
            self, 
            "Bienvenue dans Surveillance Network Optimizer",
            "🎯 <b>Créez votre réseau de surveillance</b><br><br>"
            "1. <b>Ajouter des sommets</b> : Cliquez sur 'Ajouter Sommet' puis sur la zone de dessin<br>"
            "2. <b>Créer des arêtes</b> : Mode 'Ajouter Arête', cliquez sur 2 sommets<br>"
            "3. <b>Définir les coûts</b> : Modifiez les valeurs dans le tableau<br>"
            "4. <b>Résoudre</b> : Cliquez sur 'Résoudre' pour optimiser<br><br>"
            "💡 <i>Astuce : Ouvrez un fichier d'exemple depuis le menu Fichier</i>",
            QMessageBox.Ok
        ))
    
    def check_unsaved_changes(self):
        """Vérifie s'il y a des changements non sauvegardés"""
        if self.graph_data and self.current_file:
            # Vérifier si le graphe a changé depuis le dernier chargement/sauvegarde
            # Pour simplifier, on demande toujours
            reply = QMessageBox.question(
                self, 
                "Changements non sauvegardés",
                "Voulez-vous sauvegarder les changements avant de continuer ?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                QMessageBox.Save
            )
            
            if reply == QMessageBox.Save:
                return self.save_graph()
            elif reply == QMessageBox.Cancel:
                return True  # Annuler l'opération
        
        return False
    
    def open_graph(self):
        """Ouvre un graphe depuis un fichier JSON"""
        if self.check_unsaved_changes():
            return
        
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Ouvrir un fichier de graphe",
            "",
            "Fichiers JSON (*.json);;Tous les fichiers (*)"
        )
        
        if not filename:
            return
        
        # Afficher une boîte de dialogue de progression
        progress = QProgressDialog("Chargement du fichier...", "Annuler", 0, 100, self)
        progress.setWindowTitle("Chargement")
        progress.setWindowModality(Qt.WindowModal)
        progress.setValue(10)
        
        # Charger le fichier
        result = load_graph_from_file(filename)
        
        progress.setValue(50)
        
        if not result['success']:
            progress.close()
            QMessageBox.critical(self, "Erreur de chargement", result['error'])
            return
        
        # Valider les données
        graph_data = result['graph_data']
        is_valid, error_msg = validate_graph_data(graph_data)
        
        progress.setValue(70)
        
        if not is_valid:
            progress.close()
            QMessageBox.critical(self, "Données invalides", error_msg)
            return
        
        # Charger le graphe dans l'interface
        try:
            self.graph_widget.load_graph_data(graph_data)
            self.params_widget.update_from_graph(graph_data)
            
            # Charger les paramètres
            parameters = result.get('parameters', {})
            if parameters:
                self.params_widget.set_parameters(parameters)
            
            # Charger la solution si elle existe
            solution = result.get('solution')
            if solution:
                self.solution = solution
                self.results_widget.display_solution(solution)
                self.graph_widget.highlight_solution(solution.get('selected_vertices', []))
            
            # Mettre à jour l'état
            self.current_file = filename
            self.file_label.setText(os.path.basename(filename))
            
            metadata = result.get('metadata', {})
            save_date = metadata.get('save_date', 'Date inconnue')
            
            progress.setValue(100)
            progress.close()
            
            self.statusBar().showMessage(
                f"Fichier chargé : {os.path.basename(filename)} • "
                f"{len(graph_data['vertices'])} sommets, {len(graph_data['edges'])} arêtes"
            )
            
            # Afficher un message d'information
            QMessageBox.information(
                self,
                "Fichier chargé",
                f"<b>{os.path.basename(filename)}</b><br><br>"
                f"• {len(graph_data['vertices'])} sommets<br>"
                f"• {len(graph_data['edges'])} arêtes<br>"
                f"• Sauvegardé le : {save_date[:10] if 'T' in save_date else save_date}"
            )
            
        except Exception as e:
            progress.close()
            QMessageBox.critical(
                self,
                "Erreur d'affichage",
                f"Impossible d'afficher le graphe : {str(e)}"
            )
    
    def save_graph(self):
        """Sauvegarde le graphe dans le fichier courant"""
        if self.current_file:
            return self._save_to_file(self.current_file)
        else:
            return self.save_graph_as()
    
    def save_graph_as(self):
        """Sauvegarde le graphe sous un nouveau nom"""
        default_name = f"surveillance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Sauvegarder le graphe",
            default_name,
            "Fichiers JSON (*.json);;Tous les fichiers (*)"
        )
        
        if not filename:
            return False
        
        return self._save_to_file(filename)
    
    def _save_to_file(self, filename):
        """Sauvegarde dans un fichier spécifique"""
        if not self.graph_data:
            QMessageBox.warning(self, "Avertissement", "Aucun graphe à sauvegarder.")
            return False
        
        # Récupérer les données actuelles
        graph_data = self.graph_widget.get_graph_data()
        parameters = self.params_widget.get_parameters()
        
        # Afficher une boîte de progression
        progress = QProgressDialog("Sauvegarde en cours...", "Annuler", 0, 100, self)
        progress.setWindowTitle("Sauvegarde")
        progress.setWindowModality(Qt.WindowModal)
        progress.setValue(30)
        
        # Sauvegarder
        result = save_graph_to_file(graph_data, parameters, self.solution, filename)
        
        progress.setValue(80)
        
        if not result['success']:
            progress.close()
            QMessageBox.critical(self, "Erreur de sauvegarde", result['error'])
            return False
        
        # Mettre à jour l'état
        self.current_file = filename
        self.file_label.setText(os.path.basename(filename))
        
        progress.setValue(100)
        progress.close()
        
        self.statusBar().showMessage(f"Fichier sauvegardé : {os.path.basename(filename)}")
        
        # Afficher un message de confirmation
        QMessageBox.information(
            self,
            "Sauvegarde réussie",
            f"Le graphe a été sauvegardé dans :<br><b>{os.path.basename(filename)}</b>"
        )
        
        return True
    
    def export_solution_json(self):
        """Exporte la solution en JSON"""
        if not self.solution:
            QMessageBox.warning(self, "Avertissement", "Aucune solution à exporter.")
            return
        
        default_name = f"solution_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Exporter la solution en JSON",
            default_name,
            "Fichiers JSON (*.json);;Tous les fichiers (*)"
        )
        
        if not filename:
            return
        
        # Afficher une boîte de progression
        progress = QProgressDialog("Export en cours...", "Annuler", 0, 100, self)
        progress.setWindowTitle("Export JSON")
        progress.setWindowModality(Qt.WindowModal)
        progress.setValue(30)
        
        # Exporter
        graph_data = self.graph_widget.get_graph_data()
        parameters = self.params_widget.get_parameters()
        
        result = export_solution_to_json(self.solution, graph_data, parameters, filename)
        
        progress.setValue(80)
        
        if not result['success']:
            progress.close()
            QMessageBox.critical(self, "Erreur d'export", result['error'])
            return
        
        progress.setValue(100)
        progress.close()
        
        self.statusBar().showMessage(f"Solution exportée en JSON : {os.path.basename(filename)}")
        
        QMessageBox.information(
            self,
            "Export réussi",
            f"La solution a été exportée dans :<br><b>{os.path.basename(filename)}</b>"
        )
    
    def export_solution_csv(self):
        """Exporte la solution en CSV"""
        if not self.solution:
            QMessageBox.warning(self, "Avertissement", "Aucune solution à exporter.")
            return
        
        default_name = f"rapport_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Exporter le rapport en CSV",
            default_name,
            "Fichiers CSV (*.csv);;Tous les fichiers (*)"
        )
        
        if not filename:
            return
        
        # Afficher une boîte de progression
        progress = QProgressDialog("Export en cours...", "Annuler", 0, 100, self)
        progress.setWindowTitle("Export CSV")
        progress.setWindowModality(Qt.WindowModal)
        progress.setValue(30)
        
        # Exporter
        result = export_solution_to_csv(self.solution, filename)
        
        progress.setValue(80)
        
        if not result['success']:
            progress.close()
            QMessageBox.critical(self, "Erreur d'export", result['error'])
            return
        
        progress.setValue(100)
        progress.close()
        
        self.statusBar().showMessage(f"Rapport exporté en CSV : {os.path.basename(filename)}")
        
        QMessageBox.information(
            self,
            "Export réussi",
            f"Le rapport a été exporté dans :<br><b>{os.path.basename(filename)}</b>"
        )
    
    def solve_problem(self):
        """Résout le problème de couverture de sommets"""
        # Récupérer les données du graphe
        graph_data = self.graph_widget.get_graph_data()
        
        # Récupérer les paramètres
        params = self.params_widget.get_parameters()
        
        # Valider qu'on a un graphe
        if not graph_data['vertices']:
            QMessageBox.warning(self, "Avertissement", "Le graphe est vide ! Ajoutez des sommets.")
            return
        
        # Valider les coûts
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
        self.statusBar().showMessage("⚡ Résolution en cours...")
        self.results_widget.show_loading()
        
        # Créer et lancer le worker
        self.solver_worker = SolverWorker(graph_data, params)
        
        # Connecter les signaux du worker
        self.solver_worker.started.connect(self.on_solver_started)
        self.solver_worker.finished.connect(self.on_solver_finished)
        self.solver_worker.error.connect(self.on_solver_error)
        self.solver_worker.progress.connect(self.on_solver_progress)
        
        # Lancer le worker
        self.solver_worker.start()
    
    def on_solver_started(self):
        """Début de la résolution"""
        self.statusBar().showMessage("⚡ Initialisation du solveur...")
    
    def on_solver_finished(self, solution):
        """Fin de la résolution avec succès"""
        # Réactiver le bouton
        self.params_widget.solve_button.setEnabled(True)
        
        # Stocker la solution
        self.solution = solution
        
        # Afficher les résultats
        status = solution['status']
        
        if status in ['optimal', 'suboptimal']:
            self.results_widget.display_solution(solution)
            self.graph_widget.highlight_solution(solution['selected_vertices'])
            
            # Message selon le statut
            if status == 'optimal':
                prefix = "✅ Solution OPTIMALE"
            else:
                prefix = "⚠️ Solution SOUS-OPTIMALE"
            
            # Informations supplémentaires
            gap_info = ""
            if 'gap' in solution and solution['gap'] > 0:
                gap_info = f" (Gap: {solution['gap']*100:.2f}%)"
            
            time_msg = f" en {solution.get('solve_time', 0):.2f} secondes"
            
            status_msg = f"{prefix} ! Coût : {solution['total_cost']:.2f}€{gap_info}{time_msg}"
            self.statusBar().showMessage(status_msg)
            
        elif status == 'infeasible':
            self.statusBar().showMessage("❌ Problème insoluble avec les contraintes actuelles")
            self.results_widget.display_solution(solution)
            
            QMessageBox.warning(
                self,
                "Problème Insoluble",
                f"Le problème est insoluble avec les contraintes données.\n\n"
                f"Raisons possibles :\n"
                f"• Budget trop faible\n"
                f"• Trop de sommets interdits\n"
                f"• Contradiction entre sommets obligatoires et arêtes critiques\n\n"
                f"Message : {solution.get('message', '')}"
            )
            
        elif status == 'error':
            self.statusBar().showMessage(f"❌ Erreur : {solution.get('message', '')[:50]}...")
            self.results_widget.display_solution(solution)
            
            QMessageBox.critical(
                self,
                "Erreur du Solveur",
                f"Une erreur est survenue :\n\n{solution.get('message', 'Erreur inconnue')}"
            )
            
        else:
            self.statusBar().showMessage(f"⚠️ {solution.get('message', 'Statut inconnu')}")
            self.results_widget.display_solution(solution)
    
    def on_solver_error(self, error_message):
        """Erreur pendant la résolution"""
        self.params_widget.solve_button.setEnabled(True)
        self.statusBar().showMessage(f"❌ Erreur : {error_message[:50]}...")
        QMessageBox.critical(
            self,
            "Erreur du Solveur",
            f"Une erreur est survenue pendant la résolution :\n\n{error_message}"
        )
    
    def on_solver_progress(self, progress, message):
        """Mise à jour de la progression"""
        self.statusBar().showMessage(f"⚡ {message}...")