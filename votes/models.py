from django.db import models

from accounts.models import User
from articles.models import Article


class Vote(models.Model):
    value = models.NullBooleanField()
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)

    article = models.ForeignKey(Article,
                                on_delete=models.CASCADE,
                                related_name='likes')

    voted_on = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        unique_together = ('user', 'article')

    def __str__(self):
        if self.value:
            return str(self.user) + ' ' + 'Like' + ' ' + str(self.article)
        else:
            return str(self.user) + ' ' + 'Dislike' + ' ' + str(self.article)