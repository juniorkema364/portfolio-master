import pyotp
from pyzbar.pyzbar import decode
from PIL import Image
import urllib.parse

# Fonction pour scanner le code QR et extraire l'URL
def scan_qr_code(image_path):
    # Charger l'image contenant le code QR
    img = Image.open(image_path)

    # Décoder le code QR
    decoded_objects = decode(img)

    for obj in decoded_objects:
        # Extraire l'URL du QR code
        qr_data = obj.data.decode('utf-8')
        return qr_data

    return None

# Fonction pour extraire les informations de l'URL
def extract_info_from_url(url):
    # Analyser l'URL pour obtenir les paramètres
    parsed_url = urllib.parse.urlparse(url)
    query_params = urllib.parse.parse_qs(parsed_url.query)

    # Extraire le nom du vérificateur (issuer) et la clé secrète (secret)
    issuer = parsed_url.path.split(':')[0]  # Exemple : 'Heroku'
    secret = query_params.get('secret', [None])[0]  # Exemple : la clé secrète

    return issuer, secret

# Fonction pour générer le code de vérification
def generate_verification_code(secret):
    if secret:
        totp = pyotp.TOTP(secret)
        return totp.now()
    return None

# Chemin vers l'image contenant le code QR
image_path = 'image.png'  # Remplace avec le chemin de ton image

# Étape 1 : Scanner le QR code
qr_url = scan_qr_code(image_path)

if qr_url:
    print(f"URL scannée : {qr_url}")

    # Étape 2 : Extraire le nom du vérificateur et la clé secrète
    issuer, secret = extract_info_from_url(qr_url)
    print(f"Nom du vérificateur : {issuer}")
    print(f"Clé secrète : {secret}")

    # Étape 3 : Générer le code de vérification
    verification_code = generate_verification_code(secret)
    if verification_code:
        print(f"Code de vérification : {verification_code}")
    else:
        print("Impossible de générer le code de vérification.")
else:
    print("Aucun code QR trouvé.")
