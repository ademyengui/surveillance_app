from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QTextEdit, QTableWidget,
                             QTableWidgetItem, QPushButton, QGroupBox,
                             QHeaderView, QProgressBar)
from PyQt5.QtCore import (Qt, pyqtSignal)
import json

class ResultsWidget(QWidget):
    export_json_requested = pyqtSignal()
    export_csv_requested = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.create_ui()
    
    def create_ui(self):
        """Crée l'interface du panneau résultats"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Titre
        title = QLabel("📊 RÉSULTATS")
        title.setObjectName("title")
        title.setStyleSheet("""
            QLabel#title {
                font-size: 18px;
                font-weight: 700;
                color: #1f2937;
                padding-bottom: 10px;
                border-bottom: 2px solid #10b981;
                margin-bottom: 10px;
            }
        """)
        layout.addWidget(title)
        
        # Résumé
        self.summary_group = QGroupBox("Résumé de la Solution")
        summary_layout = QVBoxLayout()
        
        # Coût total
        cost_widget = QWidget()
        cost_layout = QHBoxLayout(cost_widget)
        cost_layout.setContentsMargins(0, 0, 0, 0)
        
        cost_label = QLabel("Coût total :")
        cost_label.setStyleSheet("font-weight: 600; font-size: 14px;")
        
        self.cost_value = QLabel("-- €")
        self.cost_value.setStyleSheet("font-size: 24px; font-weight: 700; color: #10b981;")
        
        cost_layout.addWidget(cost_label)
        cost_layout.addWidget(self.cost_value)
        cost_layout.addStretch()
        
        summary_layout.addWidget(cost_widget)
        
        # Statut
        status_widget = QWidget()
        status_layout = QHBoxLayout(status_widget)
        status_layout.setContentsMargins(0, 0, 0, 0)
        
        status_label = QLabel("Statut :")
        status_label.setStyleSheet("font-weight: 600;")
        
        self.status_value = QLabel("--")
        self.status_value.setStyleSheet("font-weight: 500;")
        
        status_layout.addWidget(status_label)
        status_layout.addWidget(self.status_value)
        status_layout.addStretch()
        
        summary_layout.addWidget(status_widget)
        
        # Sommets sélectionnés
        vertices_widget = QWidget()
        vertices_layout = QHBoxLayout(vertices_widget)
        vertices_layout.setContentsMargins(0, 0, 0, 0)
        
        vertices_label = QLabel("Sommets sélectionnés :")
        vertices_label.setStyleSheet("font-weight: 600;")
        
        self.vertices_value = QLabel("--")
        
        vertices_layout.addWidget(vertices_label)
        vertices_layout.addWidget(self.vertices_value)
        vertices_layout.addStretch()
        
        summary_layout.addWidget(vertices_widget)
        
        # Temps de résolution
        self.time_label = QLabel("Temps de résolution : --")
        self.time_label.setStyleSheet("color: #6b7280; font-size: 12px;")
        summary_layout.addWidget(self.time_label)
        
        self.summary_group.setLayout(summary_layout)
        layout.addWidget(self.summary_group)
        
        # Détails
        details_group = QGroupBox("Détails des Sommets Sélectionnés")
        details_layout = QVBoxLayout()
        
        self.details_table = QTableWidget()
        self.details_table.setColumnCount(3)
        self.details_table.setHorizontalHeaderLabels(["Sommet", "Coût (€)", "Type"])
        self.details_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.details_table.setMaximumHeight(150)
        
        # Style de la table
        self.details_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #e5e7eb;
                border-radius: 6px;
            }
            QTableWidget::item {
                padding: 6px;
                text-align: center;
            }
            QHeaderView::section {
                background-color: #f3f4f6;
                font-weight: 600;
                padding: 8px;
                border: none;
                border-bottom: 2px solid #d1d5db;
            }
        """)
        
        details_layout.addWidget(self.details_table)
        
        details_group.setLayout(details_layout)
        layout.addWidget(details_group)
        
        # Couverture
        coverage_group = QGroupBox("Couverture des Arêtes")
        coverage_layout = QVBoxLayout()
        
        self.coverage_text = QTextEdit()
        self.coverage_text.setReadOnly(True)
        self.coverage_text.setMaximumHeight(120)
        self.coverage_text.setStyleSheet("""
            QTextEdit {
                background-color: #f9fafb;
                border: 1px solid #e5e7eb;
                border-radius: 6px;
                font-family: 'Courier New', monospace;
                font-size: 12px;
                padding: 8px;
            }
        """)
        coverage_layout.addWidget(self.coverage_text)
        
        coverage_group.setLayout(coverage_layout)
        layout.addWidget(coverage_group)
        
        # Boutons d'export
        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        button_layout.setContentsMargins(0, 0, 0, 0)
        
        self.export_json_btn = QPushButton("💾 Exporter JSON")
        self.export_json_btn.setObjectName("export-button")
        self.export_json_btn.clicked.connect(self.export_json)
        
        self.export_csv_btn = QPushButton("📊 Exporter CSV")
        self.export_csv_btn.setObjectName("export-button")
        self.export_csv_btn.clicked.connect(self.export_csv)
        
        self.copy_btn = QPushButton("📋 Copier Résumé")
        self.copy_btn.setObjectName("export-button")
        self.copy_btn.clicked.connect(self.copy_summary)
        
        # Style des boutons
        button_style = """
            QPushButton {
                background-color: #3b82f6;
                color: white;
                padding: 8px 12px;
                border-radius: 6px;
                font-weight: 500;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
            QPushButton:pressed {
                background-color: #1d4ed8;
            }
        """
        self.export_json_btn.setStyleSheet(button_style)
        self.export_csv_btn.setStyleSheet(button_style)
        self.copy_btn.setStyleSheet(button_style)
        
        button_layout.addWidget(self.export_json_btn)
        button_layout.addWidget(self.export_csv_btn)
        button_layout.addWidget(self.copy_btn)
        button_layout.addStretch()
        
        layout.addWidget(button_widget)
        
        layout.addStretch()
    
    def display_solution(self, solution):
        """Affiche la solution"""
        if solution['status'] != 'optimal':
            self.show_error(solution)
            return
        
        # Résumé
        self.cost_value.setText(f"{solution['total_cost']:.2f} €")
        
        selected = solution['selected_vertices']
        self.vertices_value.setText(f"{len(selected)} sommets")
        
        # Déterminer l'icône de statut
        status_icon = {
            'optimal': '✅',
            'infeasible': '❌',
            'unbounded': '⚠️',
            'error': '🚫'
        }.get(solution['status'], '❓')
        
        status_text = {
            'optimal': 'Solution Optimale',
            'infeasible': 'Problème Insoluble',
            'unbounded': 'Problème Non Borné',
            'error': 'Erreur'
        }.get(solution['status'], solution['status'])
        
        self.status_value.setText(f"{status_icon} {status_text}")
        
        # Temps de résolution
        if 'solve_time' in solution:
            self.time_label.setText(f"Temps de résolution : {solution['solve_time']:.3f} secondes")
        
        # Détails dans la table
        self.details_table.setRowCount(len(selected))
        for i, vertex_id in enumerate(selected):
            # ID du sommet
            item_id = QTableWidgetItem(vertex_id)
            item_id.setTextAlignment(Qt.AlignCenter)
            self.details_table.setItem(i, 0, item_id)
            
            # Coût du sommet
            cost = solution.get('detailed_costs', {}).get(vertex_id, '?')
            item_cost = QTableWidgetItem(f"{cost}")
            item_cost.setTextAlignment(Qt.AlignCenter)
            self.details_table.setItem(i, 1, item_cost)
            
            # Type
            item_type = QTableWidgetItem("✓ Sélectionné")
            item_type.setTextAlignment(Qt.AlignCenter)
            item_type.setForeground(Qt.darkGreen)
            self.details_table.setItem(i, 2, item_type)
        
        # Couverture des arêtes
        coverage_text = "Détail de la couverture des arêtes :\n"
        coverage_text += "═" * 40 + "\n"
        
        if 'cover_details' in solution and solution['cover_details']:
            for edge, covering_vertices in solution['cover_details'].items():
                if covering_vertices:
                    status_icon = "✅"
                    coverage_text += f"{status_icon} {edge} → {', '.join(covering_vertices)}\n"
                else:
                    status_icon = "❌"
                    coverage_text += f"{status_icon} {edge} → Non couverte\n"
        else:
            coverage_text += "Aucun détail de couverture disponible.\n"
        
        self.coverage_text.setText(coverage_text)
    
    def show_loading(self):
        """Affiche un indicateur de chargement"""
        self.cost_value.setText("Calcul...")
        self.vertices_value.setText("--")
        self.status_value.setText("⚡ En cours...")
        self.time_label.setText("Temps de résolution : --")
        self.details_table.setRowCount(0)
        self.coverage_text.setText("Résolution en cours...\nVeuillez patienter.")
    
    def show_error(self, solution):
        """Affiche un message d'erreur"""
        self.cost_value.setText("-- €")
        self.vertices_value.setText("--")
        
        status_icon = {
            'infeasible': '❌',
            'unbounded': '⚠️',
            'error': '🚫'
        }.get(solution['status'], '❓')
        
        self.status_value.setText(f"{status_icon} {solution['status']}")
        self.time_label.setText("Temps de résolution : --")
        self.details_table.setRowCount(0)
        self.coverage_text.setText(f"Erreur : {solution.get('message', 'Inconnue')}")
    
    def clear(self):
        """Efface les résultats"""
        self.cost_value.setText("-- €")
        self.vertices_value.setText("--")
        self.status_value.setText("--")
        self.time_label.setText("Temps de résolution : --")
        self.details_table.setRowCount(0)
        self.coverage_text.clear()
    
    def export_json(self):
        """Exporte les résultats en JSON"""
        # À implémenter avec QFileDialog
        print("Export JSON - à implémenter")
    
    def export_csv(self):
        """Exporte les résultats en CSV"""
        # À implémenter avec QFileDialog
        print("Export CSV - à implémenter")
    
    def copy_summary(self):
        """Copie le résumé dans le presse-papier"""
        # À implémenter avec QClipboard
        print("Copie - à implémenter")
    
    def export_json(self):
        """Émet un signal pour exporter en JSON"""
        self.export_json_requested.emit()
    def export_csv(self):
        """Émet un signal pour exporter en CSV"""
        self.export_csv_requested.emit()