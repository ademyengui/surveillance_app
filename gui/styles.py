def get_stylesheet():
    """Retourne la feuille de style CSS moderne"""
    return """
    /* ===== VARIABLES DE COULEUR ===== */
    :root {
        --primary-color: #2563eb;
        --primary-dark: #1d4ed8;
        --primary-light: #60a5fa;
        --secondary-color: #7c3aed;
        --success-color: #10b981;
        --danger-color: #ef4444;
        --warning-color: #f59e0b;
        --info-color: #3b82f6;
        --dark-color: #1f2937;
        --light-color: #f9fafb;
        --border-color: #d1d5db;
        --text-primary: #111827;
        --text-secondary: #6b7280;
        --background-primary: #ffffff;
        --background-secondary: #f3f4f6;
        --background-tertiary: #e5e7eb;
    }
    
    /* ===== FENÊTRE PRINCIPALE ===== */
    QMainWindow {
        background-color: var(--background-secondary);
    }
    
    QWidget {
        font-family: 'Segoe UI', 'Inter', 'Roboto', sans-serif;
        font-size: 14px;
        color: var(--text-primary);
    }
    
    /* ===== GROUPES ===== */
    QGroupBox {
        font-weight: 600;
        font-size: 15px;
        border: 2px solid var(--border-color);
        border-radius: 8px;
        margin-top: 12px;
        padding-top: 15px;
        padding-bottom: 10px;
        background-color: var(--background-primary);
    }
    
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 12px;
        padding: 0 8px 0 8px;
        color: var(--primary-color);
    }
    
    /* ===== TABLES ===== */
    QTableWidget {
        background-color: var(--background-primary);
        alternate-background-color: var(--background-secondary);
        gridline-color: var(--border-color);
        border: 1px solid var(--border-color);
        border-radius: 6px;
        selection-background-color: var(--primary-light);
        selection-color: white;
    }
    
    QTableWidget::item {
        padding: 8px;
        border-bottom: 1px solid var(--background-secondary);
    }
    
    QTableWidget::item:selected {
        background-color: var(--primary-color);
        color: white;
        border-radius: 4px;
    }
    
    QHeaderView::section {
        background-color: var(--background-tertiary);
        padding: 10px;
        border: none;
        border-right: 1px solid var(--border-color);
        border-bottom: 1px solid var(--border-color);
        font-weight: 600;
        color: var(--text-primary);
    }
    
    QHeaderView::section:last {
        border-right: none;
    }
    
    /* ===== BOUTONS ===== */
    QPushButton {
        background-color: var(--primary-color);
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 14px;
        min-height: 36px;
        transition: all 0.2s;
    }
    
    QPushButton:hover {
        background-color: var(--primary-dark);
        transform: translateY(-1px);
    }
    
    QPushButton:pressed {
        background-color: var(--primary-dark);
        transform: translateY(0);
    }
    
    QPushButton:disabled {
        background-color: var(--border-color);
        color: var(--text-secondary);
    }
    
    /* Bouton principal (Résoudre) */
    QPushButton#solve-button {
        background-color: var(--success-color);
        font-size: 16px;
        padding: 12px 24px;
    }
    
    QPushButton#solve-button:hover {
        background-color: #0da271;
    }
    
    /* Boutons secondaires */
    QPushButton.secondary {
        background-color: var(--secondary-color);
    }
    
    /* Boutons d'export */
    QPushButton.export-button {
        background-color: var(--info-color);
        padding: 8px 16px;
        font-size: 13px;
    }
    
    /* ===== ZONES DE TEXTE ===== */
    QTextEdit, QLineEdit, QSpinBox, QComboBox {
        background-color: var(--background-primary);
        border: 2px solid var(--border-color);
        border-radius: 6px;
        padding: 8px;
        font-size: 14px;
        selection-background-color: var(--primary-color);
        selection-color: white;
    }
    
    QTextEdit:focus, QLineEdit:focus, QSpinBox:focus, QComboBox:focus {
        border-color: var(--primary-color);
        outline: none;
    }
    
    QTextEdit {
        padding: 10px;
    }
    
    /* ===== LABELS ===== */
    QLabel {
        color: var(--text-primary);
    }
    
    QLabel.title {
        font-size: 18px;
        font-weight: 700;
        color: var(--dark-color);
        padding: 5px 0;
    }
    
    QLabel.subtitle {
        font-size: 16px;
        font-weight: 600;
        color: var(--text-secondary);
    }
    
    QLabel.value {
        font-size: 20px;
        font-weight: 700;
        color: var(--success-color);
    }
    
    /* ===== RADIO BOUTONS ===== */
    QRadioButton {
        spacing: 10px;
        padding: 6px 0;
        font-weight: 500;
    }
    
    QRadioButton::indicator {
        width: 20px;
        height: 20px;
        border: 2px solid var(--border-color);
        border-radius: 10px;
    }
    
    QRadioButton::indicator:checked {
        background-color: var(--primary-color);
        border: 6px solid var(--primary-light);
    }
    
    QRadioButton::indicator:hover {
        border-color: var(--primary-color);
    }
    
    /* ===== CHECKBOX ===== */
    QCheckBox {
        spacing: 10px;
        padding: 6px 0;
    }
    
    QCheckBox::indicator {
        width: 20px;
        height: 20px;
        border: 2px solid var(--border-color);
        border-radius: 4px;
    }
    
    QCheckBox::indicator:checked {
        background-color: var(--success-color);
        border-color: var(--success-color);
        image: url(check.svg);
    }
    
    QCheckBox::indicator:hover {
        border-color: var(--primary-color);
    }
    
    /* ===== BARRE D'OUTILS ===== */
    QToolBar {
        background-color: var(--background-primary);
        border-bottom: 2px solid var(--border-color);
        padding: 8px;
        spacing: 10px;
    }
    
    QToolBar QToolButton {
        padding: 8px 12px;
        border-radius: 4px;
    }
    
    QToolBar QToolButton:hover {
        background-color: var(--background-secondary);
    }
    
    /* ===== BARRE DE STATUT ===== */
    QStatusBar {
        background-color: var(--background-primary);
        border-top: 1px solid var(--border-color);
        color: var(--text-secondary);
    }
    
    /* ===== SPLITTER ===== */
    QSplitter::handle {
        background-color: var(--border-color);
        width: 3px;
        height: 3px;
    }
    
    QSplitter::handle:hover {
        background-color: var(--primary-color);
    }
    
    /* ===== ONGLETS ===== */
    QTabWidget::pane {
        border: 1px solid var(--border-color);
        border-radius: 6px;
        background-color: var(--background-primary);
    }
    
    QTabBar::tab {
        background-color: var(--background-secondary);
        padding: 10px 20px;
        margin-right: 2px;
        border-top-left-radius: 6px;
        border-top-right-radius: 6px;
    }
    
    QTabBar::tab:selected {
        background-color: var(--background-primary);
        font-weight: 600;
        border-bottom: 3px solid var(--primary-color);
    }
    
    /* ===== BARRE DE DÉFILEMENT ===== */
    QScrollBar:vertical {
        background-color: var(--background-secondary);
        width: 12px;
        border-radius: 6px;
    }
    
    QScrollBar::handle:vertical {
        background-color: var(--border-color);
        border-radius: 6px;
        min-height: 30px;
    }
    
    QScrollBar::handle:vertical:hover {
        background-color: var(--text-secondary);
    }
    
    QScrollBar::add-line, QScrollBar::sub-line {
        height: 0px;
    }
    
    /* ===== PROGRESS BAR ===== */
    QProgressBar {
        border: 1px solid var(--border-color);
        border-radius: 4px;
        background-color: var(--background-primary);
        text-align: center;
    }
    
    QProgressBar::chunk {
        background-color: var(--primary-color);
        border-radius: 4px;
    }
    
    /* ===== TOOLTIP ===== */
    QToolTip {
        background-color: var(--dark-color);
        color: white;
        border: 1px solid var(--border-color);
        border-radius: 4px;
        padding: 8px;
        font-size: 12px;
    }
    """