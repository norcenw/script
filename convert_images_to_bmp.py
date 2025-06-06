import os
from PIL import Image
from tqdm import tqdm

def convert_images(src_folder, dist_folder):
    # Crea la cartella di destinazione se non esiste
    if not os.path.exists(dist_folder):
        os.makedirs(dist_folder)

    # Ottiene tutti i file nella cartella sorgente
    files = [f for f in os.listdir(src_folder) if os.path.isfile(os.path.join(src_folder, f))]

    # Filtra solo le immagini e crea un iteratore per la barra di progresso
    images = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
    progress = tqdm(images, desc='Converting Images')

    # Processo di conversione
    for image_name in progress:
        image_path = os.path.join(src_folder, image_name)
        # Apertura e conversione dell'immagine
        with Image.open(image_path) as img:
            img = img.convert("RGB")  # Assicurati che sia in formato RGB
            # Costruzione del nuovo percorso del file
            new_image_path = os.path.join(dist_folder, os.path.splitext(image_name)[0] + '.bmp')
            # Salvataggio dell'immagine convertita
            img.save(new_image_path, format='BMP', bits=24)

if __name__ == "__main__":
    src_folder = 'src'
    dist_folder = 'dist'
    convert_images(src_folder, dist_folder)