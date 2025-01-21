from typing import List
import requests
from requests_toolbelt import MultipartEncoder

def _assert_status_ok_(status_code):
    if status_code not in [200, 201, 204, 400, 401, 404]:
        raise RuntimeError('Unknown response from API')
    else:
        return True

class Client:
    def __init__(self, root_api: str) -> None:
        self.root_api = root_api

    def put_blob(self, auth_token: str, name: str, writer: List[str], file_path: str) -> None:
        with open(file_path, 'rb') as file:
            multipart = MultipartEncoder(
                fields={
                    'name': name,
                    'writable_by': ', '.join(writer),
                    'owner': writer[0],
                    'file': (file_path, file, 'application/octet-stream')
                }
            )

            response = requests.put(
                f'{self.root_api}/blob',
                headers={
                    'AuthToken': auth_token,
                    'Content-Type': multipart.content_type
                },
                data = multipart
            )

        _assert_status_ok_(response.status_code)
        print(f'{response.status_code}, {response.text}')
        return response.text.split(': ')[1].strip()

    def delete_blob(self, blob_id: str, auth_token: str) -> None:
        response = requests.delete(
            f'{self.root_api}/blob/{blob_id}',
            headers = {'AuthToken': auth_token}
        )
        if _assert_status_ok_(response.status_code):
            print(f'Status Code Delete_Data Request: {response.status_code}')

    def get_blob(self, blob_id: str, auth_token: str) -> None:
        response = requests.get(
            f'{self.root_api}/blob/{blob_id}/data',
            headers = {'AuthToken': auth_token}
        )
        _assert_status_ok_(response.status_code)
        file = response.content
        print(f'{response.status_code}, File: {file}')

    def post_patch_blob(self, blob_id: str, auth_token: str, file_path: str, request: str) -> None:
        if request == 'POST':
            with open(file_path, 'rb') as file:
                multipart = MultipartEncoder(
                    fields={
                        'file': (file_path, file, 'application/octet-stream')
                    }
                )

                response = requests.post(
                    f'{self.root_api}/blob/{blob_id}/data',
                    headers={
                        'AuthToken': auth_token,
                        'Content-Type': multipart.content_type
                    },
                    data = multipart
                )

            _assert_status_ok_(response.status_code)
            print(f'{response.status_code}, {response.text}')

        elif request == 'PATCH':
            with open(file_path, 'rb') as file:
                multipart = MultipartEncoder(
                    fields={
                        'file': (file_path, file, 'application/octet-stream')
                    }
                )
                
                response = requests.patch(
                    f'{self.root_api}/blob/{blob_id}/data',
                    headers={
                        'AuthToken': auth_token,
                        'Content-Type': multipart.content_type
                    },
                    data = multipart
                )
            _assert_status_ok_(response.status_code)
            print(f'{response.status_code}, {response.text}')

        else:
            raise ValueError('Unknown request')

    def get_roles_blob(self, blob_id: str, auth_token: str) -> None:
        response = requests.get(
            f'{self.root_api}/blob/{blob_id}/roles',
            headers = {'AuthToken': auth_token},)

        _assert_status_ok_(response.status_code)
        if response.status_code == 200:
            print(f'{response.status_code}, data: {response.json()}')
        else:
            print(f'{response.status_code}, {response.text}')

    def post_patch_roles_blob(self, blob_id: str, auth_token:str ,new_roles: List[str], request: str) -> None:
        if request == 'PATCH':
            response = requests.patch(
                f'{self.root_api}/blob/{blob_id}/roles',
                headers = {'AuthToken': auth_token},
                json = {
                    'writable_by': new_roles
                }
            )
            _assert_status_ok_(response.status_code)
            print(f'Status Code Patch_Name Request: {response.status_code}')

        if request == 'POST':
            response = requests.post(
                f'{self.root_api}/blob/{blob_id}/roles',
                headers = {'AuthToken': auth_token},
                json = {
                    'writable_by': new_roles
                }
            )
            _assert_status_ok_(response.status_code)
            print(f'Status Code Post_Name Request: {response.status_code}')

    def get_name_blob(self, blob_id: str, auth_token: str) -> None:
        response = requests.get(
            f'{self.root_api}/blob/{blob_id}/name',
            headers = {'AuthToken': auth_token},)
        _assert_status_ok_(response.status_code)
        if response.status_code == 200:
            print(f'{response.status_code}, name: {response.text}')
        else:
            print(f'{response.status_code}, {response.text}')

    def post_patch_names_blob(self, blob_id: str, auth_token: str, name: str, request: str) -> None:
        if request == 'PATCH':
            response = requests.patch(
                f'{self.root_api}/blob/{blob_id}/name',
                headers = {'AuthToken': auth_token},
                json = {
                    'name': name
                }
            )
            _assert_status_ok_(response.status_code)
            print(f'{response.status_code}.{response.text}')

        if request == 'POST':
            response = requests.post(
                f'{self.root_api}/blob/{blob_id}/name',
                headers = {'AuthToken': auth_token},
                json = {
                    'name': name
                }
            )
            _assert_status_ok_(response.status_code)
            print(f'{response.status_code}, {response.text}')
if __name__ == '__main__':
    client = Client('http://192.168.56.110/api/v1')
    writted_by = ['admin', 'Paco', 'Antonio']
    blob_id = client.put_blob('token_for_admin', 'blob_2', writted_by, "hola.txt")
    # print(f'Blob ID: {blob_id}')
    # client.delete_blob(blob_id, 'token_for_admin')
    #client.get_blob('04e985e7a5e0f5b5', 'token_for_admin')
    #client.post_patch_blob('69093d05cb466d29', 'token_for_admin', '/home/sergio/Escritorio/prueba2.txt', 'POST')
    #client.post_patch_blob('36ef169ddf93b54d', 'token_for_admin', '/home/sergio/Escritorio/prueba.txt', 'PATCH')
    #client.get_roles_blob('69093d05cb466d29', 'token_for_admin')
    #client.post_patch_roles_blob('69093d05cb466d29', 'token_for_admin' ,['jesus', 'fran', 'jaime'], 'POST')
    #client.post_patch_roles_blob('06db2be4c3c10c78', ['paco', 'admin', 'antonio'], 'PATCH')
    #client.get_name_blob('69093d05cb466d29', 'token_for_admin')
    #client.post_patch_names_blob('69093d05cb466d29', 'token_for_admin', 'blob_3', 'POST')