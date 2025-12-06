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
    progress = pyqtSignal(int, str)  # Progression et message
    
    def __init__(self, graph_data, parameters):
        super().__init__()
        self.graph_data = graph_data
        self.parameters = parameters
    
    def run(self):
        """Exécute le solveur dans le thread"""
        try:
            self.started.emit()
            self.progress.emit(10, "Initialisation...")
            time.sleep(0.1)
            
            # Essayer d'utiliser Gurobi
            try:
                from .vertex_cover_solver import VertexCoverSolver
                solver = VertexCoverSolver()
                
                self.progress.emit(30, "Modélisation avec Gurobi...")
                
                # Résoudre le problème
                solution = solver.solve(
                    self.graph_data['vertices'],
                    self.graph_data['edges'],
                    self.parameters
                )
                
                self.progress.emit(90, "Solution trouvée !")
                time.sleep(0.1)
                self.progress.emit(100, "Terminé")
                
                self.finished.emit(solution)
                
            except ImportError as e:
                # Gurobi non disponible, utiliser l'algorithme glouton
                self.progress.emit(30, "Gurobi non trouvé, utilisation de l'algorithme glouton...")
                
                from .greedy_solver import GreedyVertexCoverSolver
                solver = GreedyVertexCoverSolver()
                
                solution = solver.solve(
                    self.graph_data['vertices'],
                    self.graph_data['edges'],
                    self.parameters
                )
                
                # Ajouter un message indiquant que c'est une solution gloutonne
                if solution['status'] == 'optimal':
                    solution['message'] = "Solution gloutonne (approximative) - Gurobi non installé"
                
                self.progress.emit(90, "Solution gloutonne trouvée")
                time.sleep(0.1)
                self.progress.emit(100, "Terminé")
                
                self.finished.emit(solution)
                
            except Exception as e:
                self.error.emit(f"Erreur lors de la résolution: {str(e)}")
            
        except Exception as e:
            self.error.emit(f"Erreur dans le worker: {str(e)}")