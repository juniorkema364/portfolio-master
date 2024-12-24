import pyotp

# La clé secrète extraite de l'URL
secret = "WCD4T77CACFNUJIXRQ4ITSZSL2VNKQ3M"

# Créer un objet TOTP avec la clé secrète
totp = pyotp.TOTP(secret)

# Générer le code de vérification actuel
verification_code = totp.now()

print(f"Code de vérification : {verification_code}")
