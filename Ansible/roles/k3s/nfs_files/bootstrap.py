"""modulos para crear la base de datos y el usuario administrador"""
import os
import sqlite3
from hashlib import sha256

def create_database(db_path:str):
    """
    funcion para crear la base de datos
    """
    username = 'administrator'
    #sacamos la variable de entorno para la contraseña
    password = os.getenv('ADMINPASS')
    password = sha256(password.encode()).hexdigest()
    role = 'admin'
    authcode = sha256((username + password).encode()).hexdigest()

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    request = "CREATE TABLE users"
    request += "(username TEXT PRIMARY KEY, password TEXT NOT NULL"
    request += ", role TEXT NOT NULL, authCode TEXT NOT NULL)"
    cursor.execute(request)
    #creamos el usuario incial
    cursor.execute("INSERT INTO users (username, password, role, authCode) VALUES (?, ?, ?, ?)"
                   ,(username, password, role, authcode))
    conn.commit()
    conn.close()


def bootstrap():
    """
    funcion para crear la base de datos
    """
    db_folder = os.getenv('STORAGE_FOLDER')
    #miramos si no existe la carpeta users
    if not os.path.exists(db_folder):
        os.makedirs(db_folder)

    #miramos si no existe el archivo de la base de datos
    db_path = os.path.join(db_folder, 'users.db')
    if not os.path.exists(db_path):
        create_database(db_path)

if __name__ == '__main__':
    bootstrap()
