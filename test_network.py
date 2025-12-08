"""
Script de test pour valider le module d'optimisation
sans interface graphique
"""

import sys
from network_optimizer import NetworkOptimizer
import time
import json

def test_simple_network():
    """Test 1: Réseau simple avec 5 nœuds"""
    print("="*70)
    print("TEST 1: Réseau simple (5 nœuds)")
    print("="*70)
    
    num_nodes = 5
    edges = [
        # (source, dest, capacity, cost, latency)
        (0, 1, 100, 1.5, 10),
        (0, 2, 80, 2.0, 15),
        (1, 2, 60, 1.0, 8),
        (1, 3, 100, 1.8, 12),
        (2, 3, 70, 1.2, 10),
        (2, 4, 90, 2.5, 20),
        (3, 4, 120, 1.0, 8)
    ]
    demand = 100
    
    print(f"Configuration:")
    print(f"  - Nœuds: {num_nodes}")
    print(f"  - Arêtes: {len(edges)}")
    print(f"  - Demande: {demand} unités")
    print()
    
    # Test avec mode minimisation coût
    print("Mode: Minimisation du coût")
    optimizer = NetworkOptimizer(num_nodes, edges, demand, 
                                objective_type=0, 
                                use_reliability=False, 
                                use_balance=False)
    results = optimizer.solve()
    
    print_results(results)
    
    # Test avec contraintes de fiabilité
    print("\nMode: Minimisation du coût + Fiabilité")
    optimizer2 = NetworkOptimizer(num_nodes, edges, demand, 
                                  objective_type=0, 
                                  use_reliability=True, 
                                  use_balance=False)
    results2 = optimizer2.solve()
    
    print_results(results2)
    
    # Comparer les deux résultats
    print("\n" + "="*70)
    print("COMPARAISON")
    print("="*70)
    print(f"Sans fiabilité:")
    print(f"  Coût: {results['total_cost']:.2f} €")
    print(f"  Liens actifs: {results['active_links']}")
    print()
    print(f"Avec fiabilité:")
    print(f"  Coût: {results2['total_cost']:.2f} €")
    print(f"  Liens actifs: {results2['active_links']}")
    print(f"  Impact: +{((results2['total_cost']/results['total_cost'])-1)*100:.1f}% coût")
    print()

def test_medium_network():
    """Test 2: Réseau moyen avec 8 nœuds"""
    print("="*70)
    print("TEST 2: Réseau moyen (8 nœuds)")
    print("="*70)
    
    num_nodes = 8
    edges = [
        (0, 1, 150, 1.2, 10),
        (0, 2, 120, 1.8, 12),
        (1, 2, 100, 1.0, 8),
        (1, 3, 140, 1.5, 11),
        (2, 3, 110, 1.3, 9),
        (2, 4, 130, 2.0, 15),
        (3, 4, 120, 1.1, 8),
        (3, 5, 150, 1.7, 13),
        (4, 5, 140, 1.4, 10),
        (4, 6, 130, 2.2, 18),
        (5, 6, 150, 1.2, 9),
        (5, 7, 160, 1.6, 12),
        (6, 7, 170, 1.0, 7)
    ]
    demand = 300
    
    print(f"Configuration:")
    print(f"  - Nœuds: {num_nodes}")
    print(f"  - Arêtes: {len(edges)}")
    print(f"  - Demande: {demand} unités")
    print()
    
    # Test multi-critère avec équilibrage
    print("Mode: Multi-critère + Fiabilité + Équilibrage")
    optimizer = NetworkOptimizer(num_nodes, edges, demand, 
                                objective_type=2, 
                                use_reliability=True, 
                                use_balance=True)
    results = optimizer.solve()
    
    print_results(results)

def test_all_objectives():
    """Test 3: Comparer les 3 modes d'optimisation"""
    print("="*70)
    print("TEST 3: Comparaison des objectifs d'optimisation")
    print("="*70)
    
    num_nodes = 6
    edges = [
        (0, 1, 120, 2.0, 20),
        (0, 2, 100, 1.5, 10),
        (1, 3, 110, 1.8, 15),
        (2, 3, 90, 1.2, 8),
        (2, 4, 130, 2.5, 25),
        (3, 4, 100, 1.0, 5),
        (3, 5, 120, 1.5, 12),
        (4, 5, 140, 1.3, 10)
    ]
    demand = 150
    
    print(f"Configuration commune:")
    print(f"  - Nœuds: {num_nodes}")
    print(f"  - Arêtes: {len(edges)}")
    print(f"  - Demande: {demand} unités")
    print()
    
    results_list = []
    objectives = [
        ("Minimisation du coût", 0),
        ("Minimisation de la latence", 1),
        ("Multi-critère", 2)
    ]
    
    for obj_name, obj_type in objectives:
        print(f"\n{'-'*70}")
        print(f"Objectif: {obj_name}")
        print(f"{'-'*70}")
        
        optimizer = NetworkOptimizer(num_nodes, edges, demand, 
                                    objective_type=obj_type, 
                                    use_reliability=False, 
                                    use_balance=False)
        results = optimizer.solve()
        results['objective'] = obj_name
        results_list.append(results)
        
        print(f"  Coût total: {results['total_cost']:.2f} €")
        print(f"  Latence moyenne: {results['avg_latency']:.2f} ms")
        print(f"  Liens actifs: {results['active_links']}")
        print(f"  Temps: {results['solve_time']:.3f} s")
    
    # Tableau comparatif
    print("\n" + "="*70)
    print("TABLEAU COMPARATIF")
    print("="*70)
    print(f"{'Objectif':<25} {'Coût (€)':<12} {'Latence (ms)':<15} {'Liens':<8}")
    print("-"*70)
    for res in results_list:
        print(f"{res['objective']:<25} {res['total_cost']:<12.2f} "
              f"{res['avg_latency']:<15.2f} {res['active_links']:<8}")
    print()

def test_scalability():
    """Test 4: Test de scalabilité"""
    print("="*70)
    print("TEST 4: Test de scalabilité")
    print("="*70)
    
    import numpy as np
    
    sizes = [5, 8, 10, 12]
    results = []
    
    print(f"{'Nœuds':<8} {'Arêtes':<8} {'Variables':<12} {'Temps (s)':<12} {'Statut':<10}")
    print("-"*70)
    
    for n in sizes:
        # Générer un réseau aléatoire
        edges = []
        
        # Connexions séquentielles
        for i in range(n-1):
            capacity = np.random.randint(100, 200)
            cost = round(np.random.uniform(1.0, 3.0), 2)
            latency = np.random.randint(8, 20)
            edges.append((i, i+1, capacity, cost, latency))
        
        # Connexions supplémentaires
        num_extra = n * 2
        for _ in range(num_extra):
            source = np.random.randint(0, n-2)
            dest = np.random.randint(source+1, n)
            if (source, dest) not in [(e[0], e[1]) for e in edges]:
                capacity = np.random.randint(80, 180)
                cost = round(np.random.uniform(1.0, 3.0), 2)
                latency = np.random.randint(8, 20)
                edges.append((source, dest, capacity, cost, latency))
        
        demand = 100
        
        optimizer = NetworkOptimizer(n, edges, demand, 
                                    objective_type=0, 
                                    use_reliability=False, 
                                    use_balance=False)
        
        res = optimizer.solve()
        stats = optimizer.get_model_statistics()
        
        print(f"{n:<8} {len(edges):<8} {stats['num_variables']:<12} "
              f"{res['solve_time']:<12.3f} {res['status']:<10}")
        
        results.append({
            'nodes': n,
            'edges': len(edges),
            'time': res['solve_time'],
            'status': res['status']
        })
    
    print()

def print_results(results):
    """Afficher les résultats de manière formatée"""
    if results['status'] != 'optimal':
        print(f"⚠️  Statut: {results['status']}")
        print(f"   Message: {results.get('message', 'Aucune solution trouvée')}")
        return
    
    print(f"✓ Statut: {results['status'].upper()}")
    print(f"  Temps de calcul: {results['solve_time']:.3f} secondes")
    print()
    print(f"Résultats:")
    print(f"  Coût total: {results['total_cost']:.2f} €")
    print(f"  Latence moyenne: {results['avg_latency']:.2f} ms")
    print(f"  Liens actifs: {results['active_links']}")
    print(f"  Utilisation moyenne: {results['avg_utilization']:.1%}")
    print()
    
    # Afficher les flux principaux
    if results.get('main_paths'):
        print("Chemins principaux:")
        for i, path in enumerate(results['main_paths'][:3], 1):
            print(f"  {i}. {path}")
    
    # Afficher les flux sur chaque lien
    print("\nFlux sur les liens:")
    active_flows = [(edge, flow) for edge, flow in results['flows'].items() 
                   if flow > 0.01]
    active_flows.sort(key=lambda x: x[1], reverse=True)
    
    for (source, dest), flow in active_flows[:5]:
        print(f"  {source} → {dest}: {flow:.2f} unités")
    
    if len(active_flows) > 5:
        print(f"  ... et {len(active_flows) - 5} autres liens")
    print()

def run_all_tests():
    """Exécuter tous les tests"""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*15 + "TESTS D'OPTIMISATION DE RÉSEAU" + " "*23 + "║")
    print("╚" + "="*68 + "╝")
    print()
    
    tests = [
        ("Test 1: Réseau simple", test_simple_network),
        ("Test 2: Réseau moyen", test_medium_network),
        ("Test 3: Comparaison objectifs", test_all_objectives),
        ("Test 4: Scalabilité", test_scalability)
    ]
    
    start_time = time.time()
    
    for test_name, test_func in tests:
        try:
            print()
            test_func()
            print()
            time.sleep(0.5)  # Pause entre les tests
        except Exception as e:
            print(f"❌ Erreur dans {test_name}: {str(e)}")
            import traceback
            traceback.print_exc()
    
    total_time = time.time() - start_time
    
    print("="*70)
    print(f"TOUS LES TESTS TERMINÉS EN {total_time:.2f} SECONDES")
    print("="*70)
    print()

if __name__ == "__main__":
    # Vérifier que Gurobi est disponible
    try:
        import gurobipy
        print("✓ Gurobi détecté")
    except ImportError:
        print("❌ Erreur: Gurobi n'est pas installé")
        print("   Installez-le avec: pip install gurobipy")
        print("   Et obtenez une licence sur: https://www.gurobi.com/academia/")
        sys.exit(1)
    
    # Lancer les tests
    run_all_tests()