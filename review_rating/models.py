from django.db import models
from django.contrib.auth.models import User
import uuid

class ReviewRating(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    review = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_posted')
    reviewee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_received')

    class Meta:
        db_table = 'review_rating'
        
    def __str__(self):
        return self.review