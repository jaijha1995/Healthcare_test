# myapp/urls.py
from django.urls import path
from .views import CandidateAPIView , CandidateDocumentAPIView

urlpatterns = [
    path('candidate/', CandidateAPIView.as_view(), name='candidate-list'),
    path('candidate/<int:id>/', CandidateAPIView.as_view(), name='candidate-detail'),
    path('candidates/<int:id>/doc', CandidateDocumentAPIView.as_view()),
]
