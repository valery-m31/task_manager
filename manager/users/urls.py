from django.urls import path
from .views import SignUpView, edit_profile


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/<int:pk>/', edit_profile, name='profile')
]
