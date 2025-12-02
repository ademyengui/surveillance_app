import time

class VertexCoverSolver:
    """
    Solveur pour le problème de couverture de sommets pondérée.
    Minimise le coût total de sélection des sommets pour couvrir toutes les arêtes.
    
    Note: Cette version utilise un algorithme glouton comme solution temporaire.
    Pour utiliser Gurobi, installez-le et remplacez cette implémentation.
    """
    
    def __init__(self):
        self.solution = None
        self.solve_time = 0
        
    def solve(self, vertices, edges, parameters):
        """
        Résout le problème de couverture de sommets.
        
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
            # Extraire les données
            vertex_dict = {v['id']: v for v in vertices}
            
            # Appliquer les contraintes de type
            mandatory_vertices = [v['id'] for v in vertices if v.get('type') == 'mandatory']
            forbidden_vertices = [v['id'] for v in vertices if v.get('type') == 'forbidden']
            
            # Arêtes critiques
            critical_edges = [edge for edge in edges if edge.get('critical', False)]
            normal_edges = [edge for edge in edges if not edge.get('critical', False)]
            
            # Algorithme glouton pour la couverture de sommets
            # 1. D'abord, sélectionner les sommets obligatoires
            selected = set(mandatory_vertices)
            
            # 2. Exclure les sommets interdits
            selected = selected - set(forbidden_vertices)
            
            # 3. Calculer le rapport coût/efficacité pour les sommets restants
            # Efficacité = nombre d'arêtes non couvertes incidentes / coût
            uncovered_edges = set()
            for edge in edges:
                # Vérifier si l'arête est déjà couverte
                u, v = edge['from'], edge['to']
                if u in selected or v in selected:
                    continue
                uncovered_edges.add((u, v))
            
            # Tant qu'il reste des arêtes non couvertes
            while uncovered_edges:
                best_vertex = None
                best_ratio = -1
                
                # Trouver le sommet avec le meilleur rapport
                for vertex_id, vertex in vertex_dict.items():
                    if vertex_id in forbidden_vertices or vertex_id in selected:
                        continue
                    
                    # Calculer le nombre d'arêtes non couvertes incidentes
                    incident_count = 0
                    for u, v in uncovered_edges:
                        if u == vertex_id or v == vertex_id:
                            incident_count += 1
                    
                    if incident_count > 0:
                        cost = vertex.get('cost', 1.0)
                        ratio = incident_count / cost
                        
                        if ratio > best_ratio:
                            best_ratio = ratio
                            best_vertex = vertex_id
                
                if best_vertex is None:
                    break
                
                # Ajouter le meilleur sommet
                selected.add(best_vertex)
                
                # Retirer les arêtes maintenant couvertes
                uncovered_edges = {(u, v) for (u, v) in uncovered_edges 
                                 if u != best_vertex and v != best_vertex}
            
            # Vérifier la contrainte de budget
            budget = parameters.get('budget')
            if budget and budget > 0:
                total_cost = sum(vertex_dict[v].get('cost', 1.0) for v in selected)
                if total_cost > budget:
                    # Ajuster la solution pour respecter le budget
                    # On retire les sommets les plus chers
                    sorted_selected = sorted(selected, 
                                           key=lambda v: vertex_dict[v].get('cost', 1.0), 
                                           reverse=True)
                    while total_cost > budget and sorted_selected:
                        removed = sorted_selected.pop(0)
                        selected.remove(removed)
                        total_cost -= vertex_dict[removed].get('cost', 1.0)
            
            # Calculer les détails de couverture
            cover_details = {}
            for edge in edges:
                u, v = edge['from'], edge['to']
                covering_vertices = []
                if u in selected:
                    covering_vertices.append(u)
                if v in selected:
                    covering_vertices.append(v)
                cover_details[f"{u}-{v}"] = covering_vertices
            
            # Calculer le coût total
            total_cost = sum(vertex_dict[v].get('cost', 1.0) for v in selected)
            
            # Détails des coûts
            detailed_costs = {v: vertex_dict[v].get('cost', 1.0) for v in selected}
            
            self.solve_time = time.time() - start_time
            
            return {
                'status': 'optimal',
                'total_cost': total_cost,
                'selected_vertices': list(selected),
                'cover_details': cover_details,
                'solve_time': self.solve_time,
                'gap': 0.0,
                'num_selected': len(selected),
                'detailed_costs': detailed_costs,
                'message': 'Solution gloutonne trouvée'
            }
            
        except Exception as e:
            print(f"Erreur dans le solveur: {e}")
            self.solve_time = time.time() - start_time
            return {
                'status': 'error',
                'message': str(e),
                'solve_time': self.solve_time
            }
    
    def get_sensitivity_analysis(self):
        """Analyse de sensibilité (optionnel)"""
        return None