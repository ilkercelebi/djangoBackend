from django.db import models
import uuid
from querys.models import Query

class Response(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    query_id = models.ForeignKey(Query,on_delete=models.CASCADE)
    

    