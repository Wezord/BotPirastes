import qrcode
import webbrowser

def generer_qr_code(numero_telephone, nom_contact):
    # Créer le lien WhatsApp avec le numéro de téléphone et le nom
    url_whatsapp_api = f'https://api.whatsapp.com/send?phone={numero_telephone}&text=Bonjour%20{nom_contact}'

    # Générer le QR Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url_whatsapp_api)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Sauvegarder le QR Code dans un fichier
    img.save("qr_code_whatsapp.png")

    # Ouvrir le QR Code dans le navigateur
    webbrowser.open("qr_code_whatsapp.png")

# Exemple d'utilisation
generer_qr_code("757690893", "Pir'As'tes")