import os
from PIL import Image
from tqdm import tqdm

def convert_images(src_folder, dist_folder):
    # Assicurati che la cartella di destinazione esista
    os.makedirs(dist_folder, exist_ok=True)

    # Trova tutte le sottocartelle in src_folder
    for root, _, files in os.walk(src_folder):
        # Percorso relativo della sottocartella rispetto a src_folder
        relative_path = os.path.relpath(root, src_folder)
        
        # Percorso della cartella di destinazione corrispondente
        target_folder = os.path.join(dist_folder, relative_path)
        os.makedirs(target_folder, exist_ok=True)

        # Filtra solo i file di immagini supportati
        images = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]

        # Barra di progresso per il processo di conversione
        for image_name in tqdm(images, desc=f"Converting images in {relative_path}", unit="file"):
            # Percorsi completi dei file sorgente e destinazione
            image_path = os.path.join(root, image_name)
            new_image_path = os.path.join(target_folder, os.path.splitext(image_name)[0] + '.bmp')
            
            # Apertura e conversione dell'immagine
            with Image.open(image_path) as img:
                rgb_img = img.convert("RGB")  # Converti in RGB (24 bit)
                rgb_img.save(new_image_path, format='BMP')  # Salva in BMP

if __name__ == "__main__":
    src_folder = './src'  # Cartella di origine
    dist_folder = './dist'  # Cartella di destinazione
    convert_images(src_folder, dist_folder)
