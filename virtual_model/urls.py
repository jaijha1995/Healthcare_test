from django.urls import path
from .views import CategoryView, SubCategoryView, SubSubCategoryView

urlpatterns = [
    path('category/', CategoryView.as_view(), name='category'),
    path('subcategory/', SubCategoryView.as_view(), name='subcategory'),
    path('subsubcategory/', SubSubCategoryView.as_view(), name='subsubcategory'),
]
