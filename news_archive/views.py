from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from .serializers import ArchiveSerializer
from .models import NewsArchive


@api_view(['GET'])
@permission_classes([AllowAny])
def getRoutes(request):
    routes = [
    {
        "Endpoint": "/archives/",
        "method": "GET",
        "body": None,
        "description": "List all items in the archive."
    },
    {
        "Endpoint": "/archives/<id>/",
        "method": "GET",
        "body": None,
        "description": "Retrieve a specific item from the archive."
    },
    {
        "Endpoint": "/archives/update/<id>/",
        "method": "PUT",
        "body": "Updated data for item",
        "description": "Update a specific item in the archive."
    },
    {
        "Endpoint": "/archives/delete/<id>/",
        "method": "DELETE",
        "body": None,
        "description": "Delete a specific item from the archive."
    },
    {
        "Endpoint": "/auth/register/",
        "method": "POST",
        "body": "User registration data",
        "description": "Register a new user."
    },
    {
        "Endpoint": "/auth/login/",
        "method": "POST",
        "body": "User login data",
        "description": "Login the user."
    },
    {
        "Endpoint": "/news/top-headlines/",
        "method": "GET",
        "body": None,
        "description": "Get top headlines."
    },
    {
        "Endpoint": "/news/all-articles/",
        "method": "GET",
        "body": None,
        "description": "Get all articles."
    },
    {
        "Endpoint": "/news/sources/",
        "method": "GET",
        "body": None,
        "description": "Get available news sources."
    }
]
    return Response(routes)

@api_view(['GET'])
@permission_classes([AllowAny])
def getArchives(request):
    archives = NewsArchive.objects.all()
    serializer = ArchiveSerializer(archives, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def getArchive(request, pk):
    archive = NewsArchive.objects.get(id=pk)
    serializer = ArchiveSerializer(archive, many=False)
    return Response(serializer.data)

@api_view(['PUT', 'PATCH'])
@permission_classes([AllowAny])
def updateArchive(request, pk):
    try:
        archive = NewsArchive.objects.get(pk=pk)
        
        # Use request.data to access the request body data
        serializer = ArchiveSerializer(archive, data=request.data, partial=request.method == 'PATCH')
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except NewsArchive.DoesNotExist:
        return Response({'error': 'Archive not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@permission_classes([AllowAny])   
def deleteArchive(request, pk):
    archive = NewsArchive.objects.get(id=pk)
    archive.delete()
    return Response ("Article was deleted")

@api_view(['POST'])
@permission_classes([AllowAny])  
def save_article(request):
    data = request.data

    try:
        user = request.user

        # Check if the article with the same title already exists in the user's archive
        existing_article = NewsArchive.objects.filter(title=data['title'], user=user).first()
        
        if existing_article:
            # Article already exists in the user's archive, no need to save it again
            return Response({'message': 'Article already saved in your archive.'}, status=status.HTTP_200_OK)
        else:
            # Article doesn't exist in the user's archive, create it and associate with the user
            article = NewsArchive(
                source_id=data.get('source_id'),
                source_name=data.get('source_name'),
                author=data.get('author'),
                title=data['title'],
                description=data.get('description'),
                url=data.get('url'),
                url_to_image=data.get('url_to_image'),
                published_at=data.get('published_at'),
                content=data.get('content', ''),
                user=user 
            )
            article.save()  # Save the article
            serializer = ArchiveSerializer(article, many=False)
            return Response({'message': 'Article saved to your archive.', 'data': serializer.data}, status=status.HTTP_201_CREATED)
    
    except KeyError as e:
        return Response({'error': f'Missing key in request: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)