from django.db import models
from django.contrib.auth.models import User

class Document(models.Model):
    owner = models.ForeignKey(User)
    public = models.BooleanField()
    doc_name = models.CharField(max_length = 100)
    doc_file = models.FileField(upload_to = r'files/')
    
    def __unicode__(self):
        return self.doc_name