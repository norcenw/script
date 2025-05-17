import cv2
import numpy as np
import os

def estrai_elementi_su_bianco(input_file, output_dir="dist", min_area=10):
    """
    Estrae tutti gli elementi (componenti connesse) da un'immagine con sfondo bianco
    e li salva come file PNG separati nella cartella di output.
    
    Args:
        input_file (str): Percorso del file immagine di input.
        output_dir (str): Cartella in cui salvare gli elementi estratti (default: "dist").
        min_area (int): Area minima (in pixel) per considerare un componente come valido (filtra il rumore).
    """
    # Carica l'immagine (senza canale alpha)
    img = cv2.imread(input_file, cv2.IMREAD_COLOR)
    if img is None:
        print(f"Errore: immagine non trovata o non valida: {input_file}")
        return

    # Converti l'immagine in scala di grigi
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Crea una maschera dei pixel "non bianchi" con soglia alta.
    # Tutti i pixel con valore < 250 diventano 255 nella maschera (foreground).
    # Invertiamo la soglia per avere come foreground le aree "non bianche".
    _, mask = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY_INV)

    # Trova le componenti connesse nella maschera
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(mask, connectivity=8)
    
    count = 0
    # label 0 è lo sfondo, partiamo da 1
    for label in range(1, num_labels):
        x, y, w, h, area = stats[label]
        if area < min_area:
            continue  # ignora componenti troppo piccole

        # Ritaglia l'elemento dal rettangolo delimitante
        elemento = img[y:y+h, x:x+w]
        output_file = os.path.join(output_dir, f"elemento_{label}.png")
        cv2.imwrite(output_file, elemento)
        count += 1
        print(f"Elemento {label} salvato in: {output_file}")
    
    print(f"Estrazione completata per '{input_file}': {count} elementi salvati in '{output_dir}'.")


def estrai_elementi_su_bianco_da_directory(input_dir="src", output_dir="dist", min_area=10):
    """
    Scansiona la cartella `input_dir`, individua tutti i file immagine
    e per ognuno estrae i componenti su sfondo bianco salvandoli nella cartella `output_dir`.
    
    Args:
        input_dir (str): Cartella di input che contiene le immagini da elaborare.
        output_dir (str): Cartella di output principale.
        min_area (int): Area minima (in pixel) per considerare un componente come valido.
    """
    if not os.path.isdir(input_dir):
        print(f"Errore: '{input_dir}' non è una cartella valida.")
        return

    # Crea la cartella di output principale se non esiste
    os.makedirs(output_dir, exist_ok=True)

    # Itera su tutti i file nella cartella di input
    for filename in os.listdir(input_dir):
        # Percorso completo del file
        file_path = os.path.join(input_dir, filename)

        # Verifica che non sia una sottocartella e che abbia estensione immagine
        if os.path.isfile(file_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            # Crea una sotto-cartella in base al nome del file (senza estensione),
            # in modo da salvare i ritagli in un posto dedicato.
            nome_base = os.path.splitext(filename)[0]
            destinazione = os.path.join(output_dir, nome_base)
            os.makedirs(destinazione, exist_ok=True)

            print(f"\nProcesso file: {filename}")
            estrai_elementi_su_bianco(file_path, output_dir=destinazione, min_area=min_area)


if __name__ == "__main__":
    # Esempio di utilizzo:
    estrai_elementi_su_bianco_da_directory(input_dir="src", output_dir="dist", min_area=10)
