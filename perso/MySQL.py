import mysql.connector

host = '193.203.168.6'
port = 3306
user = 'u760277800_ladminpirates'
password = 'Fuckmaloleroidespirates44$'
database = 'u760277800_allo_pirastes'
raise_on_warnings = True

connexion = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        raise_on_warnings=raise_on_warnings
    )

curseur = connexion.cursor()


if connexion.is_connected():
    curseur = connexion.cursor()

    print("2")

    requete_select = "INSERT INTO allo (Nom,Prenom, Chambre, Adresse, Nom_Allo, Heure_validation, Etat) VALUES (%s,%s,%s,%s,%s,%s,%s)"
    valeurs = ("Test1", "Test2", "Test3", "Test4", "Test5", "Test6", 0)

    curseur.execute(requete_select, valeurs)

    print("3")
    connexion.commit()
    curseur.close()
    connexion.close()
