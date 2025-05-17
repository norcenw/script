import cv2
import numpy as np
import os

def allinea_carta_verticale(img, threshold_value=200):
    """
    Ruota e ritaglia una singola immagine di carta in modo che sia allineata verticalmente
    (lato lungo in verticale e lato corto in basso).
    
    Args:
        img (numpy.ndarray): Immagine originale (BGR o BGRA).
        threshold_value (int): Valore di soglia per separare la carta dallo sfondo.
        
    Returns:
        numpy.ndarray: Immagine ruotata e ritagliata (BGRA) oppure None se non si trova alcun contorno.
    """
    # Se l'immagine non ha il canale alfa, lo aggiungiamo
    if len(img.shape) == 2:
        img_bgra = cv2.cvtColor(img, cv2.COLOR_GRAY2BGRA)
    elif img.shape[2] == 3:
        img_bgra = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    else:
        img_bgra = img.copy()

    # Utilizziamo i primi 3 canali (BGR) per trovare il contorno
    bgr = img_bgra[:, :, :3]
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    # Soglia inversa: assumiamo che la carta sia scura rispetto allo sfondo bianco
    _, thresh = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY_INV)

    # Trova il contorno esterno più grande (presumibilmente la carta)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None
    cnt = max(contours, key=cv2.contourArea)

    # Calcola il rettangolo con orientamento minimo che racchiude il contorno
    rect = cv2.minAreaRect(cnt)
    (cx, cy), (w, h), angle = rect

    # Se w < h, ruotiamo di 90° per standardizzare il rettangolo (w diventa la dimensione maggiore)
    if w < h:
        w, h = h, w
        angle += 90

    # Ruota l'immagine di -angle gradi attorno al centro trovato
    rows, cols = bgr.shape[:2]
    M = cv2.getRotationMatrix2D((cx, cy), -angle, 1.0)
    rotated = cv2.warpAffine(img_bgra, M, (cols, rows), flags=cv2.INTER_CUBIC,
                             borderMode=cv2.BORDER_CONSTANT,
                             borderValue=(255, 255, 255, 0))

    # Dopo la rotazione, ricalcoliamo il contorno per ritagliare la carta
    if rotated.shape[2] == 4:
        bgr_rot = rotated[:, :, :3]
    else:
        bgr_rot = rotated
    gray_rot = cv2.cvtColor(bgr_rot, cv2.COLOR_BGR2GRAY)
    _, thresh_rot = cv2.threshold(gray_rot, threshold_value, 255, cv2.THRESH_BINARY_INV)
    contours_rot, _ = cv2.findContours(thresh_rot, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours_rot:
        return None
    cnt_rot = max(contours_rot, key=cv2.contourArea)
    x, y, w2, h2 = cv2.boundingRect(cnt_rot)
    carta_ritagliata = rotated[y:y+h2, x:x+w2]

    # Assicuriamoci che l'immagine risultante sia in "portrait" (più alta che larga)
    final_h, final_w = carta_ritagliata.shape[:2]
    if final_w > final_h:
        carta_ritagliata = cv2.rotate(carta_ritagliata, cv2.ROTATE_90_COUNTERCLOCKWISE)

    return carta_ritagliata

def processa_cartella(src_dir="src", dist_dir="dist", threshold_value=200):
    """
    Scorre tutti i file immagine presenti nella cartella 'src' e li elabora per
    mettere la carta in verticale, salvando i risultati nella cartella 'dist'.
    """
    os.makedirs(dist_dir, exist_ok=True)

    for file_name in os.listdir(src_dir):
        if file_name.lower().endswith((".png", ".jpg", ".jpeg")):
            input_path = os.path.join(src_dir, file_name)
            img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
            if img is None:
                print(f"Errore nel caricamento di {input_path}")
                continue

            carta_allineata = allinea_carta_verticale(img, threshold_value=threshold_value)
            if carta_allineata is None:
                print(f"Nessuna carta trovata in {input_path}")
                continue

            output_path = os.path.join(dist_dir, file_name)
            cv2.imwrite(output_path, carta_allineata)
            print(f"Salvato: {output_path}")

if __name__ == "__main__":
    processa_cartella(src_dir="src", dist_dir="dist", threshold_value=200)
