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
        "Endpoint": "/archives/create/",
        "method": "POST",
        "body": "Data for new item",
        "description": "Create a new item in the archive."
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

@api_view(['POST'])
@permission_classes([AllowAny])
def createArchive(request):
    data = request.data

    try:
        # Create new Archive object
        archive = NewsArchive.objects.create(
            source_id=data.get('source_id'),
            source_name=data.get('source_name'),
            author=data.get('author'),
            title=data['title'],
            description=data.get('description'),
            url=data.get('url'),
            url_to_image=data.get('url_to_image'),
            published_at=data.get('published_at'),
            content=data.get('content', '')
        )
        serializer = ArchiveSerializer(archive, many=False)
        return Response(serializer.data)
    
    except KeyError as e:

        return Response({'error': f'Missing key in request: {str(e)}'})
    
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
        # Create new Archive object from the provided data
        archive = NewsArchive.objects.create(
            user=request.user if request.user.is_authenticated else None,
            title=data['title'],
            content=data.get('content', ''),
            author=data.get('author'),
            source=data.get('source'),
            url=data.get('url')
        )
        serializer = ArchiveSerializer(archive, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    except KeyError as e:
        return Response({'error': f'Missing key in request: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)