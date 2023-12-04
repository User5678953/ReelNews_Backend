from django.contrib import admin
from django.urls import path, include



urlpatterns = [
    path('', include('news_archive.urls')),
    path('admin/', admin.site.urls),
    path('news/', include('news_app.urls')),
    path('archives/', include('news_archive.urls')),
    path('auth/', include('auth_app.urls')),
]

