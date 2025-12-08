import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QTableWidget, 
                             QTableWidgetItem, QSpinBox, QGroupBox, QTextEdit,
                             QTabWidget, QMessageBox, QProgressBar, QDoubleSpinBox,
                             QComboBox, QCheckBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import networkx as nx
import numpy as np
from network_optimizer import NetworkOptimizer

class OptimizationThread(QThread):
    """Thread pour exécuter l'optimisation sans bloquer l'interface"""
    finished = pyqtSignal(object)
    error = pyqtSignal(str)
    
    def __init__(self, optimizer):
        super().__init__()
        self.optimizer = optimizer
        
    def run(self):
        try:
            results = self.optimizer.solve()
            self.finished.emit(results)
        except Exception as e:
            self.error.emit(str(e))

class NetworkCanvas(FigureCanvas):
    """Canvas pour visualiser le réseau"""
    def __init__(self, parent=None):
        self.fig = Figure(figsize=(10, 8))
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setParent(parent)
        
    def plot_network(self, num_nodes, edges_data, flow_solution=None):
        self.ax.clear()
        
        # Créer le graphe
        G = nx.DiGraph()
        G.add_nodes_from(range(num_nodes))
        
        # Ajouter les arêtes avec leurs propriétés
        edge_labels = {}
        for edge in edges_data:
            source, dest, capacity, cost, latency = edge
            G.add_edge(source, dest, capacity=capacity, cost=cost, latency=latency)
            
            if flow_solution and (source, dest) in flow_solution:
                flow = flow_solution[(source, dest)]
                if flow > 0.01:
                    edge_labels[(source, dest)] = f"Flow: {flow:.1f}\nCost: {cost}"
            else:
                edge_labels[(source, dest)] = f"Cap: {capacity}\nCost: {cost}"
        
        # Position des nœuds
        pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
        
        # Dessiner les nœuds
        node_colors = []
        for node in G.nodes():
            if node == 0:
                node_colors.append('lightgreen')  # Source
            elif node == num_nodes - 1:
                node_colors.append('lightcoral')  # Destination
            else:
                node_colors.append('lightblue')  # Intermédiaire
        
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
                               node_size=800, ax=self.ax)
        nx.draw_networkx_labels(G, pos, ax=self.ax, font_size=10, font_weight='bold')
        
        # Dessiner les arêtes
        if flow_solution:
            # Arêtes avec flux
            edges_with_flow = [(u, v) for (u, v) in G.edges() 
                              if (u, v) in flow_solution and flow_solution[(u, v)] > 0.01]
            edges_without_flow = [(u, v) for (u, v) in G.edges() 
                                 if (u, v) not in flow_solution or flow_solution[(u, v)] <= 0.01]
            
            nx.draw_networkx_edges(G, pos, edgelist=edges_with_flow, 
                                  edge_color='red', width=3, ax=self.ax,
                                  arrows=True, arrowsize=20, arrowstyle='->')
            nx.draw_networkx_edges(G, pos, edgelist=edges_without_flow, 
                                  edge_color='gray', width=1, ax=self.ax,
                                  arrows=True, arrowsize=15, arrowstyle='->',
                                  style='dashed')
        else:
            nx.draw_networkx_edges(G, pos, edge_color='gray', width=2, 
                                  ax=self.ax, arrows=True, arrowsize=20)
        
        # Ajouter les labels des arêtes
        nx.draw_networkx_edge_labels(G, pos, edge_labels, ax=self.ax, font_size=7)
        
        self.ax.set_title("Réseau de routage de données", fontsize=14, fontweight='bold')
        self.ax.axis('off')
        self.fig.tight_layout()
        self.draw()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.optimizer = None
        self.edges_data = []
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Optimisation du Routage de Données dans un Réseau")
        self.setGeometry(100, 100, 1400, 900)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Layout gauche (paramètres et contrôles)
        left_layout = QVBoxLayout()
        
        # Configuration du réseau
        config_group = QGroupBox("Configuration du Réseau")
        config_layout = QVBoxLayout()
        
        # Nombre de nœuds
        nodes_layout = QHBoxLayout()
        nodes_layout.addWidget(QLabel("Nombre de nœuds:"))
        self.nodes_spin = QSpinBox()
        self.nodes_spin.setRange(3, 20)
        self.nodes_spin.setValue(5)
        self.nodes_spin.valueChanged.connect(self.update_network_size)
        nodes_layout.addWidget(self.nodes_spin)
        config_layout.addLayout(nodes_layout)
        
        # Demande totale
        demand_layout = QHBoxLayout()
        demand_layout.addWidget(QLabel("Demande totale (unités):"))
        self.demand_spin = QDoubleSpinBox()
        self.demand_spin.setRange(1, 10000)
        self.demand_spin.setValue(100)
        self.demand_spin.setSingleStep(10)
        demand_layout.addWidget(self.demand_spin)
        config_layout.addLayout(demand_layout)
        
        # Objectif d'optimisation
        objective_layout = QHBoxLayout()
        objective_layout.addWidget(QLabel("Objectif:"))
        self.objective_combo = QComboBox()
        self.objective_combo.addItems(["Minimiser coût total", 
                                      "Minimiser latence moyenne",
                                      "Optimisation multi-critère"])
        objective_layout.addWidget(self.objective_combo)
        config_layout.addLayout(objective_layout)
        
        # Options avancées
        self.reliability_check = QCheckBox("Inclure contraintes de fiabilité")
        self.reliability_check.setChecked(True)
        config_layout.addWidget(self.reliability_check)
        
        self.balance_check = QCheckBox("Équilibrage de charge")
        config_layout.addWidget(self.balance_check)
        
        config_group.setLayout(config_layout)
        left_layout.addWidget(config_group)
        
        # Table des arêtes
        edges_group = QGroupBox("Arêtes du Réseau (Liens)")
        edges_layout = QVBoxLayout()
        
        self.edges_table = QTableWidget()
        self.edges_table.setColumnCount(5)
        self.edges_table.setHorizontalHeaderLabels(["Source", "Destination", 
                                                    "Capacité", "Coût/unité", 
                                                    "Latence (ms)"])
        edges_layout.addWidget(self.edges_table)
        
        # Boutons de gestion des arêtes
        edges_buttons = QHBoxLayout()
        add_edge_btn = QPushButton("Ajouter Arête")
        add_edge_btn.clicked.connect(self.add_edge_row)
        remove_edge_btn = QPushButton("Supprimer Arête")
        remove_edge_btn.clicked.connect(self.remove_edge_row)
        generate_btn = QPushButton("Générer Réseau Aléatoire")
        generate_btn.clicked.connect(self.generate_random_network)
        edges_buttons.addWidget(add_edge_btn)
        edges_buttons.addWidget(remove_edge_btn)
        edges_buttons.addWidget(generate_btn)
        edges_layout.addLayout(edges_buttons)
        
        edges_group.setLayout(edges_layout)
        left_layout.addWidget(edges_group)
        
        # Boutons de contrôle
        control_layout = QHBoxLayout()
        self.solve_btn = QPushButton("Résoudre")
        self.solve_btn.clicked.connect(self.solve_optimization)
        self.solve_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 10px;")
        
        self.clear_btn = QPushButton("Réinitialiser")
        self.clear_btn.clicked.connect(self.clear_results)
        
        control_layout.addWidget(self.solve_btn)
        control_layout.addWidget(self.clear_btn)
        left_layout.addLayout(control_layout)
        
        # Barre de progression
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        left_layout.addWidget(self.progress_bar)
        
        left_layout.addStretch()
        
        # Layout droit (résultats et visualisation)
        right_layout = QVBoxLayout()
        
        # Tabs pour les résultats
        self.tabs = QTabWidget()
        
        # Tab 1: Visualisation du réseau
        self.network_canvas = NetworkCanvas()
        self.tabs.addTab(self.network_canvas, "Visualisation du Réseau")
        
        # Tab 2: Résultats détaillés
        results_widget = QWidget()
        results_layout = QVBoxLayout()
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setFont(QFont("Courier", 10))
        results_layout.addWidget(self.results_text)
        results_widget.setLayout(results_layout)
        self.tabs.addTab(results_widget, "Résultats Détaillés")
        
        # Tab 3: Flux optimaux
        flow_widget = QWidget()
        flow_layout = QVBoxLayout()
        self.flow_table = QTableWidget()
        self.flow_table.setColumnCount(4)
        self.flow_table.setHorizontalHeaderLabels(["Source", "Destination", 
                                                   "Flux", "Coût Total"])
        flow_layout.addWidget(self.flow_table)
        flow_widget.setLayout(flow_layout)
        self.tabs.addTab(flow_widget, "Flux Optimaux")
        
        right_layout.addWidget(self.tabs)
        
        # Ajouter les layouts au layout principal
        main_layout.addLayout(left_layout, 1)
        main_layout.addLayout(right_layout, 2)
        
        # Générer un réseau initial
        self.generate_random_network()
        
    def update_network_size(self):
        """Mise à jour de la taille du réseau"""
        self.edges_table.setRowCount(0)
        self.edges_data = []
        
    def add_edge_row(self):
        """Ajouter une ligne dans la table des arêtes"""
        row = self.edges_table.rowCount()
        self.edges_table.insertRow(row)
        
        # Valeurs par défaut
        self.edges_table.setItem(row, 0, QTableWidgetItem("0"))
        self.edges_table.setItem(row, 1, QTableWidgetItem("1"))
        self.edges_table.setItem(row, 2, QTableWidgetItem("100"))
        self.edges_table.setItem(row, 3, QTableWidgetItem("1.0"))
        self.edges_table.setItem(row, 4, QTableWidgetItem("10"))
        
    def remove_edge_row(self):
        """Supprimer la ligne sélectionnée"""
        current_row = self.edges_table.currentRow()
        if current_row >= 0:
            self.edges_table.removeRow(current_row)
            
    def generate_random_network(self):
        """Générer un réseau aléatoire"""
        num_nodes = self.nodes_spin.value()
        self.edges_table.setRowCount(0)
        
        # Créer un graphe connecté
        edges = set()
        
        # S'assurer que chaque nœud est connecté
        for i in range(num_nodes - 1):
            edges.add((i, i + 1))
        
        # Ajouter des connexions supplémentaires
        num_extra_edges = num_nodes * 2
        for _ in range(num_extra_edges):
            source = np.random.randint(0, num_nodes - 1)
            dest = np.random.randint(source + 1, num_nodes)
            edges.add((source, dest))
        
        # Remplir la table
        for idx, (source, dest) in enumerate(sorted(edges)):
            self.edges_table.insertRow(idx)
            capacity = np.random.randint(50, 200)
            cost = round(np.random.uniform(0.5, 5.0), 2)
            latency = np.random.randint(5, 50)
            
            self.edges_table.setItem(idx, 0, QTableWidgetItem(str(source)))
            self.edges_table.setItem(idx, 1, QTableWidgetItem(str(dest)))
            self.edges_table.setItem(idx, 2, QTableWidgetItem(str(capacity)))
            self.edges_table.setItem(idx, 3, QTableWidgetItem(str(cost)))
            self.edges_table.setItem(idx, 4, QTableWidgetItem(str(latency)))
        
        # Visualiser le réseau
        self.visualize_network()
        
    def get_edges_data(self):
        """Récupérer les données des arêtes depuis la table"""
        edges = []
        for row in range(self.edges_table.rowCount()):
            try:
                source = int(self.edges_table.item(row, 0).text())
                dest = int(self.edges_table.item(row, 1).text())
                capacity = float(self.edges_table.item(row, 2).text())
                cost = float(self.edges_table.item(row, 3).text())
                latency = float(self.edges_table.item(row, 4).text())
                edges.append((source, dest, capacity, cost, latency))
            except (ValueError, AttributeError) as e:
                QMessageBox.warning(self, "Erreur", 
                                  f"Données invalides à la ligne {row + 1}")
                return None
        return edges
    
    def visualize_network(self):
        """Visualiser le réseau sans solution"""
        edges = self.get_edges_data()
        if edges:
            num_nodes = self.nodes_spin.value()
            self.network_canvas.plot_network(num_nodes, edges)
    
    def solve_optimization(self):
        """Lancer l'optimisation"""
        # Récupérer les données
        edges = self.get_edges_data()
        if not edges:
            return
        
        num_nodes = self.nodes_spin.value()
        demand = self.demand_spin.value()
        objective = self.objective_combo.currentIndex()
        use_reliability = self.reliability_check.isChecked()
        use_balance = self.balance_check.isChecked()
        
        # Créer l'optimiseur
        self.optimizer = NetworkOptimizer(num_nodes, edges, demand, 
                                         objective, use_reliability, use_balance)
        
        # Désactiver les boutons
        self.solve_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Mode indéterminé
        
        # Lancer l'optimisation dans un thread séparé
        self.opt_thread = OptimizationThread(self.optimizer)
        self.opt_thread.finished.connect(self.on_optimization_finished)
        self.opt_thread.error.connect(self.on_optimization_error)
        self.opt_thread.start()
        
    def on_optimization_finished(self, results):
        """Callback quand l'optimisation est terminée"""
        self.solve_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        if results['status'] == 'optimal':
            self.display_results(results)
        else:
            QMessageBox.warning(self, "Attention", 
                              f"Statut: {results['status']}\n{results.get('message', '')}")
    
    def on_optimization_error(self, error_msg):
        """Callback en cas d'erreur"""
        self.solve_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        QMessageBox.critical(self, "Erreur", f"Erreur d'optimisation:\n{error_msg}")
        
    def display_results(self, results):
        """Afficher les résultats"""
        # Texte des résultats
        result_text = f"""
╔══════════════════════════════════════════════════════════════╗
║            RÉSULTATS DE L'OPTIMISATION                       ║
╚══════════════════════════════════════════════════════════════╝

Statut: {results['status'].upper()}
Temps de calcul: {results['solve_time']:.3f} secondes

╔══════════════════════════════════════════════════════════════╗
║            FONCTION OBJECTIF                                  ║
╚══════════════════════════════════════════════════════════════╝

Coût total: {results['total_cost']:.2f} unités monétaires
Latence moyenne: {results['avg_latency']:.2f} ms
Utilisation moyenne des liens: {results['avg_utilization']:.2%}

╔══════════════════════════════════════════════════════════════╗
║            STATISTIQUES DU RÉSEAU                             ║
╚══════════════════════════════════════════════════════════════╝

Flux total acheminé: {results['total_flow']:.2f} unités
Nombre de liens actifs: {results['active_links']}
Capacité totale utilisée: {results['total_capacity_used']:.2f}
Capacité totale disponible: {results['total_capacity']:.2f}

╔══════════════════════════════════════════════════════════════╗
║            CHEMINS PRINCIPAUX                                 ║
╚══════════════════════════════════════════════════════════════╝

"""
        # Ajouter les flux principaux
        for path in results.get('main_paths', []):
            result_text += f"\n{path}"
        
        self.results_text.setText(result_text)
        
        # Table des flux
        self.flow_table.setRowCount(0)
        for idx, (edge, flow) in enumerate(results['flows'].items()):
            if flow > 0.01:
                self.flow_table.insertRow(idx)
                source, dest = edge
                
                # Trouver le coût de cette arête
                cost_per_unit = 0
                for e in self.get_edges_data():
                    if e[0] == source and e[1] == dest:
                        cost_per_unit = e[3]
                        break
                
                total_cost = flow * cost_per_unit
                
                self.flow_table.setItem(idx, 0, QTableWidgetItem(str(source)))
                self.flow_table.setItem(idx, 1, QTableWidgetItem(str(dest)))
                self.flow_table.setItem(idx, 2, QTableWidgetItem(f"{flow:.2f}"))
                self.flow_table.setItem(idx, 3, QTableWidgetItem(f"{total_cost:.2f}"))
        
        # Visualisation du réseau avec la solution
        num_nodes = self.nodes_spin.value()
        edges = self.get_edges_data()
        self.network_canvas.plot_network(num_nodes, edges, results['flows'])
        
        # Passer à l'onglet visualisation
        self.tabs.setCurrentIndex(0)
        
    def clear_results(self):
        """Réinitialiser les résultats"""
        self.results_text.clear()
        self.flow_table.setRowCount(0)
        self.visualize_network()

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()