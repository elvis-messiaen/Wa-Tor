import json
from datetime import datetime
import os
import csv

def display_simulation_history():
    """
    Crée un fichier CSV avec l'historique des simulations
    """
    # Chemin vers le fichier d'historique
    history_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'simulation_history.json')
    # Chemin pour le fichier CSV de sortie
    csv_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'simulation_history.csv')
    
    try:
        # Lecture du fichier JSON
        with open(history_file, 'r') as f:
            history = json.load(f)
        
        # Création du fichier CSV
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # Écriture de l'en-tête
            writer.writerow(['Date', 'Heure', 'Minute', 'Chronons', 'Poissons', 'Requins'])
            
            # Écriture des données
            for entry in history:
                # Conversion de la date ISO en objet datetime
                date_obj = datetime.fromisoformat(entry['date'])
                
                # Formatage des données
                date_str = date_obj.strftime('%Y-%m-%d')
                hour = date_obj.strftime('%H')
                minute = date_obj.strftime('%M')
                
                # Écriture de la ligne
                writer.writerow([date_str, hour, minute, entry['chronons'], entry['fish_count'], entry['shark_count']])
        
        print(f"Le fichier CSV a été créé avec succès : {csv_file}")
            
    except FileNotFoundError:
        print("Erreur : Le fichier d'historique n'a pas été trouvé.")
    except json.JSONDecodeError:
        print("Erreur : Le fichier d'historique est corrompu.")
    except Exception as e:
        print(f"Une erreur est survenue : {str(e)}")

if __name__ == "__main__":
    display_simulation_history() 