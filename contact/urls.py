# myapp/urls.py
from django.urls import path
from .views import contactAPIView

urlpatterns = [
    path('contact/', contactAPIView.as_view(), name='superadmin-list'),
    path('contact/<int:pk>/', contactAPIView.as_view(), name='superadmin-detail'),
]
