from django.urls import path
from .views import CreateUserView, LogoutView

urlpatterns = [
    path('register/', CreateUserView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

