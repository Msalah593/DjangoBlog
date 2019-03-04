from django.urls import path, re_path, include
from users.views import SignUp, confirmation_view, activate

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('signup/', SignUp.as_view(), name='signup'),
    path('confirmation/', confirmation_view, name='confirmation'),
    re_path(
        r'''validate/(?P<uidb64>[0-9A-Za-z_\-\']+)/
            (?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$''',
        activate, name='user-activation-link')
]
