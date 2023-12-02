from django.urls import path
from . import views


urlpatterns = [
    path('top-headlines/', views.top_headlines, name='top-headlines'),
    path('all-articles/', views.all_articles, name='all-articles'),
    path('sources/', views.sources, name='sources'),
]
