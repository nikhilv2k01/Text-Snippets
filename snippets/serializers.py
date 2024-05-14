from rest_framework import serializers
from .models import Snippet, Tag

# Serializer for the Tag model
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'title']

# Serializer for the Snippet model
class SnippetSerializer(serializers.ModelSerializer):
    # Nested TagSerializer to include tag details in the snippet representation
    tag = TagSerializer()

    class Meta:
        model = Snippet
        fields = ['id', 'title', 'timestamp', 'created_user', 'tag']

    # Custom create method to handle nested tag creation or retrieval
    def create(self, validated_data):
        # Extract tag data from validated data
        tag_data = validated_data.pop('tag')
        tag_title = tag_data.get('title')
        
        # Get or create a tag with the provided title
        tag, _ = Tag.objects.get_or_create(title=tag_title)

        # Check if a snippet with the same tag and validated data already exists
        snippet = Snippet.objects.filter(tag=tag, **validated_data).first()

        if snippet:
            # If snippet exists, return it
            return snippet
        else:
            # If snippet does not exist, create a new snippet linked to the tag
            snippet = Snippet.objects.create(tag=tag, **validated_data)
            return snippet

# Detailed serializer for the Snippet model with content field included
class SnippetDetailSerializer(serializers.ModelSerializer):
    # Nested TagSerializer to include tag details in the snippet representation
    tag = TagSerializer()

    class Meta:
        model = Snippet
        fields = ['id', 'title', 'timestamp', 'created_user', 'content', 'tag']

# Serializer for updating the Snippet model
class SnippetUpdateSerializer(serializers.ModelSerializer):
    # Nested TagSerializer to handle updating tag details
    tag = TagSerializer()

    class Meta:
        model = Snippet
        fields = ['title', 'content', 'created_user', 'tag']

    # Custom update method to handle nested tag update or creation
    def update(self, instance, validated_data):
        # Extract tag data from validated data if present
        tag_data = validated_data.pop('tag', None)
        
        if tag_data:
            tag_title = tag_data.get('title')
            try:
                # Try to get an existing tag with the provided title
                tag = Tag.objects.get(title=tag_title)
                # Update the tag attributes
                for attr, value in tag_data.items():
                    setattr(tag, attr, value)
                # Save the updated tag
                tag.save()
            except Tag.DoesNotExist:
                # If tag does not exist, create a new tag
                tag = Tag.objects.create(**tag_data)
            # Set the updated or new tag to the snippet instance
            instance.tag = tag

        # Update the snippet instance attributes
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Save the updated snippet instance
        instance.save()
        return instance
