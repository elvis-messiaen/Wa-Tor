import tkinter as tk
from tkinter import ttk
from datetime import datetime
import os
import csv

def display_simulation_history():
    """
    Affiche l'historique des simulations dans une fenêtre Tkinter
    et sauvegarde dans un fichier CSV
    """
    # Chemin vers le fichier d'historique
    history_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'simulation_history.csv')
    
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
    
    # Ajout d'une barre de défilement
    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    # Placement des éléments
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Lecture et affichage des données
    if os.path.exists(history_file):
        try:
            with open(history_file, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    date_obj = datetime.fromisoformat(row['date'])
                    date = date_obj.strftime('%Y-%m-%d')
                    time = date_obj.strftime('%H:%M')
                    tree.insert('', 'end', values=(
                        date,
                        time,
                        row['chronons'],
                        row['fish_count'],
                        row['shark_count']
                    ))
        except Exception as e:
            print(f"Erreur lors de la lecture de l'historique : {e}")
    
    # Ajout d'un bouton pour effacer l'historique
    def clear_history():
        try:
            with open(history_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['date', 'chronons', 'fish_count', 'shark_count'])
            for item in tree.get_children():
                tree.delete(item)
        except Exception as e:
            print(f"Erreur lors de l'effacement de l'historique : {e}")
    
    # Créer un cadre pour le bouton
    button_frame = ttk.Frame(history_window)
    button_frame.pack(fill=tk.X, padx=10, pady=5)
    
    clear_button = ttk.Button(button_frame, text="Effacer l'historique", command=clear_history)
    clear_button.pack(side=tk.RIGHT)

if __name__ == "__main__":
    display_simulation_history() 