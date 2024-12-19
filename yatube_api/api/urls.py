from django.urls import path, include
from rest_framework.routers import SimpleRouter

from api.views import CommentViewSet, GroupViewSet, PostViewSet, FollowApiView


router_v1 = SimpleRouter()
router_v1.register('posts', PostViewSet, basename='post')
router_v1.register('groups', GroupViewSet)
router_v1.register(
    r'posts/(?P<post_id>\d+)/comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
    path('v1/', include(router_v1.urls)),
    path('v1/follow/', FollowApiView.as_view(), name='follow-list-create'),
]
