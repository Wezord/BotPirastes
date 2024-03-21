import gspread
from gspread_formatting import *
from oauth2client.service_account import ServiceAccountCredentials
from google.auth import exceptions

# Remplacez ces informations par vos propres informations d'identification et l'ID de votre feuille de calcul
credentials_path = r'C:\Users\Wezord\Desktop\Bot\BotV2\perso\key.json'

# Création de l'authentification
gc = gspread.service_account(filename=credentials_path)

# Obtention de la référence de la feuille de calcul

scope = ["https://spreadsheets.google.com/feeds",
		 "https://www.googleapis.com/auth/spreadsheets",
		 "https://www.googleapis.com/auth/drive.file",
		 "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("key.json",scope)
client = gspread.authorize(creds)

client.list_spreadsheet_files()

def getLen(sheet):
    spreadsheet_id = ""
    if sheet == "CHICHA":
        spreadsheet_id = '1FvE61yQ1IWBnpFDgSghgLSiVfUI5_UAtK_VJb42P2Fs'
    elif sheet == "TAXI":
        spreadsheet_id = "1xQJC5gK0gP8m-CaXDyS04akR2jC0vj7SgNLZowjeSEE"
    elif sheet == "WRAP":
        spreadsheet_id = "1Tdk_LPgkdIeQLIVJaOalZFzSA_LVDZ3q0E6iLG4-RJ4"
    elif sheet == "PERSONNE":
        spreadsheet_id = "163-piIwX5kxvpZYHI_I4y0O36xhnZ5VRmaqmd4Rlbfg"
    elif sheet == "GAUFRE":
        spreadsheet_id = "1nok4QFVZjyq0HJi_KzPrhym35S9kSmmrdaY31ImdIaA"
    elif sheet == "CREPE":
        spreadsheet_id = "1by-oXfDLO9jeWCEem32Y0lA2ii9e0qw4LsnIOxybdAo"
    elif sheet == "PANCAKE":
        spreadsheet_id = "14H6W6sGlBKlqZ7b9EFPHiXk7yO90_tyUBougYALZ-9M"
    elif sheet == "PATES":
        spreadsheet_id = "1wqJwJVGZQtAPCdD4Yyz1lorSjET7JZUTFzBoKUmI8Kc"
    elif sheet == "PETIT":
        spreadsheet_id = "1lxsc0l0VTdNX0cBSaj301XvkPrei_vXIyNWBCVaMyNk"

    try:
        spreadsheet = gc.open_by_key(spreadsheet_id)
    except Exception as e:
        print(e)
        print("Probleme dans le nom de l'allo")
        return
    worksheet = spreadsheet.get_worksheet(0)
    values = worksheet.get_all_values()
    return len(values) + 1

def endAllo(sheet, ligne):
    spreadsheet_id = ""
    if sheet == "CHICHA":
        spreadsheet_id = '1FvE61yQ1IWBnpFDgSghgLSiVfUI5_UAtK_VJb42P2Fs'
    elif sheet == "TAXI":
        spreadsheet_id = "1xQJC5gK0gP8m-CaXDyS04akR2jC0vj7SgNLZowjeSEE"
    elif sheet == "WRAP":
        spreadsheet_id = "1Tdk_LPgkdIeQLIVJaOalZFzSA_LVDZ3q0E6iLG4-RJ4"
    elif sheet == "PERSONNE":
        spreadsheet_id = "163-piIwX5kxvpZYHI_I4y0O36xhnZ5VRmaqmd4Rlbfg"
    elif sheet == "GAUFRE":
        spreadsheet_id = "1nok4QFVZjyq0HJi_KzPrhym35S9kSmmrdaY31ImdIaA"
    elif sheet == "CREPE":
        spreadsheet_id = "1by-oXfDLO9jeWCEem32Y0lA2ii9e0qw4LsnIOxybdAo"
    elif sheet == "PANCAKE":
        spreadsheet_id = "14H6W6sGlBKlqZ7b9EFPHiXk7yO90_tyUBougYALZ-9M"
    elif sheet == "PATES":
        spreadsheet_id = "1wqJwJVGZQtAPCdD4Yyz1lorSjET7JZUTFzBoKUmI8Kc"
    elif sheet == "PETIT":
        spreadsheet_id = "1lxsc0l0VTdNX0cBSaj301XvkPrei_vXIyNWBCVaMyNk"

    try:
        spreadsheet = gc.open_by_key(spreadsheet_id)
    except Exception as e:
        print(e)
        print("Probleme dans le nom de l'allo")
        return

    worksheet = spreadsheet.get_worksheet(0)
    worksheet.format("G" + ligne, {"backgroundColor":  {"red": 1.0, "green": 0.0, "blue": 0.0}})

def openAllo(sheet, ligne):
    spreadsheet_id = ""
    if sheet == "CHICHA":
        spreadsheet_id = '1FvE61yQ1IWBnpFDgSghgLSiVfUI5_UAtK_VJb42P2Fs'
    elif sheet == "TAXI":
        spreadsheet_id = "1xQJC5gK0gP8m-CaXDyS04akR2jC0vj7SgNLZowjeSEE"
    elif sheet == "WRAP":
        spreadsheet_id = "1Tdk_LPgkdIeQLIVJaOalZFzSA_LVDZ3q0E6iLG4-RJ4"
    elif sheet == "PERSONNE":
        spreadsheet_id = "163-piIwX5kxvpZYHI_I4y0O36xhnZ5VRmaqmd4Rlbfg"
    elif sheet == "GAUFRE":
        spreadsheet_id = "1nok4QFVZjyq0HJi_KzPrhym35S9kSmmrdaY31ImdIaA"
    elif sheet == "CREPE":
        spreadsheet_id = "1by-oXfDLO9jeWCEem32Y0lA2ii9e0qw4LsnIOxybdAo"
    elif sheet == "PANCAKE":
        spreadsheet_id = "14H6W6sGlBKlqZ7b9EFPHiXk7yO90_tyUBougYALZ-9M"
    elif sheet == "PATES":
        spreadsheet_id = "1wqJwJVGZQtAPCdD4Yyz1lorSjET7JZUTFzBoKUmI8Kc"
    elif sheet == "PETIT":
        spreadsheet_id = "1lxsc0l0VTdNX0cBSaj301XvkPrei_vXIyNWBCVaMyNk"

    try:
        spreadsheet = gc.open_by_key(spreadsheet_id)
    except Exception as e:
        print(e)
        print("Probleme dans le nom de l'allo")
        return

    worksheet = spreadsheet.get_worksheet(0)
    worksheet.format("G" + ligne, {"backgroundColor": {"red": 0.0, "green": 1.0, "blue": 0.0}})

def ecrire(sheet, valeurs):

    spreadsheet_id = ""
    if sheet == "CHICHA":
        spreadsheet_id = '1FvE61yQ1IWBnpFDgSghgLSiVfUI5_UAtK_VJb42P2Fs'
    elif sheet == "TAXI":
        spreadsheet_id = "1xQJC5gK0gP8m-CaXDyS04akR2jC0vj7SgNLZowjeSEE"
    elif sheet == "WRAP":
        spreadsheet_id= "1Tdk_LPgkdIeQLIVJaOalZFzSA_LVDZ3q0E6iLG4-RJ4"
    elif sheet == "PERSONNE":
        spreadsheet_id = "163-piIwX5kxvpZYHI_I4y0O36xhnZ5VRmaqmd4Rlbfg"
    elif sheet == "GAUFRE":
        spreadsheet_id = "1nok4QFVZjyq0HJi_KzPrhym35S9kSmmrdaY31ImdIaA"
    elif sheet == "CREPE":
        spreadsheet_id = "1by-oXfDLO9jeWCEem32Y0lA2ii9e0qw4LsnIOxybdAo"
    elif sheet == "PANCAKE":
        spreadsheet_id = "14H6W6sGlBKlqZ7b9EFPHiXk7yO90_tyUBougYALZ-9M"
    elif sheet == "PATES":
        spreadsheet_id = "1wqJwJVGZQtAPCdD4Yyz1lorSjET7JZUTFzBoKUmI8Kc"
    elif sheet == "PETIT":
        spreadsheet_id = "1lxsc0l0VTdNX0cBSaj301XvkPrei_vXIyNWBCVaMyNk"

    try:
        spreadsheet = gc.open_by_key(spreadsheet_id)
    except Exception as e:
        print(e)
        print("Probleme dans le nom de l'allo")
        return

    worksheet = spreadsheet.get_worksheet(0)

    # Récupération du nombre de lignes
    values = worksheet.get_all_values()
    row_index = len(values) + 1

    print("Nombre de ligne "  + str(row_index))

    sheet_id = 0

    # Liste des valeurs à mettre à jour dans la ligne
    new_values = valeurs

    # Construction de la requête batchUpdate
    request = {
        "updateCells": {
            "range": {"sheetId": sheet_id, "startRowIndex": row_index - 1, "endRowIndex": row_index,
                      "startColumnIndex": 0},
            "rows": [{"values": [{"userEnteredValue": {"stringValue": value}} for value in new_values]}],
            "fields": "*"
        }
    }

    # Exécution de batchUpdate
    try:
        spreadsheet.batch_update({"requests": [request]})
        print(f"Ligne {row_index} mise à jour avec succès.")
    except exceptions.GoogleAuthError as e:
        print(f"Erreur d'authentification : {e}")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

    return row_index