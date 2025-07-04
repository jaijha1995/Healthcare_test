from rest_framework.urlpatterns import path
from .views import productAPIView

urlpatterns = [
    path('product/', productAPIView.as_view(), name='address-list'),
    path('product/<int:pk>/', productAPIView.as_view(), name='address-detail')
]
