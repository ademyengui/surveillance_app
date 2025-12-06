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
            'version': '2.0'
        },
        'graph_data': graph_data,
        'parameters': parameters
    }
    
    if solution:
        save_data['solution'] = solution
    
    if filename:
        try:
            # Assurer l'extension .json
            if not filename.endswith('.json'):
                filename += '.json'
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)
            
            return {'success': True, 'filename': filename, 'data': save_data}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    return save_data

def load_graph_from_file(filename):
    """
    Charge un graphe depuis un fichier JSON.
    
    Returns:
    --------
    dict : Résultat avec les données chargées ou l'erreur
    """
    try:
        # Vérifier que le fichier existe
        if not os.path.exists(filename):
            return {
                'success': False,
                'error': f"Le fichier '{filename}' n'existe pas."
            }
        
        # Vérifier l'extension
        if not filename.endswith('.json'):
            return {
                'success': False,
                'error': "Le fichier doit avoir l'extension .json"
            }
        
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Valider la structure du fichier
        required_keys = ['metadata', 'graph_data']
        for key in required_keys:
            if key not in data:
                return {
                    'success': False,
                    'error': f"Format invalide : clé '{key}' manquante."
                }
        
        return {
            'success': True,
            'graph_data': data.get('graph_data', {}),
            'parameters': data.get('parameters', {}),
            'solution': data.get('solution', None),
            'metadata': data.get('metadata', {}),
            'filename': filename
        }
        
    except json.JSONDecodeError as e:
        return {
            'success': False,
            'error': f"Erreur de décodage JSON : {str(e)}"
        }
    except Exception as e:
        return {
            'success': False,
            'error': f"Erreur de chargement : {str(e)}"
        }

def export_solution_to_json(solution, graph_data=None, parameters=None, filename=None):
    """
    Exporte la solution complète (graphe, paramètres, solution) en JSON.
    
    Returns:
    --------
    dict : Résultat de l'export
    """
    export_data = {
        'metadata': {
            'app_name': 'Surveillance Network Optimizer',
            'export_date': datetime.now().isoformat(),
            'export_type': 'solution',
            'version': '2.0'
        },
        'solution': solution
    }
    
    if graph_data:
        export_data['graph_data'] = graph_data
    if parameters:
        export_data['parameters'] = parameters
    
    if filename:
        try:
            # Assurer l'extension .json
            if not filename.endswith('.json'):
                filename += '.json'
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            return {'success': True, 'filename': filename}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    return export_data

def export_solution_to_csv(solution, filename):
    """Exporte la solution en CSV"""
    try:
        import csv
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # En-tête
            writer.writerow(['SURVEILLANCE NETWORK OPTIMIZER - RAPPORT DE SOLUTION'])
            writer.writerow(['Exporté le', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
            writer.writerow([])
            
            # Résumé
            writer.writerow(['RÉSUMÉ'])
            writer.writerow(['Statut', solution.get('status', 'N/A')])
            writer.writerow(['Coût total', f"{solution.get('total_cost', 0):.2f} €"])
            writer.writerow(['Nombre de sommets sélectionnés', len(solution.get('selected_vertices', []))])
            writer.writerow(['Temps de résolution', f"{solution.get('solve_time', 0):.3f} s"])
            writer.writerow(['Gap d\'optimalité', f"{solution.get('gap', 0)*100:.2f} %"])
            writer.writerow([])
            
            # Détails des sommets sélectionnés
            writer.writerow(['SOMMETS SÉLECTIONNÉS'])
            writer.writerow(['Sommet', 'Coût (€)', 'Statut'])
            
            selected = solution.get('selected_vertices', [])
            detailed_costs = solution.get('detailed_costs', {})
            
            for vertex_id in selected:
                cost = detailed_costs.get(vertex_id, 'N/A')
                writer.writerow([vertex_id, cost, 'Sélectionné'])
            
            writer.writerow([])
            
            # Couverture des arêtes
            writer.writerow(['COUVERTURE DES ARÊTES'])
            writer.writerow(['Arête', 'Sommets couvrants', 'Statut'])
            
            if 'cover_details' in solution and solution['cover_details']:
                for edge, covering in solution['cover_details'].items():
                    if covering:
                        writer.writerow([edge, ', '.join(covering), 'Couverte'])
                    else:
                        writer.writerow([edge, '', 'Non couverte'])
            else:
                writer.writerow(['Aucun détail de couverture disponible', '', ''])
        
        return {'success': True, 'filename': filename}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def validate_graph_data(graph_data):
    """
    Valide les données du graphe.
    
    Returns:
    --------
    tuple : (bool, str) - (valide, message d'erreur)
    """
    if not isinstance(graph_data, dict):
        return False, "Les données du graphe doivent être un dictionnaire."
    
    if 'vertices' not in graph_data or 'edges' not in graph_data:
        return False, "Les données doivent contenir 'vertices' et 'edges'."
    
    if not isinstance(graph_data['vertices'], list):
        return False, "'vertices' doit être une liste."
    
    if not isinstance(graph_data['edges'], list):
        return False, "'edges' doit être une liste."
    
    # Valider chaque sommet
    vertex_ids = set()
    for i, vertex in enumerate(graph_data['vertices']):
        if 'id' not in vertex:
            return False, f"Sommet {i} n'a pas d'identifiant 'id'."
        
        vertex_id = vertex['id']
        if vertex_id in vertex_ids:
            return False, f"ID de sommet dupliqué : {vertex_id}"
        vertex_ids.add(vertex_id)
    
    # Valider chaque arête
    for i, edge in enumerate(graph_data['edges']):
        if 'from' not in edge or 'to' not in edge:
            return False, f"Arête {i} doit avoir 'from' et 'to'."
        
        if edge['from'] not in vertex_ids:
            return False, f"Arête {i} : sommet 'from' ({edge['from']}) n'existe pas."
        
        if edge['to'] not in vertex_ids:
            return False, f"Arête {i} : sommet 'to' ({edge['to']}) n'existe pas."
    
    return True, "Données valides."