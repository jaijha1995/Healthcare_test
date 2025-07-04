from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Category, SubCategory, SubSubCategory
from .serializers import CategorySerializer, SubCategorySerializer, SubSubCategorySerializer


class CategoryView(APIView):
    def get(self, request):
        categories = Category.objects.filter(type='category')
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        data['type'] = 'category'
        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class SubCategoryView(APIView):
    def get(self, request):
        subcategories = SubCategory.objects.filter(type='subcategory')
        serializer = SubCategorySerializer(subcategories, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        data['type'] = 'subcategory'
        serializer = SubCategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class SubSubCategoryView(APIView):
    def get(self, request):
        subsubcategories = SubSubCategory.objects.filter(type='subsubcategory')
        serializer = SubSubCategorySerializer(subsubcategories, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        data['type'] = 'subsubcategory'
        serializer = SubSubCategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
