def get_stylesheet():
    """Retourne la feuille de style CSS moderne"""
    # NOTE: Qt's style engine (QSS) doesn't support CSS variables (:root/var()),
    # transitions, transforms, or some advanced selectors. Use explicit
    # values and simple selectors to avoid parse warnings.
    return """
    /* Basic, QSS-compatible stylesheet */
    QMainWindow { background-color: #f3f4f6; }

    QWidget {
        font-family: 'Segoe UI', 'Roboto', sans-serif;
        font-size: 14px;
        color: #111827;
    }

    QGroupBox {
        font-weight: 600;
        font-size: 15px;
        border: 2px solid #d1d5db;
        border-radius: 8px;
        margin-top: 12px;
        padding-top: 15px;
        background-color: #ffffff;
    }

    QGroupBox::title { subcontrol-origin: margin; left: 12px; color: #2563eb; }

    QTableWidget {
        background-color: #ffffff;
        alternate-background-color: #f3f4f6;
        gridline-color: #d1d5db;
        border: 1px solid #d1d5db;
        border-radius: 6px;
        selection-background-color: #60a5fa;
        selection-color: white;
    }

    QHeaderView::section {
        background-color: #e5e7eb;
        padding: 10px;
        border-right: 1px solid #d1d5db;
        border-bottom: 1px solid #d1d5db;
        font-weight: 600;
        color: #111827;
    }

    QPushButton {
        background-color: #2563eb;
        color: white;
        border: none;
        padding: 8px 14px;
        border-radius: 6px;
        font-weight: 600;
        min-height: 34px;
    }

    QPushButton:hover { background-color: #1d4ed8; }
    QPushButton:pressed { background-color: #1d4ed8; }
    QPushButton:disabled { background-color: #d1d5db; color: #6b7280; }

    QPushButton#solve-button { background-color: #10b981; font-size: 16px; padding: 10px 20px; }
    QPushButton#solve-button:hover { background-color: #0da271; }

    QTextEdit, QLineEdit, QSpinBox, QComboBox {
        background-color: #ffffff;
        border: 2px solid #d1d5db;
        border-radius: 6px;
        padding: 6px;
        font-size: 14px;
        selection-background-color: #2563eb;
        selection-color: white;
    }

    QLabel { color: #111827; }
    QLabel#title { font-size: 18px; font-weight: 700; color: #1f2937; }
    QLabel#subtitle { font-size: 16px; font-weight: 600; color: #6b7280; }

    QRadioButton { spacing: 8px; padding: 4px 0; font-weight: 500; }

    QToolBar { background-color: #ffffff; border-bottom: 2px solid #d1d5db; padding: 6px; }
    QStatusBar { background-color: #ffffff; border-top: 1px solid #d1d5db; color: #6b7280; }

    QTabWidget::pane { border: 1px solid #d1d5db; border-radius: 6px; background-color: #ffffff; }

    QScrollBar:vertical { background-color: #f3f4f6; width: 12px; border-radius: 6px; }
    QScrollBar::handle:vertical { background-color: #d1d5db; border-radius: 6px; min-height: 30px; }

    QProgressBar { border: 1px solid #d1d5db; border-radius: 4px; background-color: #ffffff; }
    QProgressBar::chunk { background-color: #2563eb; border-radius: 4px; }

    QToolTip { background-color: #1f2937; color: white; border: 1px solid #d1d5db; border-radius: 4px; padding: 6px; font-size: 12px; }
    """