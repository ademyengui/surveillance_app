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
        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Titre stylé
        title = QLabel("⚙️ PARAMÈTRES DU PROBLÈME")
        title.setObjectName("title")
        title.setStyleSheet("""
            QLabel#title {
                font-size: 18px;
                font-weight: 700;
                color: #1f2937;
                padding-bottom: 10px;
                border-bottom: 2px solid #3b82f6;
                margin-bottom: 10px;
            }
        """)
        layout.addWidget(title)
        
        # Table des coûts
        self.costs_group = QGroupBox("Coûts des Sommets")
        costs_layout = QVBoxLayout()
        
        self.costs_table = QTableWidget()
        self.costs_table.setColumnCount(3)
        self.costs_table.setHorizontalHeaderLabels(["Sommet", "Coût (€)", "Type"])
        self.costs_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.costs_table.setMaximumHeight(200)
        
        # Style de la table
        self.costs_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #e5e7eb;
                border-radius: 6px;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QHeaderView::section {
                background-color: #f3f4f6;
                font-weight: 600;
                padding: 10px;
                border: none;
                border-bottom: 2px solid #d1d5db;
            }
        """)
        
        costs_layout.addWidget(self.costs_table)
        
        self.costs_group.setLayout(costs_layout)
        layout.addWidget(self.costs_group)
        
        # Contraintes
        constraints_group = QGroupBox("Contraintes")
        constraints_layout = QVBoxLayout()
        
        # Budget
        budget_widget = QWidget()
        budget_layout = QHBoxLayout(budget_widget)
        budget_layout.setContentsMargins(0, 0, 0, 0)
        
        budget_label = QLabel("Budget maximum :")
        budget_label.setStyleSheet("font-weight: 500;")
        
        self.budget_spin = QSpinBox()
        self.budget_spin.setRange(0, 1000000)
        self.budget_spin.setValue(0)
        self.budget_spin.setSingleStep(10)
        self.budget_spin.setSpecialValueText("Illimité")
        self.budget_spin.setStyleSheet("""
            QSpinBox {
                padding: 8px;
                border: 2px solid #d1d5db;
                border-radius: 6px;
                min-width: 100px;
            }
            QSpinBox:focus {
                border-color: #3b82f6;
            }
        """)
        
        budget_unit = QLabel("€")
        budget_unit.setStyleSheet("color: #6b7280;")
        
        budget_layout.addWidget(budget_label)
        budget_layout.addWidget(self.budget_spin)
        budget_layout.addWidget(budget_unit)
        budget_layout.addStretch()
        
        constraints_layout.addWidget(budget_widget)
        
        # Options avancées
        self.advanced_check = QCheckBox("Options avancées")
        self.advanced_check.setStyleSheet("""
            QCheckBox {
                font-weight: 500;
                padding: 8px 0;
            }
        """)
        self.advanced_check.toggled.connect(self.toggle_advanced)
        constraints_layout.addWidget(self.advanced_check)
        
        # Options avancées (cachées par défaut)
        self.advanced_group = QGroupBox()
        advanced_layout = QVBoxLayout()
        
        self.min_cover_check = QCheckBox("Couverture minimum garantie")
        self.min_cover_check.setStyleSheet("padding: 5px 0;")
        advanced_layout.addWidget(self.min_cover_check)
        
        # Redondance
        redundancy_widget = QWidget()
        redundancy_layout = QHBoxLayout(redundancy_widget)
        redundancy_layout.setContentsMargins(0, 0, 0, 0)
        
        redundancy_label = QLabel("Redondance :")
        redundancy_label.setStyleSheet("font-weight: 500;")
        
        self.redundancy_spin = QSpinBox()
        self.redundancy_spin.setRange(1, 5)
        self.redundancy_spin.setValue(1)
        self.redundancy_spin.setEnabled(False)
        self.redundancy_spin.setStyleSheet("""
            QSpinBox {
                padding: 6px;
                border: 2px solid #d1d5db;
                border-radius: 4px;
                min-width: 60px;
            }
        """)
        
        redundancy_unit = QLabel("couverture(s) par arête")
        redundancy_unit.setStyleSheet("color: #6b7280; font-size: 13px;")
        
        redundancy_layout.addWidget(redundancy_label)
        redundancy_layout.addWidget(self.redundancy_spin)
        redundancy_layout.addWidget(redundancy_unit)
        redundancy_layout.addStretch()
        
        advanced_layout.addWidget(redundancy_widget)
        
        # Connecter le signal pour activer/désactiver le spin de redondance
        self.min_cover_check.toggled.connect(self.redundancy_spin.setEnabled)
        
        self.advanced_group.setLayout(advanced_layout)
        self.advanced_group.setVisible(False)
        constraints_layout.addWidget(self.advanced_group)
        
        constraints_group.setLayout(constraints_layout)
        layout.addWidget(constraints_group)
        
        # Bouton Résoudre
        self.solve_button = QPushButton("⚡ RÉSOUDRE LE PROBLÈME")
        self.solve_button.setObjectName("solve-button")
        self.solve_button.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
                color: white;
                font-weight: bold;
                padding: 15px;
                border-radius: 8px;
                font-size: 16px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #0da271;
            }
            QPushButton:pressed {
                background-color: #0c9668;
            }
            QPushButton:disabled {
                background-color: #9ca3af;
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
            item.setTextAlignment(Qt.AlignCenter)
            self.costs_table.setItem(i, 0, item)
            
            # Coût
            cost_item = QTableWidgetItem(str(vertex.get('cost', 1.0)))
            cost_item.setTextAlignment(Qt.AlignCenter)
            self.costs_table.setItem(i, 1, cost_item)
            
            # Type
            type_combo = QComboBox()
            type_combo.addItems(["Normal", "Obligatoire", "Interdit"])
            
            # Déterminer le type actuel
            vertex_type = vertex.get('type', 'normal')
            if vertex_type == 'mandatory':
                type_combo.setCurrentText("Obligatoire")
            elif vertex_type == 'forbidden':
                type_combo.setCurrentText("Interdit")
            else:
                type_combo.setCurrentText("Normal")
            
            self.costs_table.setCellWidget(i, 2, type_combo)
        
        # Adapter la hauteur de la table
        row_height = 40
        self.costs_table.setMinimumHeight(min(200, 40 + len(graph_data['vertices']) * row_height))
    
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
            
            # Coût
            cost_item = self.costs_table.item(i, 1)
            cost = 1.0
            if cost_item:
                try:
                    cost = float(cost_item.text())
                except ValueError:
                    cost = 1.0
            
            # Type
            type_combo = self.costs_table.cellWidget(i, 2)
            vertex_type = 'normal'
            if type_combo:
                type_text = type_combo.currentText().lower()
                if type_text == 'obligatoire':
                    vertex_type = 'mandatory'
                elif type_text == 'interdit':
                    vertex_type = 'forbidden'
            
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
        self.advanced_group.setVisible(False)