# myapp/serializers.py
from rest_framework import serializers
from .models import Candidate , CandidateDocument

class CandidateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Candidate
        fields = '__all__'

class CandidateDocumentSerializer(serializers.ModelSerializer):
    candidate = serializers.PrimaryKeyRelatedField(queryset=Candidate.objects.all())
    class Meta:
        model = CandidateDocument
        fields = '__all__'
        

    def create(self, validated_data):
        candidate_data = validated_data.pop('candidate')
        company_instance = Candidate.objects.create(**validated_data)
        company_instance.moduler.set(candidate_data)
        return company_instance
    

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['candidate'] = CandidateSerializer(instance.candidate).data
        return representation
