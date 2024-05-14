from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Snippet, Tag
from .serializers import SnippetSerializer, TagSerializer, SnippetUpdateSerializer, SnippetDetailSerializer

# Create your views here.

class OverviewAPIView(APIView):
    # Ensure the user is authenticated
    permission_classes = [IsAuthenticated]
    
    # Handle GET request
    def get(self, request):
        # Get the total count of snippets
        snippet_count = Snippet.objects.count()
        # Get all snippet objects
        snippets = Snippet.objects.all()
        # Serialize the snippet objects
        serializer = SnippetDetailSerializer(snippets, many=True)
        # Return the count and the serialized data
        return Response({'snippet_count': snippet_count, 'snippets': serializer.data})

class SnippetListCreateAPIView(APIView):
    # Ensure the user is authenticated
    permission_classes = [IsAuthenticated]
    
    # Handle GET request to list snippets
    def get(self, request):
        # Get all snippet objects
        snippets = Snippet.objects.all()
        # Serialize the snippet objects
        serializer = SnippetSerializer(snippets, many=True)
        # Return the serialized data
        return Response(serializer.data)

    # Handle POST request to create a new snippet
    def post(self, request):
        # Get the request data
        data = request.data
        # Set created_user to the authenticated user's ID
        data['created_user'] = request.user.id
        # Serialize the data
        serializer = SnippetSerializer(data=data)
        # Validate the data
        if serializer.is_valid():
            # Save the new snippet
            serializer.save()
            # Return the serialized data with a 201 Created status
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # Return validation errors with a 400 Bad Request status
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SnippetDetailAPIView(APIView):
    # Ensure the user is authenticated
    permission_classes = [IsAuthenticated]
    
    # Handle GET request to retrieve a snippet by ID
    def get(self, request, pk):
        try:
            # Get the snippet object by primary key
            snippet = Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            # Return an error if the snippet does not exist
            return Response({'error': 'Snippet not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Serialize the snippet object
        serializer = SnippetDetailSerializer(snippet)
        # Return the serialized data
        return Response(serializer.data)

class SnippetUpdateAPIView(APIView):
    # Ensure the user is authenticated
    permission_classes = [IsAuthenticated]
    
    # Handle PUT request to update a snippet by ID
    def put(self, request, pk):
        try:
            # Get the snippet object by primary key
            snippet = Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            # Return an error if the snippet does not exist
            return Response({'error': 'Snippet not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Get the request data
        data = request.data
        # Set created_user to the authenticated user's ID
        data['created_user'] = request.user.id
        
        # Serialize the data with the existing snippet instance
        serializer = SnippetUpdateSerializer(snippet, data=data)
        # Validate the data
        if serializer.is_valid():
            # Save the updated snippet
            serializer.save()
            # Return the serialized data
            return Response(serializer.data)
        
        # Return validation errors with a 400 Bad Request status
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SnippetDeleteAPIView(APIView):
    # Ensure the user is authenticated
    permission_classes = [IsAuthenticated]
    
    # Handle DELETE request to delete a snippet by ID
    def delete(self, request, pk):
        try:
            # Get the snippet object by primary key
            snippet = Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            # Return an error if the snippet does not exist
            return Response({'error': 'Snippet not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Delete the snippet
        snippet.delete()
        
        # Get all remaining snippet objects
        remaining_snippets = Snippet.objects.all()
        # Serialize the remaining snippet objects
        serializer = SnippetDetailSerializer(remaining_snippets, many=True)
        
        # Return the serialized data with a 200 OK status
        return Response(serializer.data, status=status.HTTP_200_OK)

class TagListAPIView(APIView):
    # Ensure the user is authenticated
    permission_classes = [IsAuthenticated]
    
    # Handle GET request to list all tags
    def get(self, request):
        # Get all tag objects
        tags = Tag.objects.all()
        # Serialize the tag objects
        serializer = TagSerializer(tags, many=True)
        # Return the serialized data
        return Response(serializer.data)

class TagDetailAPIView(APIView):
    # Ensure the user is authenticated
    permission_classes = [IsAuthenticated]
    
    # Handle GET request to retrieve snippets by tag ID
    def get(self, request, pk):
        try:
            # Get the tag object by primary key
            tag = Tag.objects.get(pk=pk)
        except Tag.DoesNotExist:
            # Return an error if the tag does not exist
            return Response({'error': 'Tag not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Get all snippets associated with the tag
        snippets = tag.snippet_set.all()
        # Serialize the snippet objects
        serializer = SnippetDetailSerializer(snippets, many=True)
        # Return the serialized data with a 200 OK status
        return Response(serializer.data, status=status.HTTP_200_OK)
