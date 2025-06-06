import os
import cv2
import pytesseract
from PIL import Image

# Specifica il percorso dell'eseguibile di Tesseract (modifica se necessario)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def preprocess_image(image_path):
    """Carica e pre-processa l'immagine per migliorare il riconoscimento OCR"""
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # Converti in scala di grigi
    _, img = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)  # Applica binarizzazione
    return img

def find_text_in_images(src_folder, search_text):
    matches = []
    
    print(f"\n Inizio scansione nella cartella: {src_folder}\n")

    # Scandisce la cartella e tutte le sottocartelle
    for root, _, files in os.walk(src_folder):
        for file in files:
            if file.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".tiff")):
                img_path = os.path.join(root, file)
                
                print(f"Analizzando immagine: {img_path}...")

                try:
                    # Pre-processa l'immagine
                    img = preprocess_image(img_path)
                    
                    # Estrai il testo
                    extracted_text = pytesseract.image_to_string(img, lang="eng")  # Cambia la lingua se necessario
                    
                    # Mostra il testo estratto (log)
                    print(f" Testo estratto da {file}:\n{extracted_text.strip()}\n{'-'*50}")
                    
                    # Verifica se la scritta è presente
                    if search_text.lower() in extracted_text.lower():
                        print(f" Match trovato in {img_path}!\n")
                        matches.append(img_path)
                
                except Exception as e:
                    print(f" Errore nell'elaborazione di {img_path}: {e}")

    return matches

if __name__ == "__main__":
    src_directory = "src"  # Cartella principale
    search_phrase = input("Inserisci la scritta da cercare: ")
    
    results = find_text_in_images(src_directory, search_phrase)
    
    print("\n**Risultati della ricerca:**")
    if results:
        print(f"\n{len(results)} immagini trovate con la scritta \"{search_phrase}\":")
        for path in results:
            print(f"- {path}")
    else:
        print("\n Nessuna immagine trovata con la scritta specificata.")
    
    print("\nScansione completata!")
