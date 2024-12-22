from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import (CommentViewSet, FollowListCreateViewSet,
                       GroupViewSet, PostViewSet)

router_v1 = SimpleRouter()
router_v1.register('posts', PostViewSet, basename='post')
router_v1.register('groups', GroupViewSet, basename='group')
router_v1.register(
    r'posts/(?P<post_id>\d+)/comments', CommentViewSet, basename='comment')
router_v1.register('follow', FollowListCreateViewSet, basename='follow')

urlpatterns = [
    path('v1/', include('djoser.urls.jwt')),
    path('v1/', include(router_v1.urls)),
]
