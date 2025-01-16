
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

class test(unittest.TestCase):

    #Comprobar status de los servicios
    def test_service_token(self):
        # Test the service
        response = requests.get(URI_TOKEN + "/status", timeout=5)
        self.assertIn(response.status_code, [200, 204])

    def test_service_auth(self):
        # Test the service
        response = requests.get(URI_AUTH + "/status", timeout=5)
        self.assertIn(response.status_code, [200, 204])






    def test_add_user(self):
        # Test the service
        response = requests.post(URI_AUTH + "/user",headers={"Content-Type": "application/json","AuthToken":"token_for_user"}, json={"username": USER_USERNAME, "password": "userpass", 'role':'user'} , timeout=5)
        self.assertIn(response.status_code, [200, 201,204])
        #Comprobamos que la respuesta es un json con el username del usuario y el rol user
        self.assertEqual(response.json()["username"], USER_USERNAME)
        self.assertEqual(response.json()["role"], "user")


    def test_get_user(self):
        # Test the service
        response = requests.get(URI_AUTH + f"/user/{USER_USERNAME}",headers={"Content-Type": "application/json","AuthToken":"token_for_user"}, timeout=5)
        self.assertIn(response.status_code, [200, 204])


    #Tests del servicio de token
    def test_make_token(self):
        # Test the service
        response = requests.put(URI_TOKEN + "/token", json={"username":    ADMIN_USERNAME, "pass_hash": ADMIN_PASS_HASH}, timeout=5)
        self.assertEqual(response.status_code, 200)

        token =response.json()["token"]
        #comprobar que se ha creado el token
        response = requests.get(URI_TOKEN+f"/token/{token}",timeout=5)
        self.assertEqual(response.status_code, 200)
        #comprobar que el username de la respuesta
        self.assertEqual(response.json()["username"], ADMIN_USERNAME)
        #comprobar que dentro del array roles se encuentra el rol admin
        self.assertIn("admin", response.json()["roles"])
