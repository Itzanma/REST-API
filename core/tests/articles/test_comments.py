from core.tests.accounts.test_authentication import SetupBase
from core.tests.articles.test_articles import ArticleTestCase


class CommentsTestCase(SetupBase):
    def test_comment_article(self):
        result = self.client.post('/api/token/', {'email': 'test_user@mail.com', 'password': '123456'})
        token = result.data['access']
        article = self.client.post('/api/v1/articles/', {
            "title": "Test Article",
            "body": "Test body",
            "author": 1
        }, HTTP_AUTHORIZATION='Bearer {0}'.format(token))

        comment = self.client.post('/api/v1/comments/', {
            "author": 1,
            "body": "nuevo",
            "article": 1
        }, HTTP_AUTHORIZATION='Bearer {0}'.format(token))
        assert comment.status_code == 201
