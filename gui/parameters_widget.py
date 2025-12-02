from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QTableWidget, QTableWidgetItem, QGroupBox,
                             QPushButton, QLabel, QSpinBox, QComboBox,
                             QCheckBox, QHeaderView)
from PyQt5.QtCore import Qt, pyqtSignal

class ParametersWidget(QWidget):
    solve_clicked = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.graph_data = None
        self.create_ui()
    
    def create_ui(self):
        """Crée l'interface du panneau paramètres"""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        # Titre
        title = QLabel("Paramètres du Problème")
        title.setStyleSheet("font-size: 14pt; font-weight: bold;")
        layout.addWidget(title)
        
        # Table des coûts
        self.costs_group = QGroupBox("Coûts des Sommets")
        costs_layout = QVBoxLayout()
        
        self.costs_table = QTableWidget()
        self.costs_table.setColumnCount(3)
        self.costs_table.setHorizontalHeaderLabels(["Sommet", "Coût (€)", "Type"])
        self.costs_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        costs_layout.addWidget(self.costs_table)
        
        self.costs_group.setLayout(costs_layout)
        layout.addWidget(self.costs_group)
        
        # Contraintes
        constraints_group = QGroupBox("Contraintes")
        constraints_layout = QVBoxLayout()
        
        # Budget
        budget_layout = QHBoxLayout()
        budget_layout.addWidget(QLabel("Budget maximum :"))
        self.budget_spin = QSpinBox()
        self.budget_spin.setRange(0, 1000000)
        self.budget_spin.setValue(0)
        self.budget_spin.setSpecialValueText("Illimité")
        budget_layout.addWidget(self.budget_spin)
        budget_layout.addWidget(QLabel("€"))
        budget_layout.addStretch()
        constraints_layout.addLayout(budget_layout)
        
        # Options avancées
        self.advanced_check = QCheckBox("Options avancées")
        self.advanced_check.toggled.connect(self.toggle_advanced)
        constraints_layout.addWidget(self.advanced_check)
        
        # Options avancées (cachées par défaut)
        self.advanced_group = QGroupBox()
        advanced_layout = QVBoxLayout()
        
        self.min_cover_check = QCheckBox("Couverture minimum garantie")
        advanced_layout.addWidget(self.min_cover_check)
        
        self.redundancy_spin = QSpinBox()
        self.redundancy_spin.setRange(1, 5)
        self.redundancy_spin.setValue(1)
        redundancy_layout = QHBoxLayout()
        redundancy_layout.addWidget(QLabel("Redondance :"))
        redundancy_layout.addWidget(self.redundancy_spin)
        redundancy_layout.addWidget(QLabel("couverture(s) par arête"))
        advanced_layout.addLayout(redundancy_layout)
        
        self.advanced_group.setLayout(advanced_layout)
        self.advanced_group.setVisible(False)
        constraints_layout.addWidget(self.advanced_group)
        
        constraints_group.setLayout(constraints_layout)
        layout.addWidget(constraints_group)
        
        # Bouton Résoudre
        self.solve_button = QPushButton("RÉSOUDRE LE PROBLÈME")
        self.solve_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                padding: 12px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.solve_button.clicked.connect(self.solve_clicked.emit)
        layout.addWidget(self.solve_button)
        
        layout.addStretch()
    
    def update_from_graph(self, graph_data):
        """Met à jour les paramètres depuis le graphe"""
        self.graph_data = graph_data
        
        # Mettre à jour la table des coûts
        self.costs_table.setRowCount(len(graph_data['vertices']))
        
        for i, vertex in enumerate(graph_data['vertices']):
            # Sommet
            item = QTableWidgetItem(vertex['id'])
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            self.costs_table.setItem(i, 0, item)
            
            # Coût
            cost_item = QTableWidgetItem(str(vertex['cost']))
            self.costs_table.setItem(i, 1, cost_item)
            
            # Type
            type_combo = QComboBox()
            type_combo.addItems(["Normal", "Obligatoire", "Interdit"])
            type_combo.setCurrentText(vertex['type'].capitalize())
            self.costs_table.setCellWidget(i, 2, type_combo)
        
        # Adapter la hauteur de la table
        self.costs_table.setMinimumHeight(30 + len(graph_data['vertices']) * 30)
    
    def get_parameters(self):
        """Récupère tous les paramètres"""
        if not self.graph_data:
            return {}
        
        params = {
            'budget': self.budget_spin.value() if self.budget_spin.value() > 0 else None,
            'advanced': {
                'min_cover': self.min_cover_check.isChecked(),
                'redundancy': self.redundancy_spin.value() if self.min_cover_check.isChecked() else 1
            }
        }
        
        # Récupérer les coûts et types depuis la table
        vertex_params = {}
        for i in range(self.costs_table.rowCount()):
            vertex_id = self.costs_table.item(i, 0).text()
            cost = float(self.costs_table.item(i, 1).text())
            type_combo = self.costs_table.cellWidget(i, 2)
            vertex_type = type_combo.currentText().lower()
            
            vertex_params[vertex_id] = {
                'cost': cost,
                'type': vertex_type
            }
        
        params['vertices'] = vertex_params
        return params
    
    def toggle_advanced(self, checked):
        """Affiche/cache les options avancées"""
        self.advanced_group.setVisible(checked)
    
    def clear(self):
        """Réinitialise le panneau"""
        self.costs_table.setRowCount(0)
        self.budget_spin.setValue(0)
        self.min_cover_check.setChecked(False)
        self.redundancy_spin.setValue(1)
        self.advanced_check.setChecked(False)