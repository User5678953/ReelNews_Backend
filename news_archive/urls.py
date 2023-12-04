from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('archives/', views.getArchives),
    path('archives/update/<str:pk>/', views.updateArchive),
    path('archives/delete/<str:pk>/', views.deleteArchive),
     path('archives/save/', views.save_article), 
    path('archives/<str:pk>/', views.getArchive),
   
]