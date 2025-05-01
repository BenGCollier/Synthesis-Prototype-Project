from django.db import models
from django.conf import settings
from courses.models import Course

class PortfolioEntry(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='portfolio_files/')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='portfolio_entries')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='portfolio_entries')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.student})"
