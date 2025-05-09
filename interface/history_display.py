import tkinter as tk
from tkinter import ttk
from datetime import datetime
import os
import csv

def refresh_history(tree: ttk.Treeview, history_file: str) -> None:
    """
    Rafraîchit l'affichage de l'historique avec les données les plus récentes.
    Cette fonction lit le fichier CSV d'historique et met à jour l'affichage
    en ajoutant des séparateurs entre les différentes simulations.
    
    Args:
        tree (ttk.Treeview): Le widget Treeview à mettre à jour
        history_file (str): Chemin vers le fichier d'historique
    """
    # Effacer toutes les entrées existantes pour éviter les doublons
    for item in tree.get_children():
        tree.delete(item)
    
    # Lecture et affichage des données du fichier CSV
    if os.path.exists(history_file):
        try:
            with open(history_file, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                previous_chronons = None
                for row in reader:
                    # Conversion du nombre de chronons en entier
                    try:
                        current_chronons = int(row['chronons'])
                    except Exception:
                        current_chronons = None
                    
                    # Ajout d'un séparateur entre les simulations
                    # (quand le nombre de chronons diminue, c'est une nouvelle simulation)
                    if previous_chronons is None or (current_chronons is not None and current_chronons < previous_chronons):
                        tree.insert('', 'end', values=('', '', '', '--- NOUVELLE SIMULATION ---', '', ''))
                    previous_chronons = current_chronons
                    
                    # Formatage de la date et de l'heure
                    date_obj = datetime.fromisoformat(row['date'])
                    date = date_obj.strftime('%Y-%m-%d')
                    time = date_obj.strftime('%H')
                    minute = date_obj.strftime('%M')
                    
                    # Insertion des données dans le tableau
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
    Cette fonction est appelée récursivement tant que la fenêtre est ouverte.
    
    Args:
        tree (ttk.Treeview): Le widget Treeview à mettre à jour
        history_file (str): Chemin vers le fichier d'historique
        history_window (tk.Toplevel): La fenêtre de l'historique
    """
    # Mise à jour de l'affichage
    refresh_history(tree, history_file)
    
    # Planification du prochain rafraîchissement si la fenêtre est toujours ouverte
    if history_window.winfo_exists():
        history_window.after(1000, lambda: auto_refresh(tree, history_file, history_window))

def display_simulation_history():
    """
    Affiche l'historique des simulations dans une fenêtre Tkinter.
    Cette fonction crée une nouvelle fenêtre avec un tableau affichant :
    - La date et l'heure de chaque enregistrement
    - Le nombre de chronons (tours)
    - Le nombre de poissons et de requins
    L'affichage est automatiquement mis à jour toutes les secondes.
    """
    # Définition du chemin vers le fichier d'historique
    history_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'simulation_history.csv')
    
    # Création de la fenêtre d'historique
    history_window = tk.Toplevel()
    history_window.title("Historique des Simulations")
    history_window.geometry("1000x600")
    
    # Création du cadre principal pour le tableau
    frame = ttk.Frame(history_window)
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Configuration du tableau
    columns = ('Date', 'Heure', 'Minute', 'Chronons', 'Poissons', 'Requins')
    tree = ttk.Treeview(frame, columns=columns, show='headings')
    
    # Définition des largeurs des colonnes
    column_widths = {
        'Date': 100,
        'Heure': 80,
        'Minute': 80,
        'Chronons': 100,
        'Poissons': 100,
        'Requins': 100
    }
    
    # Configuration des en-têtes et des colonnes
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=column_widths[col], anchor='center')
    
    # Configuration du style du tableau
    style = ttk.Style()
    style.configure("Treeview", rowheight=25)  # Hauteur des lignes
    style.configure("Treeview.Separator", background="gray")  # Couleur des séparateurs
    
    # Ajout de la barre de défilement verticale
    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    # Placement des éléments dans la fenêtre
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Affichage initial des données
    refresh_history(tree, history_file)
    
    # Démarrage du rafraîchissement automatique
    auto_refresh(tree, history_file, history_window)
    
    # Fonction pour effacer l'historique
    def clear_history():
        """
        Efface le contenu du fichier d'historique et du tableau.
        Réinitialise le fichier CSV avec uniquement l'en-tête.
        """
        try:
            # Réinitialisation du fichier CSV
            with open(history_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['date', 'chronons', 'fish_count', 'shark_count'])
            # Effacement du tableau
            for item in tree.get_children():
                tree.delete(item)
        except Exception as e:
            print(f"Erreur lors de l'effacement de l'historique : {e}")
    
    # Création du cadre pour le bouton d'effacement
    button_frame = ttk.Frame(history_window)
    button_frame.pack(fill=tk.X, padx=10, pady=5)
    
    # Ajout du bouton d'effacement
    clear_button = ttk.Button(button_frame, text="Effacer l'historique", command=clear_history)
    clear_button.pack(side=tk.RIGHT)

if __name__ == "__main__":
    display_simulation_history() 