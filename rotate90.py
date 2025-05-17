import os
from PIL import Image

# Cartelle di origine e destinazione
src_folder = "src"
dist_folder = "dist"

# Crea la cartella di destinazione se non esiste
if not os.path.exists(dist_folder):
    os.makedirs(dist_folder)

# Itera su tutti i file nella cartella src
for filename in os.listdir(src_folder):
    if filename.lower().endswith(".png"):
        src_path = os.path.join(src_folder, filename)
        dist_path = os.path.join(dist_folder, filename)
        try:
            # Apri l'immagine
            img = Image.open(src_path)
            # Ruota l'immagine di 90 gradi in senso antiorario
            img_rotated = img.rotate(90, expand=True)
            # Salva l'immagine nella cartella dist
            img_rotated.save(dist_path)
            print(f"Immagine {filename} elaborata e salvata in {dist_path}.")
        except Exception as e:
            print(f"Errore nell'elaborazione di {filename}: {e}")
