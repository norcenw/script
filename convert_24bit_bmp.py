import os
from PIL import Image
from tqdm import tqdm

# Percorsi delle cartelle sorgente e destinazione
src_folder = './src'
dist_folder = './dist'

# Assicurati che la cartella di destinazione esista
os.makedirs(dist_folder, exist_ok=True)

# Lista per tenere traccia dei file da convertire
files_to_convert = [f for f in os.listdir(src_folder) if f.endswith('.bmp')]

# Stampa il numero e i nomi dei file che saranno convertiti
print(f"Numero di file da convertire: {len(files_to_convert)}")
for file_name in files_to_convert:
    print(file_name)

# Barra di progresso per monitorare l'avanzamento della conversione
for file_name in tqdm(files_to_convert, desc="Converting", unit="file"):
    # Percorso completo del file sorgente e destinazione
    src_path = os.path.join(src_folder, file_name)
    dist_path = os.path.join(dist_folder, file_name)

    # Apri l'immagine e convertila in formato BMP a 24 bit
    with Image.open(src_path) as img:
        rgb_img = img.convert('RGB')
        rgb_img.save(dist_path, format='BMP')

print("Conversione completata.")
