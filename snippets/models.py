from django.db import models
from django.contrib.auth.models import User

# Tag model represents a tag associated with a snippet
class Tag(models.Model):
    title = models.CharField(max_length=100)  # Title of the tag

    def __str__(self):
        return self.title  # String representation of the tag is its title

# Snippet model represents a code snippet with a title, content, timestamp,
# the user who created it, and the associated tag
class Snippet(models.Model):
    title = models.CharField(max_length=100)  # Title of the snippet
    content = models.TextField()  # Content of the snippet
    timestamp = models.DateTimeField(auto_now_add=True)  # Timestamp when snippet was created
    created_user = models.ForeignKey(User, on_delete=models.CASCADE)  # User who created the snippet
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)  # Tag associated with the snippet

    def __str__(self):
        return self.title  # String representation of the snippet is its title
