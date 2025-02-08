from rest_framework import serializers
from .models import User, Notes

class UserRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        min_length=8,
        style={'input_type': 'password'}
    )
    confirm_password = serializers.CharField(
        write_only=True, 
        required=True,
        style={'input_type': 'password'}
    )

    def validate(self, data):
        # Password matching validation
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match"})
        
        # Unique email and username checks
        if User.objects.filter(user_email=data['email']).exists():
            raise serializers.ValidationError({"email": "Email already exists"})
        
        if User.objects.filter(user_name=data['username']).exists():
            raise serializers.ValidationError({"username": "Username already exists"})
        
        return data

    def create(self, validated_data):
        # Remove confirm_password before user creation
        validated_data.pop('confirm_password')
        
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user
    
    


class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes  # Ensure this matches your model name
        fields = [
            'note_id',  # Change from 'id'
            'note_title',  # Change from 'title'
            'note_content',  # Change from 'content'
            'last_update', 
            'created_on'
        ]
        read_only_fields = ['note_id', 'last_update', 'created_on']

