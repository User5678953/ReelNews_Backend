from django.shortcuts import render

# Create your views here.
from newsapi import NewsApiClient
from django.http import JsonResponse
from datetime import datetime, timedelta

# Initialize
newsapi = NewsApiClient(api_key='d446e80f75794e569d031dde304a73f2')

def top_headlines(request):
    # Fetch query parameters
    query = request.GET.get('q', 'world')  
    category = request.GET.get('category', 'general')  
    language = request.GET.get('language', 'en') 
    country = request.GET.get('country', 'us')  

    response = newsapi.get_top_headlines(q=query,
                                         category=category,
                                         language=language,
                                         country=country)
    return JsonResponse(response)



def all_articles(request):
    # Fetch query parameters
    query = request.GET.get('q', 'news, world, business, technology, sports, entertainment')  
    sources = request.GET.get('sources', '')  
    domains = request.GET.get('domains', '') 

    # Set the date range
    today = datetime.today()
    thirty_days_ago = today - timedelta(days=30)

    response = newsapi.get_everything(q=query,
                                      sources=sources,
                                      domains=domains,
                                      from_param=thirty_days_ago.strftime('%Y-%m-%d'),
                                      to=today.strftime('%Y-%m-%d'),
                                      language='en',
                                      sort_by='relevancy',
                                      page=1)
    return JsonResponse(response)

def sources(request):
    response = newsapi.get_sources(language='en', country='us')
    return JsonResponse(response)
