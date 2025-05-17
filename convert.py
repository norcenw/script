import os
from PIL import Image

def convert_images_to_bmp(src_folder="src", dist_folder="dist"):
    # Creazione della cartella di destinazione se non esiste
    os.makedirs(dist_folder, exist_ok=True)
    
    # Scansione della cartella sorgente per i file immagine
    for filename in os.listdir(src_folder):
        file_path = os.path.join(src_folder, filename)
        
        # Verifica se il file è un'immagine
        try:
            with Image.open(file_path) as img:
                # Conversione a BMP 24 bit
                bmp_filename = os.path.splitext(filename)[0] + ".bmp"
                bmp_path = os.path.join(dist_folder, bmp_filename)
                img.convert("RGB").save(bmp_path, "BMP")
                print(f"Convertito: {filename} -> {bmp_filename}")
        except Exception as e:
            print(f"Errore con {filename}: {e}")

if __name__ == "__main__":
    convert_images_to_bmp()
