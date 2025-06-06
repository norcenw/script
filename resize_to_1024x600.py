import os
from PIL import Image
from tqdm import tqdm

def resize_images(src_folder, dist_folder, target_size=(1025, 600), original_aspect_ratio=(2133, 1250)):
    # Crea la cartella di destinazione se non esiste
    if not os.path.exists(dist_folder):
        os.makedirs(dist_folder)

    # Scansiona tutti i file nella cartella sorgente
    files = [f for f in os.listdir(src_folder) if os.path.isfile(os.path.join(src_folder, f))]
    
    # Filtra solo le immagini
    images = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]

    # Calcola il rapporto di aspetto
    orig_width, orig_height = original_aspect_ratio
    target_width, target_height = target_size
    aspect_ratio = orig_width / orig_height

    # Ridimensiona ogni immagine mantenendo le proporzioni
    for image_name in tqdm(images, desc="Resizing Images"):
        image_path = os.path.join(src_folder, image_name)
        with Image.open(image_path) as img:
            img_aspect_ratio = img.width / img.height
            
            # Calcola la nuova dimensione mantenendo il rapporto di aspetto
            if img_aspect_ratio > aspect_ratio:
                # L'immagine è più larga rispetto al target, usa la larghezza come riferimento
                new_width = target_width
                new_height = int(target_width / img_aspect_ratio)
            else:
                # L'immagine è più alta rispetto al target, usa l'altezza come riferimento
                new_height = target_height
                new_width = int(target_height * img_aspect_ratio)

            # Ridimensiona l'immagine mantenendo il rapporto di aspetto
            img_resized = img.resize((new_width, new_height), Image.LANCZOS)
            
            # Salva l'immagine ridimensionata nella cartella di destinazione
            img_resized.save(os.path.join(dist_folder, image_name))

if __name__ == "__main__":
    src_folder = './src'  # Cartella sorgente
    dist_folder = './dist'  # Cartella destinazione
    resize_images(src_folder, dist_folder)
