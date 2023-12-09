from rest_framework.views import APIView
from rest_framework.response import Response
import os
import logging
from newsapi import NewsApiClient
from datetime import datetime, timedelta
from rest_framework.permissions import AllowAny

# Initialize logger
logger = logging.getLogger(__name__)

class TopHeadlinesView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        query = request.query_params.get('q')
        category = request.query_params.get('category')
        language = request.query_params.get('language')
        country = request.query_params.get('country')

        # Log the received parameters
        logger.info(f'Received parameters: Query={query}, Category={category}, Language={language}, Country={country}')

        newsapi = NewsApiClient(api_key=os.getenv('NEWS_API_KEY'))
        response = newsapi.get_top_headlines(q=query, category=category, language=language, country=country)

        # Log the raw response
        logger.info(f'NewsAPI Response: {response}')

        return Response(response)

class AllArticlesView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        query = request.query_params.get('q', 'news, world, business, technology, sports, entertainment')
        sources = request.query_params.get('sources', '')
        domains = request.query_params.get('domains', '')

        today = datetime.today()
        thirty_days_ago = today - timedelta(days=30)

        response = newsapi.get_everything(q=query, sources=sources, domains=domains, from_param=thirty_days_ago.strftime('%Y-%m-%d'), to=today.strftime('%Y-%m-%d'), language='en', sort_by='relevancy', page=1)
        return Response(response)

class SourcesView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        response = newsapi.get_sources(language='en', country='us')
        return Response(response)
