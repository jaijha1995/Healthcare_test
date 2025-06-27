from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Candidate
from .serializers import CandidateSerializer

class CandidateAPIView(APIView):
    def get(self, request, id=None):
        # List or retrieve
        if id:
            candidate = Candidate.objects.filter(id=id).first()
            if not candidate:
                return Response({"status": "error", "message": "Candidate not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = CandidateSerializer(candidate)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            skill_filter = request.GET.get('skill', None)
            if skill_filter:
                candidates = Candidate.objects.filter(skills__icontains=skill_filter)
            else:
                candidates = Candidate.objects.all()
            serializer = CandidateSerializer(candidates, many=True)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CandidateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data, "msg": "Candidate created successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "error", "data": serializer.errors, "msg": "Please provide valid fields"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id=None):
        if not id:
            return Response({"status": "error", "message": "ID is required for update"}, status=status.HTTP_400_BAD_REQUEST)
        candidate = Candidate.objects.filter(id=id).first()
        if not candidate:
            return Response({"status": "error", "message": "Candidate not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CandidateSerializer(candidate, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors, "message": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id=None):
        if not id:
            return Response({"status": "error", "message": "ID is required for partial update"}, status=status.HTTP_400_BAD_REQUEST)
        candidate = Candidate.objects.filter(id=id).first()
        if not candidate:
            return Response({"status": "error", "message": "Candidate not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CandidateSerializer(candidate, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors, "message": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):
        if not id:
            return Response({"status": "error", "message": "ID is required for deletion"}, status=status.HTTP_400_BAD_REQUEST)
        candidate = Candidate.objects.filter(id=id).first()
        if not candidate:
            return Response({"status": "error", "message": "Candidate not found"}, status=status.HTTP_404_NOT_FOUND)
        candidate.delete()
        return Response({"status": "success", "message": "Candidate deleted successfully"}, status=status.HTTP_200_OK)
    



##### Candidate Documents #####

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Candidate, CandidateDocument
from .serializers import CandidateDocumentSerializer

class CandidateDocumentAPIView(APIView):
    """
    Add, Get, and Update resume/certificates for a candidate.
    Endpoint: /api/candidates/{id}/doc
    """

    def get(self, request, id):
        """
        Retrieve all documents (resume/certificates) for a candidate.
        """
        candidate = Candidate.objects.filter(id=id).first()
        if not candidate:
            return Response({"status": "error", "message": "Candidate not found"}, status=status.HTTP_404_NOT_FOUND)
        documents = CandidateDocument.objects.filter(candidate=candidate)
        serializer = CandidateDocumentSerializer(documents, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, id):
        """
        Upload a new resume/certificate for a candidate.
        Accepts: doc_type (str), document (file)
        """
        candidate = Candidate.objects.filter(id=id).first()
        if not candidate:
            return Response({"status": "error", "message": "Candidate not found"}, status=status.HTTP_404_NOT_FOUND)
        data = request.data.copy()
        data['candidate'] = candidate.id
        serializer = CandidateDocumentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data, "msg": "Document uploaded"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        """
        Update an existing document for a candidate.
        Accepts: id (doc ID), doc_type (optional), document (optional)
        """
        candidate = Candidate.objects.filter(id=id).first()
        if not candidate:
            return Response({"status": "error", "message": "Candidate not found"}, status=status.HTTP_404_NOT_FOUND)
        doc_id = request.data.get("id")
        if not doc_id:
            return Response({"status": "error", "message": "Document ID required in body"}, status=status.HTTP_400_BAD_REQUEST)
        doc = CandidateDocument.objects.filter(id=doc_id, candidate=candidate).first()
        if not doc:
            return Response({"status": "error", "message": "Document not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CandidateDocumentSerializer(doc, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data, "msg": "Document updated"}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)