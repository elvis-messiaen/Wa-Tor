import tkinter as tk
from tkinter import ttk
from datetime import datetime
from typing import List, Dict
import csv
import os

class SimulationHistory:
    """
    Classe gérant l'historique des simulations Wa-Tor.
    Cette classe permet de :
    - Sauvegarder les données de chaque simulation
    - Charger l'historique depuis un fichier CSV
    - Afficher l'historique dans une interface graphique
    - Effacer l'historique
    """
    
    def __init__(self):
        """
        Initialise l'historique des simulations.
        Crée une liste vide pour stocker les simulations et charge l'historique existant.
        """
        self.simulations: List[Dict] = []  # Liste des simulations avec leurs données
        self.history_file = "simulation_history.csv"  # Fichier de sauvegarde
        self.load_history()  # Chargement de l'historique existant
    
    def add_simulation(self, chronons: int, fish_count: int, shark_count: int):
        """
        Ajoute une nouvelle simulation à l'historique.
        
        Args:
            chronons (int): Nombre de tours de la simulation
            fish_count (int): Nombre de poissons à la fin de la simulation
            shark_count (int): Nombre de requins à la fin de la simulation
        """
        # Création d'un dictionnaire avec les données de la simulation
        simulation = {
            'date': datetime.now().isoformat(),  # Date et heure actuelles
            'chronons': chronons,  # Nombre de tours
            'fish_count': fish_count,  # Nombre de poissons
            'shark_count': shark_count  # Nombre de requins
        }
        self.simulations.append(simulation)  # Ajout à la liste
        self.save_history()  # Sauvegarde dans le fichier
    
    def save_history(self):
        """
        Sauvegarde l'historique dans un fichier CSV.
        Le fichier contient les colonnes : date, chronons, fish_count, shark_count.
        """
        try:
            with open(self.history_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['date', 'chronons', 'fish_count', 'shark_count'])
                writer.writeheader()  # Écriture de l'en-tête
                writer.writerows(self.simulations)  # Écriture des données
        except Exception as e:
            print(f"Erreur lors de la sauvegarde de l'historique : {e}")
    
    def load_history(self):
        """
        Charge l'historique depuis le fichier CSV.
        Si le fichier n'existe pas ou s'il y a une erreur, initialise une liste vide.
        """
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', newline='', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    self.simulations = list(reader)  # Conversion en liste
            except Exception as e:
                print(f"Erreur lors du chargement de l'historique : {e}")
                self.simulations = []  # Initialisation d'une liste vide en cas d'erreur
    
    def show_history_window(self):
        """
        Affiche une fenêtre avec l'historique des simulations.
        La fenêtre contient un tableau avec les colonnes :
        - Date
        - Heure
        - Chronons (nombre de tours)
        - Nombre de poissons
        - Nombre de requins
        """
        # Création de la fenêtre d'historique
        history_window = tk.Toplevel()
        history_window.title("Historique des Simulations")
        history_window.geometry("800x600")
        
        # Création du cadre principal pour le tableau
        frame = ttk.Frame(history_window)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Configuration du tableau
        columns = ('Date', 'Heure', 'Chronons', 'Poissons', 'Requins')
        tree = ttk.Treeview(frame, columns=columns, show='headings')
        
        # Configuration des colonnes
        for col in columns:
            tree.heading(col, text=col)  # En-têtes des colonnes
            tree.column(col, width=120)  # Largeur des colonnes
        
        # Ajout des données dans le tableau
        for sim in self.simulations:
            try:
                # Formatage de la date et de l'heure
                date_obj = datetime.fromisoformat(sim['date'])
                date = date_obj.strftime('%Y-%m-%d')
                time = date_obj.strftime('%H:%M')
                
                # Insertion des données dans le tableau
                tree.insert('', 'end', values=(
                    date,
                    time,
                    sim['chronons'],
                    sim['fish_count'],
                    sim['shark_count']
                ))
            except Exception as e:
                print(f"Erreur lors de l'affichage d'une simulation : {e}")
        
        # Ajout de la barre de défilement verticale
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Placement des éléments dans la fenêtre
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Fonction pour effacer l'historique
        def clear_history():
            """
            Efface l'historique des simulations.
            Vide la liste des simulations et le tableau d'affichage.
            """
            self.simulations = []  # Vidage de la liste
            self.save_history()  # Sauvegarde du fichier vide
            for item in tree.get_children():
                tree.delete(item)  # Effacement du tableau
        
        # Création du cadre pour le bouton d'effacement
        button_frame = ttk.Frame(history_window)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Ajout du bouton d'effacement
        clear_button = ttk.Button(button_frame, text="Effacer l'historique", command=clear_history)
        clear_button.pack(side=tk.RIGHT) 