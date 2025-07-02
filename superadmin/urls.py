# myapp/urls.py
from django.urls import path
from .views import SuperAdminListView, SuperAdminDetailView , Loginsuperadmin

urlpatterns = [
    path('superadmin/', SuperAdminListView.as_view(), name='superadmin-list'),
    path('superadmin/<int:pk>/', SuperAdminDetailView.as_view(), name='superadmin-detail'),
    path('login/', Loginsuperadmin.as_view()),
]
