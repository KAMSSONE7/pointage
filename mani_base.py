import mysql.connector
from mysql.connector import Error
from datetime import datetime

try:
    # Connexion à la base de données
    connection = mysql.connector.connect(
        host='switchback.proxy.rlwy.net',  # adresse de serveur MySQL
        database='railway',  # base de données à utiliser
        user='root',  # nom d'utilisateur MySQL
        password='IowFRbmQYlvxWwLrMLalevEQqhQtWvYN',  # mot de passe MySQL
        port=55321,  # port MySQL
        charset='utf8mb4'
    )
    
    if connection.is_connected():
        cursor = connection.cursor()
        # Requête SQL pour insérer un nouveau etudiant
        TIMESTAMP = datetime.now()
        cursor.execute("INSERT INTO Presence_ens VALUE (%s,%s,%s,%s,%s,%s)",('ENS001',1,datetime.now(),TIMESTAMP,'20:14:43','effectue'))
        cursor.execute("COMMIT;")
        cursor.fetchall()
        connection.commit()

except Error as e:
    print(f"Erreur lors de la connexion à MySQL: {e}")

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("Connexion MySQL fermée")   
        
# list_administration=[]
# for i in range(len(list_ad)):
#     ch=str(list_ad[i][1])+' '+str( list_ad[i][2])
#     list_administration.append(ch)
        
        
# list_etudiant=[]
# for i in range(len(list_et)):
#     ch=str(list_et[i][3])+' '+str( list_et[i][4])
#     list_etudiant.append(ch)

# name='KADJO ALLOUAN MOISE BIENVENUE'
# def affiche():
#     if (name in list_etudiant):
#         index=list_etudiant.index(name)
#         '''
#         list_et[i][j] : pour selectionner un etudiant a position {i} et 
#         la {j}ieme colonne(proprietes) de l'etudiant en question
        
#         '''
#         niveau= list_et[index][5]
#         email= list_et[index][6]
#         numero=list_et[2][7] 
#         adresse=list_et[index][8]
#         print(f"Nom & Prenoms :{name}  Niveau :{niveau}  Numero :{numero}  Email :{email}  Adresse :{adresse}")    
    

# affiche()
# # Exemple d'utilisation
# print(f"{list_etudiant} ")

# print(list_ad)    
