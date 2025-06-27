from django.db import models

# Create your models here.


class Candidate(models.Model):
    name = models.CharField(max_length=100)
    skills = models.TextField(blank=True)
    education = models.TextField(blank=True)
    related_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Candidate"
        verbose_name_plural = "Candidates"
        ordering = ['name']



class CandidateDocument(models.Model):
    candidate = models.ForeignKey(Candidate, related_name='documents', on_delete=models.CASCADE)
    document = models.FileField(upload_to='candidate_documents/')
    doc_type = models.CharField(max_length=50, help_text="e.g. Resume, Certificate")

    def __str__(self):
        return f"{self.candidate.name} - {self.doc_type}"
    
    class Meta:
        verbose_name = "Candidate Document"
        verbose_name_plural = "Candidate Documents"
        ordering = ['candidate', 'doc_type']