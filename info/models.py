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

    def __str__(self):
        return self.page_type
