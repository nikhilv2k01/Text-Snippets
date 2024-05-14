from django.urls import path
from . import views

# URL patterns for the API endpoints
urlpatterns = [
    # URL pattern for the overview API endpoint
    path('overview/', views.OverviewAPIView.as_view(), name='overview'),

    # URL pattern for listing and creating snippets
    path('snippets/', views.SnippetListCreateAPIView.as_view(), name='snippet-list-create'),

    # URL pattern for retrieving a specific snippet by its primary key
    path('snippets/<int:pk>/', views.SnippetDetailAPIView.as_view(), name='snippet-detail'),

    # URL pattern for updating a specific snippet by its primary key
    path('snippets/<int:pk>/update/', views.SnippetUpdateAPIView.as_view(), name='snippet-update'),

    # URL pattern for deleting a specific snippet by its primary key
    path('snippets/<int:pk>/delete/', views.SnippetDeleteAPIView.as_view(), name='snippet-delete'),

    # URL pattern for listing all tags
    path('tags/', views.TagListAPIView.as_view(), name='tag-list'),

    # URL pattern for retrieving snippets associated with a specific tag by its primary key
    path('tags/<int:pk>/', views.TagDetailAPIView.as_view(), name='tag-detail'),
]
