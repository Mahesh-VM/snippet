from django.urls import re_path
from authapp.viewsets import UserViewSet


urlpatterns = [
    # re_path('^get-user/$', UserViewSet.as_view({'get': 'list'}), name='user'),
    re_path('^register-user/$', UserViewSet.as_view({'post': 'create'}), name='register'),
]
