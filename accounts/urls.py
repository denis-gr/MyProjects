from django.urls import path, include

from .views import SignUpView, ProfileView, UserDeleteView, LoginView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('', include('django.contrib.auth.urls')),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('delete/', UserDeleteView.as_view(), name='user_delete'),
]
