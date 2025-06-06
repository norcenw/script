import os
from PIL import Image
from tqdm import tqdm

def convert_images(src_folder, dist_folder):
    # Controlla se la cartella sorgente esiste
    if not os.path.exists(src_folder):
        print(f"La cartella di origine '{src_folder}' non esiste!")
        return

    # Crea la cartella di destinazione se non esiste
    if not os.path.exists(dist_folder):
        os.makedirs(dist_folder)

    # Ottiene tutti i file presenti nella cartella src
    files = [f for f in os.listdir(src_folder) if os.path.isfile(os.path.join(src_folder, f))]
    
    # Filtra solo i file che sono immagini (supporta png, jpg, jpeg, bmp, gif)
    images = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
    
    # Utilizza tqdm per mostrare una barra di progresso durante la conversione
    for image_name in tqdm(images, desc="Conversione immagini"):
        image_path = os.path.join(src_folder, image_name)
        try:
            with Image.open(image_path) as img:
                # Converte l'immagine in RGB (utile per alcune immagini con trasparenza o altri formati)
                img = img.convert("RGB")
                # Costruisce il nuovo nome con estensione .png
                new_image_name = os.path.splitext(image_name)[0] + '.png'
                new_image_path = os.path.join(dist_folder, new_image_name)
                # Salva l'immagine in formato PNG
                img.save(new_image_path, format='PNG')
        except Exception as e:
            print(f"Errore nella conversione di {image_name}: {e}")

if __name__ == "__main__":
    src_folder = './src'   # Cartella sorgente contenente le immagini
    dist_folder = 'dist' # Cartella di destinazione per le immagini convertite
    convert_images(src_folder, dist_folder)
