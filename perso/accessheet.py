import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds",
		 "https://www.googleapis.com/auth/spreadsheets",
		 "https://www.googleapis.com/auth/drive.file",
		 "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("key.json",scope)
client = gspread.authorize(creds)

client.list_spreadsheet_files()

sheet = client.open("Personne").sheet1

def getSheet():
	return sheet
def new_id():
	return len(sheet.col_values(1))

def set_id(id):
	sheet.update_cell(id+1,1,id)

def set_numero(id,numero):
	sheet.update_cell(id+1,2,numero)
def set_prenom(id,prenom):
	sheet.update_cell(id+1,3,prenom)

def set_nom(id,nom):
	sheet.update_cell(id+1,4,nom)

def set_chambre(id,chambre):
	sheet.update_cell(id+1,4,chambre)

def set_annee(id,annee):
	sheet.update_cell(id+1,6,annee)

def set_points(id, points):
	sheet.update_cell(id+1, 5, points)

def set_creation_state(id, state):
	sheet.update_cell(id+1, 7, state)
def get_creation_state(id):
	print("state",sheet.col_values(7)[id])
	return sheet.col_values(7)[id]

def get_chambre(id):
	return sheet.col_values(4)[id]

def get_allo_state(id):
	return sheet.col_values(9)[id]

def set_allo_state(id,state):
	sheet.update_cell(id + 1, 9, state)

def get_adresse(id):
	return sheet.col_values(6)[id]

def get_prenom(id):
	return sheet.col_values(3)[id]

def set_adresse(id,adresse):
	sheet.update_cell(id + 1, 6, adresse)

def set_actual_state(id, state):
	sheet.update_cell(id + 1, 8, state)

def get_actual_state(id):
	return sheet.col_values(8)[id]

def is_numero(numero):
	col = sheet.col_values(2)
	ind = 0
	for num in col:
		ind = ind + 1
		if ("+"+num) == numero:
			return ind-1
	return False