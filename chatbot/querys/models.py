from django.db import models
import uuid
from users.models import User

class Query(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user_query = models.CharField(max_length=256)
    timestamp =models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Query by {self.user.username} at {self.timestamp}"
