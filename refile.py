import cv2
import numpy as np
import os

def trova_contorno_principale(img_bin, area_minima=1000):
    """
    Ritorna il contorno di area massima (superiore a 'area_minima')
    trovato in un'immagine binaria.
    """
    contours, _ = cv2.findContours(img_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    max_area = 0
    best_contour = None

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > max_area and area > area_minima:
            max_area = area
            best_contour = cnt
    
    return best_contour

def ottieni_quattro_vertici_approx(contour, tolleranza=0.02):
    """
    Prova ad approssimare un contorno a un poligono di 4 vertici
    (utile per la correzione prospettica).
    Restituisce i vertici in caso di successo, altrimenti None.
    """
    peri = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, tolleranza * peri, True)
    if len(approx) == 4:
        return approx
    else:
        return None

def ordina_punti_poligono(pts):
    """
    Riordina i 4 punti (x,y) di un quadrilatero in modo da poter
    effettuare una trasformazione prospettica corretta.
    """
    pts = pts.reshape(4, 2)
    # Ordina per Y (top->bottom)
    sorted_y = pts[np.argsort(pts[:,1]), :]
    top = sorted_y[:2, :]
    bottom = sorted_y[2:, :]

    # Ordina i due punti top e bottom da sinistra a destra
    top = top[np.argsort(top[:,0]), :]
    bottom = bottom[np.argsort(bottom[:,0]), :]

    # Ritorna nell’ordine: top-left, top-right, bottom-left, bottom-right
    return np.array([top[0], top[1], bottom[0], bottom[1]], dtype="float32")

def warp_immagine(img, punti, margine=10):
    """
    Esegue la trasformazione prospettica di un quadrilatero in un rettangolo.
    """
    pts_ordinati = ordina_punti_poligono(punti)

    # Calcola le dimensioni del nuovo rettangolo
    (tl, tr, bl, br) = pts_ordinati
    widthA = np.linalg.norm(br - bl)
    widthB = np.linalg.norm(tr - tl)
    heightA = np.linalg.norm(tr - br)
    heightB = np.linalg.norm(tl - bl)
    maxWidth = int(max(widthA, widthB))
    maxHeight = int(max(heightA, heightB))

    # Matrice di destinazione (rettangolo dritto)
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [0, maxHeight - 1],
        [maxWidth - 1, maxHeight - 1]
    ], dtype="float32")

    # Matrice di trasformazione
    M = cv2.getPerspectiveTransform(pts_ordinati, dst)
    warped = cv2.warpPerspective(img, M, (maxWidth, maxHeight))
    
    # Ritaglia un margine interno (opzionale)
    if margine > 0:
        h, w = warped.shape[:2]
        cropped = warped[margine:h-margine, margine:w-margine]
        return cropped
    else:
        return warped

def crea_maschera_angoli_arrotondati(width, height, raggio=30):
    """
    Crea una maschera RGBA con canale alpha che ha
    un rettangolo di dimensioni (width x height) e angoli arrotondati.
    """
    mask = np.zeros((height, width, 4), dtype=np.uint8)
    alpha_channel = np.zeros((height, width), dtype=np.uint8)

    # Disegna un rettangolo con angoli arrotondati in bianco (255) sull'alpha_channel
    cv2.rectangle(alpha_channel, (raggio, 0), (width - raggio, height), 255, -1)
    cv2.rectangle(alpha_channel, (0, raggio), (width, height - raggio), 255, -1)
    cv2.circle(alpha_channel, (raggio, raggio), raggio, 255, -1)
    cv2.circle(alpha_channel, (width - raggio, raggio), raggio, 255, -1)
    cv2.circle(alpha_channel, (raggio, height - raggio), raggio, 255, -1)
    cv2.circle(alpha_channel, (width - raggio, height - raggio), raggio, 255, -1)

    mask[..., 3] = alpha_channel
    return mask

def processa_carta(
    input_path,
    output_path,
    area_minima=1000,
    usa_trasf_prospettica=True,
    mantieni_angoli_arrotondati=True,
    raggio_angoli=30
):
    """
    - Trova la sagoma principale della carta
    - Esegue il crop rettangolare (bounding rect)
    - (Opzionale) Corregge l’orientamento con trasformazione prospettica
    - (Opzionale) Applica maschera con angoli arrotondati e salva in PNG con trasparenza
    """
    img = cv2.imread(input_path)
    if img is None:
        print(f"Impossibile aprire l'immagine: {input_path}")
        return

    # Converti in scala di grigi
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Threshold per separare la carta dallo sfondo (se bianco/chiaro)
    _, bin_img = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

    # Trova contorno principale
    contorno = trova_contorno_principale(bin_img, area_minima=area_minima)
    if contorno is None:
        print(f"Nessun contorno valido per {input_path}. Salto.")
        return

    # Crop di base
    x, y, w, h = cv2.boundingRect(contorno)
    carta_cropped = img[y:y+h, x:x+w]

    # Trasformazione prospettica (se abbiamo 4 vertici)
    if usa_trasf_prospettica:
        approx = ottieni_quattro_vertici_approx(contorno)
        if approx is not None:
            carta_cropped = warp_immagine(img, approx)
        else:
            print("Impossibile approssimare a 4 vertici. Uso boundingRect semplice.")

    # Angoli arrotondati
    if mantieni_angoli_arrotondati:
        h2, w2 = carta_cropped.shape[:2]
        # Crea la maschera con gli angoli arrotondati
        maschera_rgba = crea_maschera_angoli_arrotondati(w2, h2, raggio=raggio_angoli)
        # Converte la carta in BGRA
        carta_rgba = cv2.cvtColor(carta_cropped, cv2.COLOR_BGR2BGRA)
        # Applica la maschera al canale alpha
        carta_rgba[..., 3] = maschera_rgba[..., 3]
        cv2.imwrite(output_path, carta_rgba)
        print(f"Salvato con angoli arrotondati: {output_path}")
    else:
        # Salva normale in PNG
        cv2.imwrite(output_path, carta_cropped)
        print(f"Salvato (senza angoli arrotondati): {output_path}")

def processa_tutte_le_carte(
    input_dir="src",
    output_dir="dist",
    area_minima=1000,
    usa_trasf_prospettica=True,
    mantieni_angoli_arrotondati=True,
    raggio_angoli=30
):
    """
    Itera su tutte le immagini in input_dir, le processa e salva in output_dir.
    """
    if not os.path.isdir(input_dir):
        print(f"Cartella di input non trovata: {input_dir}")
        return

    os.makedirs(output_dir, exist_ok=True)

    # Filtra i file immagine
    estensioni_valide = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff')
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(estensioni_valide):
            input_path = os.path.join(input_dir, filename)
            nome_base, est = os.path.splitext(filename)
            # Output file, aggiungiamo un suffisso "_output" (o come preferisci)
            output_file = os.path.join(output_dir, f"{nome_base}_output.png")

            print(f"\nProcesso: {filename}")
            processa_carta(
                input_path=input_path,
                output_path=output_file,
                area_minima=area_minima,
                usa_trasf_prospettica=usa_trasf_prospettica,
                mantieni_angoli_arrotondati=mantieni_angoli_arrotondati,
                raggio_angoli=raggio_angoli
            )

if __name__ == "__main__":
    # Esempio di utilizzo
    processa_tutte_le_carte(
        input_dir="src",       # cartella sorgente
        output_dir="dist",     # cartella destinazione
        area_minima=1000,      # area minima contorno
        usa_trasf_prospettica=True,       # raddrizza la carta se riesce
        mantieni_angoli_arrotondati=True, # applica maschera con angoli arrotondati
        raggio_angoli=30                  # dimensione arrotondamento
    )
