import tkinter as tk
from tkinter import ttk
from datetime import datetime
from typing import List, Dict
import csv
import os

class SimulationHistory:
    def __init__(self):
        self.simulations: List[Dict] = []
        self.history_file = "simulation_history.csv"
        self.load_history()
    
    def add_simulation(self, chronons: int, fish_count: int, shark_count: int):
        """Ajoute une nouvelle simulation à l'historique"""
        simulation = {
            'date': datetime.now().isoformat(),
            'chronons': chronons,
            'fish_count': fish_count,
            'shark_count': shark_count
        }
        self.simulations.append(simulation)
        self.save_history()
    
    def save_history(self):
        """Sauvegarde l'historique dans un fichier CSV"""
        try:
            with open(self.history_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['date', 'chronons', 'fish_count', 'shark_count'])
                writer.writeheader()
                writer.writerows(self.simulations)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde de l'historique : {e}")
    
    def load_history(self):
        """Charge l'historique depuis le fichier CSV"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', newline='', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    self.simulations = list(reader)
            except Exception as e:
                print(f"Erreur lors du chargement de l'historique : {e}")
                self.simulations = []
    
    def show_history_window(self):
        """Affiche une fenêtre avec l'historique des simulations"""
        # Créer une nouvelle fenêtre
        history_window = tk.Toplevel()
        history_window.title("Historique des Simulations")
        history_window.geometry("800x600")
        
        # Créer un cadre pour le tableau
        frame = ttk.Frame(history_window)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Création du tableau
        columns = ('Date', 'Heure', 'Chronons', 'Poissons', 'Requins')
        tree = ttk.Treeview(frame, columns=columns, show='headings')
        
        # Configuration des colonnes
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        # Ajout des données
        for sim in self.simulations:
            try:
                date_obj = datetime.fromisoformat(sim['date'])
                date = date_obj.strftime('%Y-%m-%d')
                time = date_obj.strftime('%H:%M')
                tree.insert('', 'end', values=(
                    date,
                    time,
                    sim['chronons'],
                    sim['fish_count'],
                    sim['shark_count']
                ))
            except Exception as e:
                print(f"Erreur lors de l'affichage d'une simulation : {e}")
        
        # Ajout d'une barre de défilement
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Placement des éléments
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Ajout d'un bouton pour effacer l'historique
        def clear_history():
            self.simulations = []
            self.save_history()
            for item in tree.get_children():
                tree.delete(item)
        
        # Créer un cadre pour le bouton
        button_frame = ttk.Frame(history_window)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        clear_button = ttk.Button(button_frame, text="Effacer l'historique", command=clear_history)
        clear_button.pack(side=tk.RIGHT) 