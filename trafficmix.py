    
import hashlib
import unittest
import requests
import clientblob
import os

ADMIN_USERNAME = 'administrator'
ADMIN_PASS_HASH = hashlib.sha256('admin'.encode()).hexdigest()
ADMIN_AUTH_CODE = hashlib.sha256(f'{ADMIN_USERNAME}{ADMIN_PASS_HASH}'.encode()).hexdigest()
USER_USERNAME = 'user'
USER_PASS_HASH = hashlib.sha256('userpass'.encode()).hexdigest()
USER_PASS_CODE = hashlib.sha256(f'{USER_USERNAME}{USER_PASS_HASH}'.encode()).hexdigest()
#URI_AUTH = 'http://miservicio:30080/auth/auth/v1'
#URI_AUTH = 'http://10.0.2.8/auth/v1'
URI_AUTH = 'http://192.168.56.110/auth/v1'
#URI_TOKEN = 'http://miservicio:30080/token/api/v1'
#URI_TOKEN = 'http://10.0.2.8/api/v1'
URI_TOKEN = 'http://192.168.56.110/api/v1'
URI_BLOB = 'http://192.168.56.110/api/v1'

class TestTrafficMix(unittest.TestCase):
    def test_traffic_mix_auth(self):
        print("Test traffic mix")
        print(f"Creando Token para el usuario {ADMIN_USERNAME}, con pass_hash {ADMIN_PASS_HASH}")
        print(f"PUT {URI_TOKEN}/token , json={{'username': {ADMIN_USERNAME}, 'pass_hash': {ADMIN_PASS_HASH}}}")
        response = requests.put(URI_TOKEN + "/token", json={"username": ADMIN_USERNAME, "pass_hash": ADMIN_PASS_HASH}, timeout=5)
        print(f"Respuesta: {response.status_code}, {response.json()} \n")
        self.assertEqual(response.status_code, 200)

        token_admin =response.json()["token"]
        #comprobar que se ha creado el token
        print(f"Pedimos informacion del token {token_admin}")
        print(f"GET {URI_TOKEN}/token/{token_admin}")
        response = requests.get(URI_TOKEN+f"/token/{token_admin}",timeout=5)
        print(f"Respuesta: {response.status_code}, {response.json()} \n")
        self.assertEqual(response.status_code, 200)
        #comprobar que el username de la respuesta
        self.assertEqual(response.json()["username"], ADMIN_USERNAME)
        #comprobar que dentro del array roles se encuentra el rol admin
        self.assertIn("admin", response.json()["roles"])

        #eliminamos previamente el usuario nacho(sin comprobar si existe solo para asegurarnos que no existe)
        print(f"Eliminamos prviamente el usuario nacho")
        response = requests.delete(URI_AUTH + f"/user/nacho",headers={"Content-Type": "application/json","AuthToken":token_admin}, timeout=10)
        # Creamos un nuevo usuario nacho
        print(f"Creamos un nuevo usuario nacho")
        print(f"PUT {URI_AUTH}/user , json={{'username': 'nacho', 'password': 'nachopass', 'role':'user'}}")
        response = requests.put(URI_AUTH + "/user",headers={"Content-Type": "application/json","AuthToken":token_admin}, json={"username": "nacho", "password": "nachopass", 'role':'user'} )
        print(f"Respuesta: {response.status_code} \n")
        self.assertIn(response.status_code, [200, 201,204])

        # Obtenemos el usuario nacho
        print(f"Obtenemos el usuario nacho")
        print(f"GET {URI_AUTH}/user/nacho")
        response = requests.get(URI_AUTH + "/user/nacho",headers={"Content-Type": "application/json","AuthToken":token_admin}, timeout=5)
        print(f"Respuesta: {response.status_code}, {response.json()} \n")
        self.assertEqual(response.status_code, 200)
        #comprobamos que el json de respuesta tiene el username nacho y dentro del array roles el rol user
        self.assertEqual(response.json()["username"], "nacho")
        self.assertIn("user", response.json()["role"])

        #Creamos un token para el usuario nacho
        print(f"Creando Token para el usuario nacho, con password 'nachopass' y con pass_hash {hashlib.sha256('nachopass'.encode()).hexdigest()}")
        pass_hash = hashlib.sha256('nachopass'.encode()).hexdigest()
        print(f"PUT {URI_TOKEN}/token , json={{'username': 'nacho', 'pass_hash': {pass_hash}}}")
        response = requests.put(URI_TOKEN + "/token", json={"username":    "nacho", "pass_hash": pass_hash}, timeout=5)
        print(f"Respuesta: {response.status_code}, {response.json()} \n")
        self.assertEqual(response.status_code, 200)
        token_nacho =response.json()["token"]

        # Modificamos el usuario nacho con la password supernachopass y el rol de admin
        print(f"Modificamos el usuario nacho con la password supernachopass y el rol de admin")
        print(f"POST {URI_AUTH}/user/nacho , json={{'username': 'nacho', 'password': 'supernachopass', 'role':'admin'}}")
        response = requests.post(URI_AUTH + "/user/nacho",headers={"Content-Type": "application/json","AuthToken":token_nacho}, json={"username": "nacho", "password": "supernachopass", 'role':'admin'} )
        print(f"Respuesta: {response.status_code} \n")
        self.assertIn(response.status_code, [200, 201,204])
        # Obtenemos el usuario nacho
        print(f"Obtenemos de nuevo el usuario nacho")
        print(f"GET {URI_AUTH}/user/nacho") 
        response = requests.get(URI_AUTH + "/user/nacho",headers={"Content-Type": "application/json","AuthToken":token_nacho}, timeout=5)
        print(f"Respuesta: {response.status_code}, {response.json()} \n")
        self.assertEqual(response.status_code, 200)
        #comprobamos que el json de respuesta tiene el username nacho y dentro del array roles el rol admin
        self.assertEqual(response.json()["username"], "nacho")
        self.assertIn("admin", response.json()["role"])

        # Verificamos el usuario nacho con la password supernachopass
        print(f"Verificamos el usuario nacho con la password supernachopass")
        nacho_pass_hash = hashlib.sha256('supernachopass'.encode()).hexdigest()
        nacho_pass_code = hashlib.sha256(f'nacho{nacho_pass_hash}'.encode()).hexdigest()
        print(f"GET {URI_AUTH}/is_authorized/{nacho_pass_code}")
        response = requests.get(URI_AUTH + f"/is_authorized/{nacho_pass_code}", timeout=5)
        print(f"Respuesta: {response.status_code} \n")
        self.assertEqual(response.status_code, 200)
        #comprobamos que el rol de admin esta en roles
        self.assertIn("admin", response.json()["roles"])

        


        # Probamos el servicio de blobs

        #Creamos un archivo hola.txt
        print("Creamos un archivo hola.txt, con el contenido 'Hola Mundo, esto es un blob'")
        with open("hola.txt", "w") as f:
            f.write("Hola Mundo, esto es un blob")
        #Creamos un blob con el archivo hola.txt
        print("Creamos un blob con el archivo hola.txt")

        client = clientblob.Client(URI_BLOB)
        writted_by = ['admin', 'Paco', 'Antonio']
        print(f"PUT {URI_TOKEN}/blob , json={{'name': 'blob_admin', 'writable_by': {writted_by}, 'filename': 'hola.txt'}}")
        blob_id = client.put_blob(token_admin, 'blob_admin', writted_by, "hola.txt")
        #Borramos el archivo hola.txt
        print("Borramos el archivo original hola.txt")
        os.remove("hola.txt")
        #obtenemos el blob
        print(f"Obtenemos el blob {blob_id}")
        print(f"GET {URI_TOKEN}/blob/{blob_id}")
        client.get_blob(blob_id, token_admin)
        print()
        #obtenemos los roles del blob
        print(f"Obtenemos los roles del blob {blob_id}")
        print(f"GET {URI_TOKEN}/blob/{blob_id}/roles")
        client.get_roles_blob(blob_id, token_admin)
        print()

        #obtenemos el nombre del blob
        print(f"Obtenemos el nombre del blob {blob_id}")
        print(f"GET {URI_TOKEN}/blob/{blob_id}/name")
        client.get_name_blob(blob_id, token_admin)
        print()

        #borramos el blob
        print(f"Borramos el blob {blob_id}")
        print(f"DELETE {URI_TOKEN}/blob/{blob_id}")
        client.delete_blob(blob_id, token_admin)
        print()


        # Borramos el usuario nacho
        print(f"Borramos el usuario nacho")
        print(f"DELETE {URI_AUTH}/user/nacho")
        response = requests.delete(URI_AUTH + "/user/nacho",headers={"Content-Type": "application/json","AuthToken":token_nacho}, timeout=5)
        print(f"Respuesta: {response.status_code} \n")
        self.assertEqual(response.status_code, 204)



if __name__ == '__main__':
    t=TestTrafficMix()
    t.test_traffic_mix_auth()
