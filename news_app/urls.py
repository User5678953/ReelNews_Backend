from django.urls import path
from .views import TopHeadlinesView, AllArticlesView, SourcesView

urlpatterns = [
    path('top-headlines/', TopHeadlinesView.as_view(), name='top-headlines'),
    path('all-articles/', AllArticlesView.as_view(), name='all-articles'),
    path('sources/', SourcesView.as_view(), name='sources'),
]
