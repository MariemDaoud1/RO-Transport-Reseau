"""
Exemples de configurations de réseaux pour tester l'application
Chaque exemple représente un cas d'usage réel
"""

# Exemple 1: Réseau de campus universitaire
CAMPUS_NETWORK = {
    'name': 'Réseau Campus INSAT',
    'description': 'Connexion entre bâtiments du campus',
    'num_nodes': 6,
    'demand': 200,
    'edges': [
        # (source, dest, capacité, coût, latence)
        # 0=Entrée principale, 1=Bâtiment Admin, 2=Bibliothèque
        # 3=Département Informatique, 4=Labo Recherche, 5=Serveur Central
        (0, 1, 200, 1.0, 5),   # Entrée → Admin (fibre)
        (0, 2, 150, 1.5, 8),   # Entrée → Bibliothèque
        (1, 2, 100, 0.8, 3),   # Admin → Bibliothèque (courte distance)
        (1, 3, 180, 1.2, 6),   # Admin → Info
        (2, 3, 120, 1.0, 5),   # Bibliothèque → Info
        (2, 4, 140, 1.8, 10),  # Bibliothèque → Labo
        (3, 4, 160, 1.0, 4),   # Info → Labo (fibre)
        (3, 5, 200, 0.8, 3),   # Info → Serveur (haute priorité)
        (4, 5, 180, 1.0, 5),   # Labo → Serveur
    ],
    'node_names': [
        'Entrée Principale',
        'Bâtiment Admin',
        'Bibliothèque',
        'Dépt Informatique',
        'Laboratoire Recherche',
        'Serveur Central'
    ]
}

# Exemple 2: Réseau de distribution de contenu (CDN)
CDN_NETWORK = {
    'name': 'Réseau CDN Multi-Régions',
    'description': 'Distribution de contenu vidéo entre data centers',
    'num_nodes': 8,
    'demand': 500,
    'edges': [
        # 0=Origine (serveur source), 7=Client final
        # Régions: 1,2=Europe, 3,4=Asie, 5,6=Amérique
        (0, 1, 300, 2.0, 20),  # Origine → Paris
        (0, 2, 280, 2.5, 25),  # Origine → Londres
        (0, 3, 250, 3.5, 40),  # Origine → Tokyo
        (1, 2, 200, 0.5, 5),   # Paris ↔ Londres (courte latence)
        (2, 1, 200, 0.5, 5),
        (1, 4, 220, 2.0, 30),  # Paris → Singapour
        (2, 5, 240, 2.5, 35),  # Londres → New York
        (3, 4, 180, 1.0, 15),  # Tokyo → Singapour
        (4, 6, 200, 2.0, 30),  # Singapour → Los Angeles
        (5, 6, 250, 1.5, 20),  # New York → Los Angeles
        (5, 7, 300, 1.0, 10),  # New York → Client
        (6, 7, 280, 1.2, 12),  # Los Angeles → Client
    ],
    'node_names': [
        'Serveur Origine',
        'CDN Paris',
        'CDN Londres',
        'CDN Tokyo',
        'CDN Singapour',
        'CDN New York',
        'CDN Los Angeles',
        'Client Final'
    ]
}

# Exemple 3: Réseau d'entreprise avec backup
ENTERPRISE_NETWORK = {
    'name': 'Réseau Entreprise avec Redondance',
    'description': 'Réseau d\'entreprise avec chemins de backup',
    'num_nodes': 7,
    'demand': 150,
    'edges': [
        # 0=Siège social, 6=Site distant important
        # Chemins primaires (fibre, coût bas, capacité haute)
        (0, 1, 200, 0.8, 5),   # Siège → Router 1 (primaire)
        (1, 3, 180, 1.0, 6),   # Router 1 → Switch Core
        (3, 5, 200, 0.8, 5),   # Switch Core → Router 3
        (5, 6, 180, 1.0, 6),   # Router 3 → Site distant
        
        # Chemins de backup (sans fil, coût élevé, capacité réduite)
        (0, 2, 100, 3.0, 20),  # Siège → Router 2 (backup)
        (2, 4, 90, 3.5, 25),   # Router 2 → Switch Backup
        (4, 6, 100, 3.0, 20),  # Switch Backup → Site distant
        
        # Liens inter-switches (redondance)
        (1, 2, 120, 1.5, 10),  # Router 1 ↔ Router 2
        (3, 4, 150, 1.5, 8),   # Switch Core ↔ Switch Backup
        (5, 4, 100, 2.0, 15),  # Router 3 → Switch Backup
    ],
    'node_names': [
        'Siège Social',
        'Router Principal 1',
        'Router Backup 2',
        'Switch Core',
        'Switch Backup',
        'Router Principal 3',
        'Site Distant'
    ]
}

# Exemple 4: Réseau métropolitain (MAN)
METROPOLITAN_NETWORK = {
    'name': 'Réseau Métropolitain Tunis',
    'description': 'Infrastructure réseau entre quartiers de Tunis',
    'num_nodes': 10,
    'demand': 400,
    'edges': [
        # 0=Centre-ville (hub principal), 9=Banlieue (destination)
        (0, 1, 300, 1.0, 8),   # Centre → La Marsa
        (0, 2, 280, 1.2, 10),  # Centre → Carthage
        (0, 3, 250, 1.5, 12),  # Centre → Le Bardo
        (1, 2, 200, 0.8, 5),   # La Marsa → Carthage
        (1, 4, 220, 1.3, 10),  # La Marsa → La Goulette
        (2, 4, 180, 1.0, 7),   # Carthage → La Goulette
        (3, 5, 240, 1.2, 9),   # Le Bardo → Manouba
        (3, 6, 200, 1.5, 11),  # Le Bardo → Ariana
        (4, 7, 220, 1.1, 8),   # La Goulette → Ben Arous
        (5, 6, 180, 0.9, 6),   # Manouba → Ariana
        (5, 8, 200, 1.4, 10),  # Manouba → Zaghouan
        (6, 7, 190, 1.2, 9),   # Ariana → Ben Arous
        (7, 8, 210, 1.3, 10),  # Ben Arous → Zaghouan
        (7, 9, 250, 1.0, 7),   # Ben Arous → Banlieue
        (8, 9, 230, 1.2, 9),   # Zaghouan → Banlieue
    ],
    'node_names': [
        'Centre-Ville Tunis',
        'La Marsa',
        'Carthage',
        'Le Bardo',
        'La Goulette',
        'Manouba',
        'Ariana',
        'Ben Arous',
        'Zaghouan',
        'Zone Banlieue'
    ]
}

# Exemple 5: Réseau IoT Smart City
IOT_SMART_CITY = {
    'name': 'Infrastructure IoT Smart City',
    'description': 'Réseau de capteurs et actuateurs urbains',
    'num_nodes': 12,
    'demand': 300,
    'edges': [
        # 0=Gateway central, 11=Cloud
        # Clusters de capteurs
        (0, 1, 150, 0.5, 5),   # Gateway → Cluster Transport
        (0, 2, 140, 0.5, 5),   # Gateway → Cluster Environnement
        (0, 3, 130, 0.5, 5),   # Gateway → Cluster Énergie
        
        # Sous-réseaux Transport
        (1, 4, 120, 0.8, 8),   # Transport → Parking
        (1, 5, 110, 0.8, 8),   # Transport → Trafic
        (4, 5, 80, 0.3, 3),    # Parking ↔ Trafic
        
        # Sous-réseaux Environnement
        (2, 6, 100, 0.8, 8),   # Environnement → Qualité Air
        (2, 7, 110, 0.8, 8),   # Environnement → Météo
        (6, 7, 90, 0.3, 3),    # Qualité Air ↔ Météo
        
        # Sous-réseaux Énergie
        (3, 8, 130, 0.8, 8),   # Énergie → Éclairage
        (3, 9, 120, 0.8, 8),   # Énergie → Bâtiments
        (8, 9, 100, 0.3, 3),   # Éclairage ↔ Bâtiments
        
        # Agrégation vers Edge Computing
        (4, 10, 140, 1.0, 10), # Parking → Edge Server
        (5, 10, 130, 1.0, 10), # Trafic → Edge Server
        (6, 10, 120, 1.0, 10), # Qualité Air → Edge Server
        (7, 10, 110, 1.0, 10), # Météo → Edge Server
        (8, 10, 130, 1.0, 10), # Éclairage → Edge Server
        (9, 10, 120, 1.0, 10), # Bâtiments → Edge Server
        
        # Vers le Cloud
        (10, 11, 200, 2.0, 20), # Edge Server → Cloud
    ],
    'node_names': [
        'Gateway Central',
        'Cluster Transport',
        'Cluster Environnement',
        'Cluster Énergie',
        'Capteurs Parking',
        'Capteurs Trafic',
        'Capteurs Qualité Air',
        'Station Météo',
        'Contrôle Éclairage',
        'Smart Buildings',
        'Edge Computing Server',
        'Cloud Platform'
    ]
}

# Dictionnaire de tous les exemples
NETWORK_EXAMPLES = {
    'campus': CAMPUS_NETWORK,
    'cdn': CDN_NETWORK,
    'enterprise': ENTERPRISE_NETWORK,
    'metropolitan': METROPOLITAN_NETWORK,
    'iot': IOT_SMART_CITY
}

def get_example(name):
    """
    Récupérer un exemple par son nom
    
    Args:
        name: 'campus', 'cdn', 'enterprise', 'metropolitan', ou 'iot'
    
    Returns:
        dict: Configuration du réseau
    """
    return NETWORK_EXAMPLES.get(name.lower())

def list_examples():
    """Lister tous les exemples disponibles"""
    print("Exemples de réseaux disponibles:")
    print("=" * 70)
    for key, network in NETWORK_EXAMPLES.items():
        print(f"\n{key.upper()}: {network['name']}")
        print(f"  Description: {network['description']}")
        print(f"  Nœuds: {network['num_nodes']}")
        print(f"  Arêtes: {len(network['edges'])}")
        print(f"  Demande: {network['demand']} unités")

def save_example_to_file(name, filename):
    """
    Sauvegarder un exemple dans un fichier texte
    
    Args:
        name: Nom de l'exemple
        filename: Nom du fichier de sortie
    """
    network = get_example(name)
    if not network:
        print(f"Exemple '{name}' introuvable")
        return
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"# {network['name']}\n")
        f.write(f"# {network['description']}\n")
        f.write(f"# Nœuds: {network['num_nodes']}\n")
        f.write(f"# Demande: {network['demand']}\n\n")
        
        f.write("# Format: source destination capacité coût latence\n")
        for source, dest, cap, cost, lat in network['edges']:
            f.write(f"{source} {dest} {cap} {cost} {lat}\n")
    
    print(f"Exemple sauvegardé dans {filename}")

if __name__ == "__main__":
    # Afficher tous les exemples
    list_examples()
    
    print("\n" + "=" * 70)
    print("Pour utiliser un exemple dans votre application:")
    print("  from example_data import get_example")
    print("  network = get_example('campus')")
    print("  edges = network['edges']")
    print("=" * 70)