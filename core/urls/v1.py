from django.urls import include, path
from rest_framework import  routers

from accounts.views import UserViewSet
from events.views import EventViewSet, SpeakerViewSet
from profiles.views import ProfileViewSet
from articles.views import ArticleViewSet, CommentViewSet
from votes.views import LikesViewSet

router = routers.DefaultRouter()

router.register(r'users', UserViewSet)
router.register(r'profiles', ProfileViewSet)
router.register(r'articles', ArticleViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'likes', LikesViewSet)
router.register(r'events', EventViewSet)
router.register(r'speakers', SpeakerViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path(r'password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset'))
]