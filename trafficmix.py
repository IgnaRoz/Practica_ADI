    
import hashlib
import unittest
import requests

ADMIN_USERNAME = 'administrator'
ADMIN_PASS_HASH = hashlib.sha256('admin'.encode()).hexdigest()
ADMIN_AUTH_CODE = hashlib.sha256(f'{ADMIN_USERNAME}{ADMIN_PASS_HASH}'.encode()).hexdigest()
USER_USERNAME = 'user'
USER_PASS_HASH = hashlib.sha256('userpass'.encode()).hexdigest()
USER_PASS_CODE = hashlib.sha256(f'{USER_USERNAME}{USER_PASS_HASH}'.encode()).hexdigest()
URI_AUTH = 'http://miservicio:30080/auth/auth/v1'
#URI_AUTH = 'http://192.168.1.100:3000/auth/v1'
URI_TOKEN = 'http://miservicio:30080/token/api/v1'
#URI_TOKEN = 'http://192.168.1.100:3002/api/v1'

class TestTrafficMix(unittest.TestCase):
    def test_traffic_mix_auth(self):
        
        response = requests.put(URI_TOKEN + "/token", json={"username": ADMIN_USERNAME, "pass_hash": ADMIN_PASS_HASH}, timeout=5)
        self.assertEqual(response.status_code, 200)
        
        token_admin =response.json()["token"]
        #comprobar que se ha creado el token
        response = requests.get(URI_TOKEN+f"/token/{token_admin}",timeout=5)
        self.assertEqual(response.status_code, 200)
        #comprobar que el username de la respuesta
        self.assertEqual(response.json()["username"], ADMIN_USERNAME)
        #comprobar que dentro del array roles se encuentra el rol admin
        self.assertIn("admin", response.json()["roles"])

        #eliminamos previamente el usuario nacho(sin comprobar si existe solo para asegurarnos que no existe)
        response = requests.delete(URI_AUTH + f"/user/nacho",headers={"Content-Type": "application/json","AuthToken":token_admin}, timeout=10)
        # Creamos un nuevo usuario nacho
        response = requests.put(URI_AUTH + "/user",headers={"Content-Type": "application/json","AuthToken":token_admin}, json={"username": "nacho", "password": "nachopass", 'role':'user'} )
        self.assertIn(response.status_code, [200, 201,204])
        # Obtenemos el usuario nacho
        response = requests.get(URI_AUTH + "/user/nacho",headers={"Content-Type": "application/json","AuthToken":token_admin}, timeout=5)
        self.assertEqual(response.status_code, 200)
        #comprobamos que el json de respuesta tiene el username nacho y dentro del array roles el rol user
        self.assertEqual(response.json()["username"], "nacho")
        self.assertIn("user", response.json()["role"])

        #Creamos un token para el usuario nacho
        response = requests.put(URI_TOKEN + "/token", json={"username":    "nacho", "pass_hash": USER_PASS_HASH}, timeout=5)
        self.assertEqual(response.status_code, 200)
        token_nacho =response.json()["token"]

        # Modificamos el usuario nacho con la password supernachopass y el rol de admin
        response = requests.post(URI_AUTH + "/user/nacho",headers={"Content-Type": "application/json","AuthToken":token_nacho}, json={"username": "nacho", "password": "supernachopass", 'role':'admin'} )
        self.assertIn(response.status_code, [200, 201,204])
        # Obtenemos el usuario nacho
        response = requests.get(URI_AUTH + "/user/nacho",headers={"Content-Type": "application/json","AuthToken":token_nacho}, timeout=5)
        self.assertEqual(response.status_code, 200)
        #comprobamos que el json de respuesta tiene el username nacho y dentro del array roles el rol admin
        self.assertEqual(response.json()["username"], "nacho")
        self.assertIn("admin", response.json()["roles"])

        # Verificamos el usuario nacho con la password supernachopass
        nacho_pass_hash = hashlib.sha256('supernachopass'.encode()).hexdigest()
        nacho_pass_code = hashlib.sha256(f'nacho{nacho_pass_hash}'.encode()).hexdigest()
        response = requests.get(URI_AUTH + f"/is_authorized/{nacho_pass_code}", timeout=5)
        self.assertEqual(response.status_code, 200)
        #comprobamos que el rol de admin esta en roles
        self.assertIn("admin", response.json()["roles"])

        # Borramos el usuario nacho
        response = requests.delete(URI_AUTH + "/user/nacho",headers={"Content-Type": "application/json","AuthToken":token_nacho}, timeout=5)
        self.assertEqual(response.status_code, 204)



if __name__ == '__main__':
    t=TestTrafficMix()
    t.test_traffic_mix_auth()