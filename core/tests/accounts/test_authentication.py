from accounts.models import User
from rest_framework.test import APITestCase


class SetupBase(APITestCase):
    # Se crea un usuario para ejecutar los tests en el
    def setUp(self):
        self.user = User.objects.create_user('test_user', 'test_user@mail.com', '123456')
        result = self.client.post('/api/token/', {'email': 'test_user@mail.com', 'password': '123456'})


class AuthTestCase(SetupBase):

    # Se comprueba si al momento de autenticar un usuario se recibe un access token en result.data
    def test_auth(self):
        result = self.client.post('/api/token/', {'email': 'test_user@mail.com', 'password': '123456'})
        assert result.status_code == 200
        assert 'access' in result.data

    # Se comprueba que el token que se recibe al autenticarse funciona
    def test_valid_token(self):
        result = self.client.post('/api/token/', {'email': 'test_user@mail.com', 'password': '123456'})
        token = result.data['access']
        user_result = self.client.get('/api/v1/users/', HTTP_AUTHORIZATION='Bearer {0}'.format(token))
        assert user_result.status_code == 200

    def test_str_user(self):
        self.assertEqual(str(self.user), self.user.username)


class UsersMethodsTestCase(SetupBase):

    # Se comprueba que los usuarios que no envien un jwt no pueden listar usuarios
    def test_unauthorized_get(self):
        result = self.client.get('/api/v1/users/')
        result_only_one = self.client.get('/api/v1/users/1/')
        assert result.status_code, result_only_one.status_code == 403

    # Se comprueba que para crear un usuario no es necesario enviar jwt
    def test_create_user(self):
        user = self.client.post('/api/v1/users/', {
            "username": "testN",
            "email": "testn@gmail.com",
            "first_name": "test name",
            "last_name": "test last name",
            "course": "E2020",
            "gender": "M",
            "password": "prueba1234"
        })
        assert user.status_code == 201

    # Se comprueba que solo el usuario puede editar su propio usuario
    def test_edit_user(self):
        result = self.client.post('/api/token/', {'email': 'test_user@mail.com', 'password': '123456'})
        token = result.data['access']
        user_result = self.client.patch('/api/v1/users/test_user/', {'name': 'editado'},
                                     HTTP_AUTHORIZATION='Bearer {0}'.format(token))
        assert  user_result.status_code == 200



class NewProfileTestCase(SetupBase):

    # Test que prueba que un perfil se crea después de crear un usuario
    def test_new_profile(self):
        auth = self.client.post('/api/token/', {'email': 'test_user@mail.com', 'password': '123456'})
        token = auth.data['access']
        result = self.client.get('/api/v1/profiles/test_user/', HTTP_AUTHORIZATION='Bearer {0}'.format(token))
        assert result.status_code == 200
