from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from .models import Contact
from .serializers import contactSerializer


class contactAPIView(APIView):
    def get(self, request, id=None):
        if id:
            contact_obj = Contact.objects.filter(id=id).first()
            if contact_obj:
                serializer = contactSerializer(contact_obj)
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "error", "message": "Contact not found"}, status=status.HTTP_404_NOT_FOUND)

        # ✅ Apply dynamic pagination
        paginator = PageNumberPagination()
        page_size = request.query_params.get('page_size')
        paginator.page_size = int(page_size) if page_size and page_size.isdigit() else 100

        queryset = Contact.objects.all().order_by('id')
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = contactSerializer(paginated_queryset, many=True)

        return paginator.get_paginated_response({"status": "success", "data": serializer.data})

    def post(self, request, org_id=None):
        serializer = contactSerializer(data=request.data)
        if serializer.is_valid():
            contact_obj = serializer.save()
            return Response({
                "status": "success",
                "data": serializer.data,
                "msg": "We will connect shortly"
            }, status=status.HTTP_200_OK)
        return Response({
            "status": "Please provide mandatory fields",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id=None):
        if not id:
            return Response({"status": "error", "message": "ID is required for update"}, status=status.HTTP_400_BAD_REQUEST)

        contact_obj = Contact.objects.filter(id=id).first()
        if not contact_obj:
            return Response({"status": "error", "message": "Contact not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = contactSerializer(contact_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"status": "error", "message": "Invalid data", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id=None):
        if not id:
            return Response({"status": "error", "message": "ID is required for partial update"}, status=status.HTTP_400_BAD_REQUEST)

        contact_obj = Contact.objects.filter(id=id).first()
        if not contact_obj:
            return Response({"status": "error", "message": "Contact not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = contactSerializer(contact_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"status": "error", "message": "Invalid data", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):
        if not id:
            return Response({"status": "error", "message": "ID is required for deletion"}, status=status.HTTP_400_BAD_REQUEST)

        contact_obj = Contact.objects.filter(id=id).first()
        if not contact_obj:
            return Response({"status": "error", "message": "Contact not found"}, status=status.HTTP_404_NOT_FOUND)

        contact_obj.delete()
        return Response({"status": "success", "message": "Contact deleted successfully"}, status=status.HTTP_200_OK)
