# Create your views here.

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegistrationSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Notes
from .serializers import NotesSerializer


@api_view(['POST'])
def user_registration(request):
    serializer = UserRegistrationSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            'user_id': str(user.user_id),
            'username': user.user_name,
            'email': user.user_email
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
def user_login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    # Check if email and password are provided
    if not email or not password:
        return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(user_email=email)

        # Check if password is correct
        if not user.check_password(password):
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response({
            'user_id': str(user.user_id),
            'username': user.user_name,
            'email': user.user_email,
            'refresh_token': str(refresh),
            'access_token': str(refresh.access_token)
        }, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_note(request):
    serializer = NotesSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_note_by_id(request, note_id):
    try:
        note = Notes.objects.get(note_id=note_id, user=request.user, is_deleted=False)
        serializer = NotesSerializer(note)
        return Response(serializer.data)
    except Notes.DoesNotExist:
        return Response({"error": "Note not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_notes(request):
   
    user_notes = Notes.objects.filter(
        user=request.user,  # Specific to current user
        is_deleted=False    # Only active notes
    )
    serializer = NotesSerializer(user_notes, many=True)
    
    return Response({
        'user_id': str(request.user.user_id),
        'username': request.user.user_name,
        'total_notes': user_notes.count(),
        'notes': serializer.data
    })
     
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_note(request, note_id):
    try:
        note = Notes.objects.get(note_id=note_id, user=request.user, is_deleted=False)
        serializer = NotesSerializer(note, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Notes.DoesNotExist:
        return Response({"error": "Note not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_note(request, note_id):
    try:
        note = Notes.objects.get(note_id=note_id, user=request.user, is_deleted=False)
        note.is_deleted = True
        note.save()
        return Response(
            {"message": "Note deleted successfully"}, 
            status=status.HTTP_204_NO_CONTENT
        )
    except Notes.DoesNotExist:
        return Response({"error": "Note not found"}, status=status.HTTP_404_NOT_FOUND)
