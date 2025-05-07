import tkinter as tk
from tkinter import ttk
from datetime import datetime
import os
import csv

def refresh_history(tree: ttk.Treeview, history_file: str) -> None:
    """
    Rafraîchit l'affichage de l'historique avec les données les plus récentes.
    
    Args:
        tree (ttk.Treeview): Le widget Treeview à mettre à jour
        history_file (str): Chemin vers le fichier d'historique
    """
    # Effacer toutes les entrées existantes
    for item in tree.get_children():
        tree.delete(item)
    
    # Recharger les données
    if os.path.exists(history_file):
        try:
            with open(history_file, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                previous_chronons = None
                for row in reader:
                    try:
                        current_chronons = int(row['chronons'])
                    except Exception:
                        current_chronons = None
                    # Insérer la démarcation si c'est la première ligne ou si la simulation redémarre
                    if previous_chronons is None or (current_chronons is not None and current_chronons < previous_chronons):
                        tree.insert('', 'end', values=('', '', '', '--- NOUVELLE SIMULATION ---', '', ''))
                    previous_chronons = current_chronons
                    date_obj = datetime.fromisoformat(row['date'])
                    date = date_obj.strftime('%Y-%m-%d')
                    time = date_obj.strftime('%H')
                    minute = date_obj.strftime('%M')
                    tree.insert('', 'end', values=(
                        date,
                        time,
                        minute,
                        row['chronons'],
                        row['fish_count'],
                        row['shark_count']
                    ))
        except Exception as e:
            print(f"Erreur lors de la lecture de l'historique : {e}")

def auto_refresh(tree: ttk.Treeview, history_file: str, history_window: tk.Toplevel) -> None:
    """
    Rafraîchit automatiquement l'historique toutes les secondes.
    
    Args:
        tree (ttk.Treeview): Le widget Treeview à mettre à jour
        history_file (str): Chemin vers le fichier d'historique
        history_window (tk.Toplevel): La fenêtre de l'historique
    """
    refresh_history(tree, history_file)
    # Planifier le prochain rafraîchissement si la fenêtre est toujours ouverte
    if history_window.winfo_exists():
        history_window.after(1000, lambda: auto_refresh(tree, history_file, history_window))

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
    history_window.geometry("1000x600")
    
    # Créer un cadre pour le tableau
    frame = ttk.Frame(history_window)
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Création du tableau
    columns = ('Date', 'Heure', 'Minute', 'Chronons', 'Poissons', 'Requins')
    tree = ttk.Treeview(frame, columns=columns, show='headings')
    
    # Configuration des colonnes
    column_widths = {
        'Date': 100,
        'Heure': 80,
        'Minute': 80,
        'Chronons': 100,
        'Poissons': 100,
        'Requins': 100
    }
    
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=column_widths[col], anchor='center')
    
    # Configuration du style pour les séparateurs
    style = ttk.Style()
    style.configure("Treeview", rowheight=25)  # Augmenter la hauteur des lignes
    style.configure("Treeview.Separator", background="gray")  # Couleur des séparateurs
    
    # Ajout d'une barre de défilement
    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    # Placement des éléments
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Lecture et affichage des données initiales
    refresh_history(tree, history_file)
    
    # Démarrer le rafraîchissement automatique
    auto_refresh(tree, history_file, history_window)
    
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
    
    # Bouton pour effacer l'historique
    clear_button = ttk.Button(button_frame, text="Effacer l'historique", command=clear_history)
    clear_button.pack(side=tk.RIGHT)

if __name__ == "__main__":
    display_simulation_history() 