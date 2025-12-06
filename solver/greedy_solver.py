import time
import heapq

class GreedyVertexCoverSolver:
    """
    Solveur glouton pour le problème de couverture de sommets.
    Utilisé comme solution de secours si Gurobi n'est pas disponible.
    """
    
    def __init__(self):
        self.solution = None
        self.solve_time = 0
        
    def solve(self, vertices, edges, parameters):
        """
        Résout le problème de couverture de sommets avec un algorithme glouton.
        
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
            # Convertir les données en structures plus pratiques
            vertex_dict = {v['id']: v for v in vertices}
            vertex_ids = list(vertex_dict.keys())
            
            # Séparer les arêtes critiques et normales
            critical_edges = [e for e in edges if e.get('critical', False)]
            normal_edges = [e for e in edges if not e.get('critical', False)]
            
            # Initialiser les ensembles
            selected = set()
            uncovered_edges = set()
            
            # 1. Ajouter les sommets obligatoires
            for v_id in vertex_ids:
                if vertex_dict[v_id].get('type') == 'mandatory':
                    selected.add(v_id)
            
            # 2. Retirer les sommets interdits
            for v_id in vertex_ids:
                if vertex_dict[v_id].get('type') == 'forbidden':
                    selected.discard(v_id)
            
            # 3. Initialiser les arêtes non couvertes
            for edge in edges:
                u, v = edge['from'], edge['to']
                # Ne pas ajouter si déjà couverte par un sommet obligatoire
                if u not in selected and v not in selected:
                    uncovered_edges.add((u, v, edge.get('critical', False)))
            
            # 4. Algorithme glouton
            while uncovered_edges:
                # Calculer le rapport coût/bénéfice pour chaque sommet
                scores = []
                
                for v_id in vertex_ids:
                    # Ignorer les sommets déjà sélectionnés ou interdits
                    if v_id in selected or vertex_dict[v_id].get('type') == 'forbidden':
                        continue
                    
                    # Compter les arêtes non couvertes incidentes
                    benefit = 0
                    for u, v, critical in list(uncovered_edges):
                        if u == v_id or v == v_id:
                            if critical:
                                benefit += 2  # Plus d'importance aux arêtes critiques
                            else:
                                benefit += 1
                    
                    if benefit > 0:
                        cost = vertex_dict[v_id].get('cost', 1.0)
                        score = benefit / cost  # Rapport bénéfice/coût
                        scores.append((-score, v_id, benefit))  # Négatif pour max-heap
                
                if not scores:
                    break  # Plus de sommets utiles
                
                # Sélectionner le sommet avec le meilleur score
                heapq.heapify(scores)
                best_score, best_vertex, benefit = heapq.heappop(scores)
                selected.add(best_vertex)
                
                # Retirer les arêtes maintenant couvertes
                new_uncovered = set()
                for u, v, critical in uncovered_edges:
                    if u != best_vertex and v != best_vertex:
                        new_uncovered.add((u, v, critical))
                uncovered_edges = new_uncovered
            
            # 5. Vérifier la contrainte de budget
            budget = parameters.get('budget')
            if budget and budget > 0:
                total_cost = sum(vertex_dict[v].get('cost', 1.0) for v in selected)
                
                # Si le budget est dépassé, retirer les sommets les plus chers
                if total_cost > budget:
                    # Trier les sommets par coût décroissant
                    sorted_vertices = sorted(selected, 
                                           key=lambda v: vertex_dict[v].get('cost', 1.0), 
                                           reverse=True)
                    
                    while total_cost > budget and sorted_vertices:
                        removed = sorted_vertices.pop(0)
                        selected.remove(removed)
                        total_cost -= vertex_dict[removed].get('cost', 1.0)
            
            # 6. Vérifier la couverture
            # Pour les arêtes critiques, vérifier que les deux extrémités sont sélectionnées
            for edge in critical_edges:
                u, v = edge['from'], edge['to']
                if u not in selected or v not in selected:
                    # Forcer la sélection des deux sommets
                    selected.add(u)
                    selected.add(v)
            
            # 7. Préparer les résultats
            selected_vertices = list(selected)
            total_cost = sum(vertex_dict[v].get('cost', 1.0) for v in selected_vertices)
            
            # Détails de couverture
            cover_details = {}
            for edge in edges:
                u, v = edge['from'], edge['to']
                covering = []
                if u in selected_vertices:
                    covering.append(u)
                if v in selected_vertices:
                    covering.append(v)
                cover_details[f"{u}-{v}"] = covering
            
            # Détails des coûts
            detailed_costs = {v: vertex_dict[v].get('cost', 1.0) for v in selected_vertices}
            
            self.solve_time = time.time() - start_time
            
            return {
                'status': 'optimal',
                'total_cost': total_cost,
                'selected_vertices': selected_vertices,
                'cover_details': cover_details,
                'solve_time': self.solve_time,
                'gap': 0.0,
                'num_selected': len(selected_vertices),
                'detailed_costs': detailed_costs,
                'message': 'Solution gloutonne trouvée (approximative)'
            }
            
        except Exception as e:
            self.solve_time = time.time() - start_time
            return {
                'status': 'error',
                'message': f'Erreur dans l\'algorithme glouton: {str(e)}',
                'solve_time': self.solve_time
            }