from django.db import models
from django.utils import timezone

class MessageScan(models.Model):
    CLASSIFICATION_CHOICES = [
        ('phishing', 'Phishing'),
        ('legitimate', 'Legitimate'),
    ]

    text = models.TextField()
    classification = models.CharField(max_length=20, choices=CLASSIFICATION_CHOICES)
    confidence = models.FloatField()
    is_url_scan = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.classification.capitalize()} - {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
