import os
from PIL import Image
from tqdm import tqdm

def resize_images(src_folder, dist_folder, size=(150, 150)):
    # Crea la cartella di destinazione se non esiste
    if not os.path.exists(dist_folder):
        os.makedirs(dist_folder)

    # Scansiona tutti i file nella cartella sorgente
    files = [f for f in os.listdir(src_folder) if os.path.isfile(os.path.join(src_folder, f))]
    
    # Filtra solo le immagini
    images = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]

    # Ridimensiona ogni immagine e salvala nella cartella dist
    for image_name in tqdm(images, desc="Resizing Images"):
        image_path = os.path.join(src_folder, image_name)
        with Image.open(image_path) as img:
            # Ridimensiona l'immagine a 150x150
            img_resized = img.resize(size, Image.LANCZOS)
            # Salva l'immagine ridimensionata nella cartella di destinazione
            img_resized.save(os.path.join(dist_folder, image_name))

if __name__ == "__main__":
    src_folder = './src'  # Cartella sorgente
    dist_folder = './dist'  # Cartella destinazione
    resize_images(src_folder, dist_folder)
