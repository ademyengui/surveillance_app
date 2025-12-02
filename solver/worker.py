from PyQt5.QtCore import QThread, pyqtSignal
import time

class SolverWorker(QThread):
    """
    Worker pour exécuter le solveur dans un thread séparé.
    Émet des signaux pour mettre à jour l'interface.
    """
    
    # Signaux
    started = pyqtSignal()
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, graph_data, parameters):
        super().__init__()
        self.graph_data = graph_data
        self.parameters = parameters
    
    def run(self):
        """Exécute le solveur dans le thread"""
        try:
            self.started.emit()
            
            # Simuler un temps de calcul (pour montrer que c'est asynchrone)
            time.sleep(0.5)
            
            # Importer dynamiquement pour éviter les problèmes si Gurobi n'est pas installé
            try:
                from .vertex_cover_solver import VertexCoverSolver
                solver = VertexCoverSolver()
                
                # Résoudre le problème
                solution = solver.solve(
                    self.graph_data['vertices'],
                    self.graph_data['edges'],
                    self.parameters
                )
                
                self.finished.emit(solution)
                
            except ImportError as e:
                self.error.emit(f"Erreur d'importation du solveur: {e}")
            except Exception as e:
                self.error.emit(f"Erreur lors de la résolution: {e}")
            
        except Exception as e:
            self.error.emit(f"Erreur dans le worker: {str(e)}")