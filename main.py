import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from gui.main_window import MainWindow

def main():
    # Créer l'application
    app = QApplication(sys.argv)
    app.setApplicationName("Surveillance Network Optimizer")
    app.setStyle('Fusion')  # Style moderne
    
    # Créer et afficher la fenêtre principale
    window = MainWindow()
    window.show()
    
    # Exécuter l'application
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()