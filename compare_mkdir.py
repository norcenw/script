import os
import pandas as pd

def compare_directories(dir1, dir2, output_excel):
    # Lista per memorizzare le differenze
    differences = []

    # Funzione per rimuovere l'estensione dal nome del file
    def remove_extension(filename):
        return os.path.splitext(filename)[0]

    # Funzione per ottenere una mappa dei file (nome senza estensione -> percorso completo)
    def get_file_map(directory):
        file_map = {}
        for root, _, files in os.walk(directory):
            for file in files:
                name_no_ext = remove_extension(file)
                file_map[name_no_ext] = os.path.join(root, file)
        return file_map

    # Ottieni le mappe dei file per entrambe le directory
    dir1_map = get_file_map(dir1)
    dir2_map = get_file_map(dir2)

    # Trova i file comuni e quelli unici
    common_files = set(dir1_map.keys()).intersection(set(dir2_map.keys()))
    only_in_dir1 = set(dir1_map.keys()) - set(dir2_map.keys())
    only_in_dir2 = set(dir2_map.keys()) - set(dir1_map.keys())

    # Aggiungi le differenze alla lista
    for file in only_in_dir1:
        differences.append({
            'Tipo': 'File mancante',
            'Percorso': dir1_map[file],
            'Dettaglio': f'Solo in {dir1}'
        })
    for file in only_in_dir2:
        differences.append({
            'Tipo': 'File mancante',
            'Percorso': dir2_map[file],
            'Dettaglio': f'Solo in {dir2}'
        })

    # Crea un DataFrame con le differenze
    df = pd.DataFrame(differences)

    # Salva il DataFrame in un file Excel
    df.to_excel(output_excel, index=False)
    print(f"File Excel delle differenze salvato in: {output_excel}")

# Percorsi delle cartelle da confrontare
src1 = 'src1'
src2 = 'src2'
output_excel = 'dist/differenze.xlsx'

# Esegui il confronto e genera il file Excel
compare_directories(src1, src2, output_excel)