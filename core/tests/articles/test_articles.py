from rest_framework.test import APITestCase

from accounts.models import User
from articles.models import Article
from core.tests.accounts.test_authentication import SetupBase


class ArticleTestCase(SetupBase):

    def test_create(self):
        # Se comprueba que un usuario autenticado pueda crear un artículo y evita creación por parte de no autorizados
        result = self.client.post('/api/token/', {'email': 'test_user@mail.com', 'password': '123456'})
        token = result.data['access']
        article = self.client.post('/api/v1/articles/', {
            "title": "Test Article",
            "body": "Test body",
            "author": 1
        }, HTTP_AUTHORIZATION='Bearer {0}'.format(token))

        unauthorized = self.client.post('/api/v1/articles/', {
            "title": "Test Article",
            "body": "Test body",
            "author": 1
        })

        assert article.status_code == 201 and unauthorized.status_code == 403

