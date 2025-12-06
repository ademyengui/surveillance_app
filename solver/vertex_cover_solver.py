import time
import sys

class VertexCoverSolver:
    """
    Solveur pour le problème de couverture de sommets pondérée avec Gurobi.
    Minimise le coût total de sélection des sommets pour couvrir toutes les arêtes.
    """
    
    def __init__(self):
        self.solution = None
        self.solve_time = 0
        self.model = None
        
    def solve(self, vertices, edges, parameters):
        """
        Résout le problème de couverture de sommets avec Gurobi.
        
        Parameters:
        -----------
        vertices : list[dict]
            Liste des sommets avec id, coût, type, etc.
        edges : list[dict]
            Liste des arêtes avec from, to, critical
        parameters : dict
            Paramètres additionnels (budget, options avancées)
            
        Returns:
        --------
        dict : Solution et métadonnées
        """
        start_time = time.time()
        
        try:
            # Essayer d'importer Gurobi
            try:
                import gurobipy as gp
                from gurobipy import GRB
            except ImportError as e:
                return {
                    'status': 'error',
                    'message': f"Gurobi non installé : {e}\n"
                              f"Installez avec: pip install gurobipy\n"
                              f"Ou utilisez une licence académique gratuite.",
                    'solve_time': time.time() - start_time
                }
            
            # Créer un dictionnaire pour accéder rapidement aux sommets
            vertex_dict = {v['id']: v for v in vertices}
            vertex_ids = list(vertex_dict.keys())
            
            # Créer le modèle Gurobi
            try:
                self.model = gp.Model("Vertex_Cover")
                self.model.setParam('OutputFlag', 0)  # Désactiver la sortie console
                self.model.setParam('TimeLimit', 30)   # Limite de temps de 30 secondes
            except gp.GurobiError as e:
                return {
                    'status': 'error',
                    'message': f"Erreur d'initialisation Gurobi : {e}\n"
                              f"Vérifiez votre licence Gurobi.",
                    'solve_time': time.time() - start_time
                }
            
            # Variables de décision : x[v] = 1 si le sommet v est sélectionné
            x = {}
            for v_id in vertex_ids:
                vertex = vertex_dict[v_id]
                v_type = vertex.get('type', 'normal')
                
                # Définir les bornes selon le type
                lb = 0
                ub = 1
                if v_type == 'mandatory':
                    lb = ub = 1  # Forcé à 1
                elif v_type == 'forbidden':
                    lb = ub = 0  # Forcé à 0
                
                x[v_id] = self.model.addVar(vtype=GRB.BINARY, 
                                          lb=lb, ub=ub, 
                                          name=f"x_{v_id}")
            
            # Fonction objectif : minimiser le coût total
            objective = gp.quicksum(vertex_dict[v_id].get('cost', 1.0) * x[v_id] 
                                  for v_id in vertex_ids)
            self.model.setObjective(objective, GRB.MINIMIZE)
            
            # Contraintes de couverture
            
            # 1. Arêtes normales : au moins une extrémité doit être sélectionnée
            for edge in edges:
                u = edge['from']
                v = edge['to']
                critical = edge.get('critical', False)
                
                if critical:
                    # Arête critique : les DEUX extrémités doivent être sélectionnées
                    self.model.addConstr(x[u] + x[v] >= 2, 
                                       name=f"critical_{u}_{v}")
                else:
                    # Arête normale : au moins une extrémité
                    self.model.addConstr(x[u] + x[v] >= 1, 
                                       name=f"cover_{u}_{v}")
            
            # 2. Contrainte de budget (si spécifiée)
            budget = parameters.get('budget')
            if budget and budget > 0:
                self.model.addConstr(
                    gp.quicksum(vertex_dict[v_id].get('cost', 1.0) * x[v_id] 
                              for v_id in vertex_ids) <= budget,
                    name="budget"
                )
            
            # 3. Options avancées : redondance
            advanced = parameters.get('advanced', {})
            if advanced.get('min_cover', False):
                redundancy = advanced.get('redundancy', 1)
                for edge in edges:
                    u = edge['from']
                    v = edge['to']
                    self.model.addConstr(x[u] + x[v] >= redundancy,
                                       name=f"redundancy_{u}_{v}")
            
            # Résoudre le modèle
            self.model.optimize()
            
            # Traiter les résultats
            solve_time = time.time() - start_time
            
            if self.model.status == GRB.OPTIMAL:
                # Solution optimale trouvée
                selected_vertices = []
                detailed_costs = {}
                
                for v_id in vertex_ids:
                    if x[v_id].X > 0.5:  # Variable binaire, seuil à 0.5
                        selected_vertices.append(v_id)
                        detailed_costs[v_id] = vertex_dict[v_id].get('cost', 1.0)
                
                # Calculer le détail de la couverture
                cover_details = {}
                for edge in edges:
                    u = edge['from']
                    v = edge['to']
                    covering = []
                    if u in selected_vertices:
                        covering.append(u)
                    if v in selected_vertices:
                        covering.append(v)
                    cover_details[f"{u}-{v}"] = covering
                
                return {
                    'status': 'optimal',
                    'total_cost': self.model.ObjVal,
                    'selected_vertices': selected_vertices,
                    'cover_details': cover_details,
                    'solve_time': solve_time,
                    'gap': self.model.MIPGap,
                    'num_selected': len(selected_vertices),
                    'detailed_costs': detailed_costs,
                    'message': f'Solution optimale trouvée par Gurobi (gap: {self.model.MIPGap*100:.2f}%)'
                }
            
            elif self.model.status == GRB.INFEASIBLE:
                return {
                    'status': 'infeasible',
                    'message': 'Le problème est insoluble avec les contraintes données.\n'
                              'Essayez de réduire le budget ou de changer les sommets obligatoires.',
                    'solve_time': solve_time
                }
            
            elif self.model.status == GRB.TIME_LIMIT:
                # Solution réalisable mais pas optimale (limite de temps atteinte)
                if hasattr(self.model, 'ObjVal'):
                    selected_vertices = []
                    detailed_costs = {}
                    
                    for v_id in vertex_ids:
                        if x[v_id].X > 0.5:
                            selected_vertices.append(v_id)
                            detailed_costs[v_id] = vertex_dict[v_id].get('cost', 1.0)
                    
                    return {
                        'status': 'suboptimal',
                        'total_cost': self.model.ObjVal,
                        'selected_vertices': selected_vertices,
                        'cover_details': {},
                        'solve_time': solve_time,
                        'gap': self.model.MIPGap,
                        'num_selected': len(selected_vertices),
                        'detailed_costs': detailed_costs,
                        'message': f'Solution réalisable trouvée (limite de temps atteinte). Gap: {self.model.MIPGap*100:.2f}%'
                    }
                else:
                    return {
                        'status': 'time_limit',
                        'message': 'Limite de temps atteinte sans solution réalisable.',
                        'solve_time': solve_time
                    }
            
            else:
                status_names = {
                    GRB.LOADED: 'MODÈLE CHARGÉ',
                    GRB.OPTIMAL: 'OPTIMAL',
                    GRB.INFEASIBLE: 'INFAISABLE',
                    GRB.INF_OR_UNBD: 'INFAISABLE OU NON BORNE',
                    GRB.UNBOUNDED: 'NON BORNÉ',
                    GRB.CUTOFF: 'COUPURE',
                    GRB.ITERATION_LIMIT: 'LIMITE D\'ITÉRATIONS',
                    GRB.NODE_LIMIT: 'LIMITE DE NŒUDS',
                    GRB.TIME_LIMIT: 'LIMITE DE TEMPS',
                    GRB.SOLUTION_LIMIT: 'LIMITE DE SOLUTIONS',
                    GRB.INTERRUPTED: 'INTERROMPU',
                    GRB.NUMERIC: 'ERREUR NUMÉRIQUE',
                    GRB.SUBOPTIMAL: 'SOUS-OPTIMAL',
                    GRB.INPROGRESS: 'EN COURS'
                }
                
                status_name = status_names.get(self.model.status, f'INCONNU ({self.model.status})')
                return {
                    'status': 'error',
                    'message': f'Statut Gurobi : {status_name}',
                    'solve_time': solve_time
                }
                
        except gp.GurobiError as e:
            solve_time = time.time() - start_time
            return {
                'status': 'error',
                'message': f'Erreur Gurobi : {str(e)}',
                'solve_time': solve_time
            }
        except Exception as e:
            solve_time = time.time() - start_time
            return {
                'status': 'error',
                'message': f'Erreur inattendue : {str(e)}',
                'solve_time': solve_time
            }
    
    def get_sensitivity_analysis(self):
        """Analyse de sensibilité avec Gurobi"""
        if not self.model or self.model.status != GRB.OPTIMAL:
            return None
        
        try:
            import gurobipy as gp
            from gurobipy import GRB
            
            sensitivity = {
                'variables': {},
                'constraints': {}
            }
            
            # Prix réduits pour les variables
            for var in self.model.getVars():
                sensitivity['variables'][var.VarName] = {
                    'value': var.X,
                    'reduced_cost': var.RC,
                    'lower_bound': var.LB,
                    'upper_bound': var.UB
                }
            
            # Valeurs duales pour les contraintes
            for constr in self.model.getConstrs():
                sensitivity['constraints'][constr.ConstrName] = {
                    'slack': constr.Slack,
                    'dual_value': constr.Pi,
                    'rhs': constr.RHS
                }
            
            return sensitivity
            
        except:
            return None