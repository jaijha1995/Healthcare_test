from django.urls import path
from .views import OrderView

urlpatterns = [
    path('orders/', OrderView.as_view()),             # GET (paginated), POST
    path('orders/<int:pk>/', OrderView.as_view()),    # PATCH, DELETE by ID
]