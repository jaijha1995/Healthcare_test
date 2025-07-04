from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import UserRateThrottle
from django.db.models import Q
from django.core.cache import cache
from .models import Product
from .serializers import ProductSerializer


class productAPIView(APIView):
    #throttle_classes = [UserRateThrottle]  # Apply per-view rate limiting

    def get(self, request, id=None):
        if id:
            cache_key = f"product_detail_{id}"
            cached_data = cache.get(cache_key)

            if cached_data:
                return Response(cached_data, status=status.HTTP_200_OK)

            product_obj = Product.objects.filter(id=id).first()
            if product_obj:
                serializer = ProductSerializer(product_obj)
                data = {"status": "success", "data": serializer.data}
                cache.set(cache_key, data, timeout=60 * 60 * 24)  # Cache for 24 Hrs
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({"status": "error", "message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        # ✅ List Products with filters
        title_types = request.query_params.get('title_types')
        name = request.query_params.get('name')
        price = request.query_params.get('price')
        in_stock = request.query_params.get('in_stock')
        gender = request.query_params.get('gender')
        size_tags = request.query_params.get('size_tags')
        section = request.query_params.get('section')

        cache_key = f"product_list_{request.get_full_path()}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)

        queryset = Product.objects.all()

        if title_types:
            queryset = queryset.filter(title_types=title_types)
        if name:
            queryset = queryset.filter(Q(name__icontains=name) | Q(description__icontains=name))
        if price:
            queryset = queryset.filter(price=price)
        if in_stock in ['true', 'false']:
            queryset = queryset.filter(in_stock=(in_stock.lower() == 'true'))
        if gender:
            queryset = queryset.filter(gender=gender)
        if size_tags:
            queryset = queryset.filter(size_tags__icontains=size_tags)
        if section:
            queryset = queryset.filter(section__icontains=section)

        paginator = PageNumberPagination()
        page_size = request.query_params.get('page_size')
        paginator.page_size = int(page_size) if page_size and page_size.isdigit() else 100

        queryset = queryset.order_by('id')
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = ProductSerializer(paginated_queryset, many=True)

        response_data = {"status": "success", "data": serializer.data}
        cache.set(cache_key, response_data, timeout=60 * 5)  # Cache for 5 min

        return paginator.get_paginated_response(response_data)

    def post(self, request, org_id=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product_obj = serializer.save()
            cache.clear()  # Invalidate cache
            return Response({
                "status": "success",
                "data": serializer.data,
                "msg": "Product created successfully"
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "error",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id=None):
        if not id:
            return Response({"status": "error", "message": "ID is required for update"}, status=status.HTTP_400_BAD_REQUEST)

        product_obj = Product.objects.filter(id=id).first()
        if not product_obj:
            return Response({"status": "error", "message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.clear()  # Invalidate cache
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"status": "error", "message": "Invalid data", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id=None):
        if not id:
            return Response({"status": "error", "message": "ID is required for partial update"}, status=status.HTTP_400_BAD_REQUEST)

        product_obj = Product.objects.filter(id=id).first()
        if not product_obj:
            return Response({"status": "error", "message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            cache.clear()  # Invalidate cache
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"status": "error", "message": "Invalid data", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):
        if not id:
            return Response({"status": "error", "message": "ID is required for deletion"}, status=status.HTTP_400_BAD_REQUEST)

        product_obj = Product.objects.filter(id=id).first()
        if not product_obj:
            return Response({"status": "error", "message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        product_obj.delete()
        cache.clear()  # Invalidate cache
        return Response({"status": "success", "message": "Product deleted successfully"}, status=status.HTTP_200_OK)
