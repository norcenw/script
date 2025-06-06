from PIL import Image
import os

# Definisci i percorsi delle cartelle
src_folder = './src'
dist_folder = './dist'

# Colore da cercare (in formato RGB)
target_color = (38, 43, 45)  # Corrisponde a #262b2d

# Crea la cartella di destinazione se non esiste
if not os.path.exists(dist_folder):
    os.makedirs(dist_folder)

# Funzione per ritagliare e salvare l'immagine
def process_image(image_path, output_path):
    # Apri l'immagine
    img = Image.open(image_path).convert("RGB")
    pixels = img.load()

    # Trova i bordi del contenuto all'interno del colore target
    left, top, right, bottom = img.width, img.height, 0, 0

    for y in range(img.height):
        for x in range(img.width):
            if pixels[x, y] == target_color:
                if x < left:
                    left = x
                if x > right:
                    right = x
                if y < top:
                    top = y
                if y > bottom:
                    bottom = y

    # Ritaglia l'immagine
    if left < right and top < bottom:
        cropped_img = img.crop((left, top, right, bottom))
        # Ridimensiona l'immagine (opzionale)
        cropped_img = cropped_img.resize((cropped_img.width // 2, cropped_img.height // 2))
        # Salva l'immagine
        cropped_img.save(output_path)
        print(f"Immagine processata e salvata: {output_path}")
    else:
        print(f"Nessun contenuto trovato per il colore {target_color} in {image_path}")

# Elabora tutte le immagini nella cartella src
for filename in os.listdir(src_folder):
    if filename.endswith(('.png', '.jpg', '.jpeg')):
        src_path = os.path.join(src_folder, filename)
        dist_path = os.path.join(dist_folder, filename)
        process_image(src_path, dist_path)

print("Elaborazione completata!")