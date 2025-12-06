from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QTableWidget, QTableWidgetItem, QGroupBox,
                             QPushButton, QLabel, QSpinBox, QComboBox,
                             QCheckBox, QHeaderView)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

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
        self.costs_table.setMaximumHeight(250)
        
        # Style de la table - AMÉLIORÉ pour meilleure lisibilité
        self.costs_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 2px solid #d1d5db;
                border-radius: 6px;
                gridline-color: #e5e7eb;
            }
            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid #f3f4f6;
                color: #111827;
                font-size: 13px;
            }
            QTableWidget::item:selected {
                background-color: #3b82f6;
                color: white;
                font-weight: bold;
            }
            QHeaderView::section {
                background-color: #f3f4f6;
                font-weight: 600;
                font-size: 13px;
                padding: 12px 8px;
                border: none;
                border-bottom: 2px solid #d1d5db;
                color: #111827;
            }
            QTableWidget QComboBox {
                font-size: 13px;
                padding: 6px;
                border: 1px solid #d1d5db;
                border-radius: 4px;
                background-color: white;
                color: #111827;
            }
            QTableWidget QComboBox::drop-down {
                border: none;
            }
            QTableWidget QComboBox::down-arrow {
                image: none;
                border-left: 1px solid #d1d5db;
                padding: 0 8px;
            }
        """)
        
        # Définir une police plus lisible
        font = QFont("Segoe UI", 11)
        self.costs_table.setFont(font)
        
        costs_layout.addWidget(self.costs_table)
        
        # Instructions sous la table
        instructions = QLabel("Double-cliquez sur une cellule pour modifier le coût")
        instructions.setStyleSheet("""
            QLabel {
                color: #6b7280;
                font-size: 11px;
                font-style: italic;
                padding-top: 5px;
            }
        """)
        costs_layout.addWidget(instructions)
        
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
        budget_label.setStyleSheet("font-weight: 500; font-size: 13px;")
        
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
                min-width: 120px;
                font-size: 13px;
                color: #111827;
            }
            QSpinBox:focus {
                border-color: #3b82f6;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                width: 20px;
                border-left: 1px solid #d1d5db;
            }
        """)
        
        budget_unit = QLabel("€")
        budget_unit.setStyleSheet("color: #6b7280; font-size: 13px;")
        
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
                font-size: 13px;
                padding: 8px 0;
                color: #111827;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
        """)
        self.advanced_check.toggled.connect(self.toggle_advanced)
        constraints_layout.addWidget(self.advanced_check)
        
        # Options avancées (cachées par défaut)
        self.advanced_group = QGroupBox("Options avancées")
        self.advanced_group.setStyleSheet("""
            QGroupBox {
                font-weight: 500;
                font-size: 13px;
                border: 1px solid #e5e7eb;
                border-radius: 6px;
                margin-top: 5px;
                padding-top: 10px;
                color: #6b7280;
            }
        """)
        advanced_layout = QVBoxLayout()
        
        self.min_cover_check = QCheckBox("Couverture minimum garantie")
        self.min_cover_check.setStyleSheet("""
            QCheckBox {
                padding: 5px 0;
                font-size: 12px;
                color: #111827;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
            }
        """)
        advanced_layout.addWidget(self.min_cover_check)
        
        # Redondance
        redundancy_widget = QWidget()
        redundancy_layout = QHBoxLayout(redundancy_widget)
        redundancy_layout.setContentsMargins(0, 0, 0, 0)
        
        redundancy_label = QLabel("Redondance :")
        redundancy_label.setStyleSheet("font-weight: 500; font-size: 12px; color: #111827;")
        
        self.redundancy_spin = QSpinBox()
        self.redundancy_spin.setRange(1, 5)
        self.redundancy_spin.setValue(1)
        self.redundancy_spin.setEnabled(False)
        self.redundancy_spin.setStyleSheet("""
            QSpinBox {
                padding: 6px;
                border: 1px solid #d1d5db;
                border-radius: 4px;
                min-width: 60px;
                font-size: 12px;
            }
            QSpinBox:disabled {
                background-color: #f3f4f6;
                color: #9ca3af;
            }
        """)
        
        redundancy_unit = QLabel("couverture(s) par arête")
        redundancy_unit.setStyleSheet("color: #6b7280; font-size: 12px;")
        
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
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                            stop:0 #10b981, stop:1 #0da271);
                color: white;
                font-weight: bold;
                padding: 15px 25px;
                border-radius: 8px;
                font-size: 15px;
                margin-top: 10px;
                border: none;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                            stop:0 #0da271, stop:1 #0c9668);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                            stop:0 #0c9668, stop:1 #0b8a5f);
                padding: 16px 25px 14px 25px;
            }
            QPushButton:disabled {
                background: #9ca3af;
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
            item.setFont(QFont("Segoe UI", 11, QFont.Bold))  # Police améliorée
            self.costs_table.setItem(i, 0, item)
            
            # Coût
            cost_item = QTableWidgetItem(f"{vertex.get('cost', 1.0):.2f}")
            cost_item.setTextAlignment(Qt.AlignCenter)
            cost_item.setFont(QFont("Segoe UI", 11))  # Police améliorée
            self.costs_table.setItem(i, 1, cost_item)
            
            # Type
            type_combo = QComboBox()
            type_combo.addItems(["Normal", "Obligatoire", "Interdit"])
            type_combo.setFont(QFont("Segoe UI", 11))  # Police améliorée
            
            # Déterminer le type actuel
            vertex_type = vertex.get('type', 'normal')
            if vertex_type == 'mandatory':
                type_combo.setCurrentText("Obligatoire")
                type_combo.setStyleSheet("""
                    QComboBox {
                        background-color: #fee2e2;
                        color: #dc2626;
                        font-weight: 500;
                    }
                """)
            elif vertex_type == 'forbidden':
                type_combo.setCurrentText("Interdit")
                type_combo.setStyleSheet("""
                    QComboBox {
                        background-color: #f3f4f6;
                        color: #6b7280;
                        font-weight: 500;
                    }
                """)
            else:
                type_combo.setCurrentText("Normal")
                type_combo.setStyleSheet("""
                    QComboBox {
                        background-color: white;
                        color: #111827;
                    }
                """)
            
            self.costs_table.setCellWidget(i, 2, type_combo)
            
            # Définir une hauteur de ligne pour meilleure lisibilité
            self.costs_table.setRowHeight(i, 40)
        
        # Adapter la hauteur de la table
        row_height = 40
        header_height = self.costs_table.horizontalHeader().height()
        table_height = header_height + len(graph_data['vertices']) * row_height
        self.costs_table.setMinimumHeight(min(250, table_height))
    
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
                    cost_text = cost_item.text().replace(',', '.')
                    cost = float(cost_text)
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
        
        # Ajuster la hauteur du groupe
        if checked:
            self.advanced_group.setMinimumHeight(100)
        else:
            self.advanced_group.setMinimumHeight(0)
    
    def clear(self):
        """Réinitialise le panneau"""
        self.costs_table.setRowCount(0)
        self.budget_spin.setValue(0)
        self.min_cover_check.setChecked(False)
        self.redundancy_spin.setValue(1)
        self.advanced_check.setChecked(False)
        self.advanced_group.setVisible(False)
    
        def set_parameters(self, parameters):
            """Définit les paramètres depuis un dictionnaire"""
            # Budget
            budget = parameters.get('budget')
            if budget:
                self.budget_spin.setValue(int(budget))
            else:
                self.budget_spin.setValue(0)
            
            # Options avancées
            advanced = parameters.get('advanced', {})
            if advanced.get('min_cover', False):
                self.advanced_check.setChecked(True)
                self.min_cover_check.setChecked(True)
                self.redundancy_spin.setValue(advanced.get('redundancy', 1))
            else:
                self.advanced_check.setChecked(False)
                self.min_cover_check.setChecked(False)
                self.redundancy_spin.setValue(1)
            
            # Mettre à jour les types des sommets dans la table
            vertex_params = parameters.get('vertices', {})
            for i in range(self.costs_table.rowCount()):
                vertex_id = self.costs_table.item(i, 0).text()
                if vertex_id in vertex_params:
                    # Type
                    type_combo = self.costs_table.cellWidget(i, 2)
                    vertex_type = vertex_params[vertex_id].get('type', 'normal')
                    
                    if vertex_type == 'mandatory':
                        type_combo.setCurrentText("Obligatoire")
                        type_combo.setStyleSheet("""
                            QComboBox {
                                background-color: #fee2e2;
                                color: #dc2626;
                                font-weight: 500;
                            }
                        """)
                    elif vertex_type == 'forbidden':
                        type_combo.setCurrentText("Interdit")
                        type_combo.setStyleSheet("""
                            QComboBox {
                                background-color: #f3f4f6;
                                color: #6b7280;
                                font-weight: 500;
                            }
                        """)
                    else:
                        type_combo.setCurrentText("Normal")
                        type_combo.setStyleSheet("""
                            QComboBox {
                                background-color: white;
                                color: #111827;
                            }
                        """)
                    
                    # Coût
                    cost = vertex_params[vertex_id].get('cost', 1.0)
                    cost_item = QTableWidgetItem(f"{cost:.2f}")
                    cost_item.setTextAlignment(Qt.AlignCenter)
                    cost_item.setFont(QFont("Segoe UI", 11))
                    self.costs_table.setItem(i, 1, cost_item)