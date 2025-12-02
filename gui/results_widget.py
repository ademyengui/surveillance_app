from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QTextEdit, QTableWidget,
                             QTableWidgetItem, QPushButton, QGroupBox,
                             QHeaderView)
from PyQt5.QtCore import Qt
import json

class ResultsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.create_ui()
    
    def create_ui(self):
        """Crée l'interface du panneau résultats"""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        # Titre
        title = QLabel("Résultats")
        title.setStyleSheet("font-size: 14pt; font-weight: bold;")
        layout.addWidget(title)
        
        # Résumé
        self.summary_group = QGroupBox("Résumé de la Solution")
        summary_layout = QVBoxLayout()
        
        self.cost_label = QLabel("Coût total : -- €")
        self.cost_label.setStyleSheet("font-size: 16pt; color: #2E7D32;")
        summary_layout.addWidget(self.cost_label)
        
        self.vertices_label = QLabel("Sommets sélectionnés : --")
        summary_layout.addWidget(self.vertices_label)
        
        self.status_label = QLabel("Statut : --")
        summary_layout.addWidget(self.status_label)
        
        self.summary_group.setLayout(summary_layout)
        layout.addWidget(self.summary_group)
        
        # Détails
        details_group = QGroupBox("Détails de la Solution")
        details_layout = QVBoxLayout()
        
        self.details_table = QTableWidget()
        self.details_table.setColumnCount(3)
        self.details_table.setHorizontalHeaderLabels(["Sommet", "Coût", "Type"])
        self.details_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        details_layout.addWidget(self.details_table)
        
        details_group.setLayout(details_layout)
        layout.addWidget(details_group)
        
        # Couverture
        coverage_group = QGroupBox("Couverture des Arêtes")
        coverage_layout = QVBoxLayout()
        
        self.coverage_text = QTextEdit()
        self.coverage_text.setReadOnly(True)
        self.coverage_text.setMaximumHeight(150)
        coverage_layout.addWidget(self.coverage_text)
        
        coverage_group.setLayout(coverage_layout)
        layout.addWidget(coverage_group)
        
        # Boutons d'export
        button_layout = QHBoxLayout()
        
        self.export_json_btn = QPushButton("Exporter JSON")
        self.export_json_btn.clicked.connect(self.export_json)
        button_layout.addWidget(self.export_json_btn)
        
        self.export_csv_btn = QPushButton("Exporter CSV")
        self.export_csv_btn.clicked.connect(self.export_csv)
        button_layout.addWidget(self.export_csv_btn)
        
        self.copy_btn = QPushButton("Copier Résumé")
        self.copy_btn.clicked.connect(self.copy_summary)
        button_layout.addWidget(self.copy_btn)
        
        layout.addLayout(button_layout)
        
        layout.addStretch()
    
    def display_solution(self, solution):
        """Affiche la solution"""
        # Résumé
        self.cost_label.setText(f"Coût total : {solution['total_cost']} €")
        
        selected = solution['selected_vertices']
        self.vertices_label.setText(f"Sommets sélectionnés : {len(selected)}")
        
        self.status_label.setText(f"Statut : {solution['status']}")
        
        # Détails dans la table
        self.details_table.setRowCount(len(selected))
        for i, vertex_id in enumerate(selected):
            # Ici, on devrait avoir les détails complets du sommet
            # Pour l'instant, on affiche juste l'ID
            self.details_table.setItem(i, 0, QTableWidgetItem(vertex_id))
            self.details_table.setItem(i, 1, QTableWidgetItem("--"))
            self.details_table.setItem(i, 2, QTableWidgetItem("--"))
        
        # Couverture
        coverage_text = "Détail de la couverture :\n"
        if 'cover_details' in solution and solution['cover_details']:
            for edge, covered_by in solution['cover_details'].items():
                coverage_text += f"{edge} → {covered_by}\n"
        else:
            coverage_text += "À calculer..."
        
        self.coverage_text.setText(coverage_text)
    
    def show_loading(self):
        """Affiche un indicateur de chargement"""
        self.cost_label.setText("Calcul en cours...")
        self.vertices_label.setText("--")
        self.status_label.setText("--")
        self.details_table.setRowCount(0)
        self.coverage_text.setText("")
    
    def clear(self):
        """Efface les résultats"""
        self.cost_label.setText("Coût total : -- €")
        self.vertices_label.setText("Sommets sélectionnés : --")
        self.status_label.setText("Statut : --")
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