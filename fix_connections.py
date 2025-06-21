import re

# Chemin du fichier à modifier
file_path = r'c:\Users\HP\Desktop\PROGETAGLM - Copie 3\page_boite_de_reception.py'

# Lire le contenu du fichier
with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()

# Remplacer les connexions directes par get_db_connection()
pattern = r"connection\s*=\s*mysql\.connector\.connect\([^)]*\)"
replacement = "connection = get_db_connection()"
new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# Écrire le contenu modifié dans le fichier
with open(file_path, 'w', encoding='utf-8') as file:
    file.write(new_content)

print("Les connexions directes ont été remplacées par get_db_connection().")
