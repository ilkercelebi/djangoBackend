from django.conf import settings
from django.db import models
import uuid
from querys.models import Query

class Response(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Doğru Kullanım
    query = models.ForeignKey(Query, on_delete=models.CASCADE)
    result = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response by {self.user.username} for query {self.query.id}"
