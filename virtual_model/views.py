from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.core.cache import cache
from .models import Category, SubCategory, SubSubCategory
from .serializers import CategorySerializer, SubCategorySerializer, SubSubCategorySerializer


class CustomPagination(PageNumberPagination):
    page_size = 100  # Always fetch 100 items
    page_size_query_param = 'page_size'
    max_page_size = 100


class CategoryView(APIView):
    def get(self, request):
        cache_key = 'category_list_page_' + str(request.GET.get('page', 1))
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        categories = Category.objects.filter(type='category')
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(categories, request)
        serializer = CategorySerializer(result_page, many=True)

        cache.set(cache_key, serializer.data, timeout=60 * 5)  # Cache for 5 minutes
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        data['type'] = 'category'
        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            cache.clear()  # Clear cache on new insert
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class SubCategoryView(APIView):
    def get(self, request):
        cache_key = 'subcategory_list_page_' + str(request.GET.get('page', 1))
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        subcategories = SubCategory.objects.filter(type='subcategory')
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(subcategories, request)
        serializer = SubCategorySerializer(result_page, many=True)

        cache.set(cache_key, serializer.data, timeout=60 * 5)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        data['type'] = 'subcategory'
        serializer = SubCategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            cache.clear()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class SubSubCategoryView(APIView):
    def get(self, request):
        cache_key = 'subsubcategory_list_page_' + str(request.GET.get('page', 1))
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        subsubcategories = SubSubCategory.objects.filter(type='subsubcategory')
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(subsubcategories, request)
        serializer = SubSubCategorySerializer(result_page, many=True)

        cache.set(cache_key, serializer.data, timeout=60 * 5)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        data['type'] = 'subsubcategory'
        serializer = SubSubCategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            cache.clear()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
