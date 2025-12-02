def get_stylesheet():
    """Retourne la feuille de style CSS"""
    return """
    QMainWindow {
        background-color: #f0f0f0;
    }
    
    QWidget {
        font-family: 'Segoe UI', Arial, sans-serif;
    }
    
    QGroupBox {
        font-weight: bold;
        border: 2px solid #cccccc;
        border-radius: 5px;
        margin-top: 10px;
        padding-top: 10px;
    }
    
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 5px 0 5px;
    }
    
    QTableWidget {
        background-color: white;
        alternate-background-color: #f9f9f9;
        gridline-color: #e0e0e0;
        border: 1px solid #cccccc;
    }
    
    QTableWidget::item {
        padding: 5px;
    }
    
    QTableWidget::item:selected {
        background-color: #e3f2fd;
    }
    
    QHeaderView::section {
        background-color: #e0e0e0;
        padding: 5px;
        border: 1px solid #cccccc;
        font-weight: bold;
    }
    
    QPushButton {
        background-color: #2196F3;
        color: white;
        border: none;
        padding: 8px 15px;
        border-radius: 4px;
        font-weight: bold;
    }
    
    QPushButton:hover {
        background-color: #1976D2;
    }
    
    QPushButton:pressed {
        background-color: #0d47a1;
    }
    
    QTextEdit {
        background-color: white;
        border: 1px solid #cccccc;
        border-radius: 3px;
        padding: 5px;
    }
    
    QSpinBox, QComboBox {
        padding: 5px;
        border: 1px solid #cccccc;
        border-radius: 3px;
        background-color: white;
    }
    
    QLabel {
        color: #333333;
    }
    
    QRadioButton {
        spacing: 8px;
    }
    
    QRadioButton::indicator {
        width: 16px;
        height: 16px;
    }
    
    QRadioButton::indicator:checked {
        background-color: #2196F3;
        border: 4px solid #bbdefb;
        border-radius: 8px;
    }
    
    QCheckBox {
        spacing: 8px;
    }
    
    QCheckBox::indicator {
        width: 16px;
        height: 16px;
    }
    
    QCheckBox::indicator:checked {
        background-color: #4CAF50;
        border: 1px solid #388E3C;
    }
    """