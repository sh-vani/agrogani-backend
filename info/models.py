# pages/models.py
from django.db import models

class Page(models.Model):
    PAGE_TYPES = [
        ('terms', 'Terms & Conditions'),
        ('privacy', 'Privacy Policy'),
        ('about', 'About Us'),
        ('contact', 'Contact Us'),
    ]
    page_type = models.CharField(max_length=50, choices=PAGE_TYPES, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()  # Store HTML content
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title