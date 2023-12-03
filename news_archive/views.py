from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from .serializers import ArchiveSerializer
from .models import Archive


@api_view(['GET'])
@permission_classes([AllowAny])
def getRoutes(request):
    routes = [
    {
        'Endpoint': '/archive/',
        'method': 'GET',
        'body': None,
        'description': 'List all items in the archive.'
    },
    {
        'Endpoint': '/archive/<id>/',
        'method': 'GET',
        'body': None,
        'description': 'Retrieve a specific item from the archive.'
    },
    {
        'Endpoint': '/archive/create/',
        'method': 'POST',
        'body': 'Data for new item',
        'description': 'Create a new item in the archive.'
    },
    {
        'Endpoint': '/archive/update/<id>/',
        'method': 'PUT',
        'body': 'Updated data for item',
        'description': 'Update a specific item in the archive.'
    },
    {
        'Endpoint': '/archive/delete/<id>/',
        'method': 'DELETE',
        'body': None,
        'description': 'Delete a specific item from the archive.'
    }
]

    return Response(routes)

@api_view(['GET'])
@permission_classes([AllowAny])
def getArchives(request):
    archives = Archive.objects.all()
    serializer = ArchiveSerializer(archives, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def getArchive(request, pk):
    archive = Archive.objects.get(id=pk)
    serializer = ArchiveSerializer(archive, many=False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
def createArchive(request):
    data = request.data

    try:
        # Create new Archive object
        archive = Archive.objects.create(
            user=None,
            title=data['title'],
            content=data.get('content', ''), 
            author=data.get('author'),
            source=data.get('source'),
            url=data.get('url')
        )
        serializer = ArchiveSerializer(archive, many=False)
        return Response(serializer.data)
    
    except KeyError as e:

        return Response({'error': f'Missing key in request: {str(e)}'})
    
@api_view(['PUT', 'PATCH'])
@permission_classes([AllowAny])
def updateArchive(request, pk):
    try:
        archive = Archive.objects.get(pk=pk)
        
        # Use request.data to access the request body data
        serializer = ArchiveSerializer(archive, data=request.data, partial=request.method == 'PATCH')
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Archive.DoesNotExist:
        return Response({'error': 'Archive not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@permission_classes([AllowAny])   
def deleteArchive(request, pk):
    archive = Archive.objects.get(id=pk)
    archive.delete()
    return Response ("Article was deleted")