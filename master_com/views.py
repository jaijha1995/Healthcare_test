from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from .models import Order
from .serializers import OrderSerializer


# ✅ Custom Pagination (100 per page)
class OrderPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 100


class OrderView(APIView):
    def get(self, request):
        cache_key = f"orders_page_{request.GET.get('page', 1)}"
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        orders = Order.objects.select_related(
            'customer', 'superadmin', 'candidate', 'contact', 
            'product', 'category', 'subcategory', 'subsubcategory'
        ).all().order_by('-order_date')

        paginator = OrderPagination()
        page = paginator.paginate_queryset(orders, request)
        serializer = OrderSerializer(page, many=True, context={'request': request})

        cache.set(cache_key, serializer.data, timeout=60 * 5)  # cache for 5 minutes
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = OrderSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            cache.clear()  # clear all cache after create
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        if not pk:
            return Response({'error': 'Order ID (pk) is required for PATCH'}, status=400)

        order = get_object_or_404(Order, pk=pk)
        serializer = OrderSerializer(order, data=request.data, partial=True, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            cache.clear()  # Clear cache after update
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if not pk:
            return Response({'error': 'Order ID (pk) is required for DELETE'}, status=400)

        order = get_object_or_404(Order, pk=pk)
        order.delete()
        cache.clear()  # Clear cache after delete
        return Response({'message': 'Order deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
