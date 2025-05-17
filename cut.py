import cv2
import numpy as np
import os

def extract_elements_from_png(input_file, output_dir="dist", min_area=10):
    """
    Estrae tutti gli elementi (componenti connesse) da un'immagine PNG che hanno intorno uno sfondo trasparente
    e li salva come file PNG separati nella cartella di output.
    
    Args:
        input_file (str): Percorso del file PNG di input.
        output_dir (str): Cartella in cui salvare gli elementi estratti (default: "dist").
        min_area (int): Area minima (in pixel) per considerare un componente come valido (filtra il rumore).
    """
    # Carica l'immagine con il canale alpha
    img = cv2.imread(input_file, cv2.IMREAD_UNCHANGED)
    if img is None:
        print("Errore: immagine non trovata.")
        return

    # Verifica che l'immagine abbia un canale alpha
    if img.shape[2] < 4:
        print("L'immagine non ha un canale alpha.")
        return

    # Estrai il canale alpha e crea una maschera binaria:
    # I pixel con alpha > 0 sono considerati parte degli elementi
    alpha = img[:, :, 3]
    _, mask = cv2.threshold(alpha, 0, 255, cv2.THRESH_BINARY)
    
    # Trova le componenti connesse nella maschera
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(mask, connectivity=8)
    
    # Crea la cartella di output se non esiste
    os.makedirs(output_dir, exist_ok=True)
    
    count = 0
    # Salta l'etichetta 0 che rappresenta lo sfondo
    for label in range(1, num_labels):
        x, y, w, h, area = stats[label]
        if area < min_area:
            continue  # ignora componenti troppo piccole
        
        # Ritaglia l'elemento dal rettangolo delimitante
        element = img[y:y+h, x:x+w]
        output_file = os.path.join(output_dir, f"rock_{label}.png")
        cv2.imwrite(output_file, element)
        count += 1
        print(f"Elemento {label} salvato in: {output_file}")
    
    print(f"Estrazione completata: {count} elementi salvati in '{output_dir}'.")

if __name__ == "__main__":
    # Modifica il percorso dell'immagine in base alle tue esigenze
    input_file = "src/immagine.png"
    extract_elements_from_png(input_file)
