import json
import os
from datetime import datetime

def save_graph_to_file(graph_data, parameters, solution=None, filename=None):
    """
    Sauvegarde le graphe, les paramètres et éventuellement la solution dans un fichier JSON.
    
    Returns:
    --------
    dict : Données sauvegardées
    """
    save_data = {
        'metadata': {
            'app_name': 'Surveillance Network Optimizer',
            'save_date': datetime.now().isoformat(),
            'problem_type': 'vertex_cover',
            'version': '1.0'
        },
        'graph_data': graph_data,
        'parameters': parameters
    }
    
    if solution:
        save_data['solution'] = solution
    
    if filename:
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Erreur de sauvegarde: {e}")
            return False
    
    return save_data

def load_graph_from_file(filename):
    """
    Charge un graphe depuis un fichier JSON.
    
    Returns:
    --------
    tuple : (graph_data, parameters, solution, metadata) ou None en cas d'erreur
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return (
            data.get('graph_data', {}),
            data.get('parameters', {}),
            data.get('solution', None),
            data.get('metadata', {})
        )
    except Exception as e:
        print(f"Erreur de chargement: {e}")
        return None

def export_solution_to_csv(solution, filename):
    """Exporte la solution en CSV"""
    try:
        import csv
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # En-tête
            writer.writerow(['Sommet', 'Coût (€)', 'Statut'])
            writer.writerow([])
            
            # Données des sommets
            selected = solution.get('selected_vertices', [])
            detailed_costs = solution.get('detailed_costs', {})
            
            for vertex_id in selected:
                cost = detailed_costs.get(vertex_id, 'N/A')
                writer.writerow([vertex_id, cost, 'Sélectionné'])
            
            # Résumé
            writer.writerow([])
            writer.writerow(['RÉSUMÉ'])
            writer.writerow(['Coût total', f"{solution.get('total_cost', 0):.2f} €"])
            writer.writerow(['Nombre de sommets', len(selected)])
            writer.writerow(['Temps de résolution', f"{solution.get('solve_time', 0):.3f} s"])
            writer.writerow(['Statut', solution.get('status', 'N/A')])
        
        return True
    except Exception as e:
        print(f"Erreur d'export CSV: {e}")
        return False