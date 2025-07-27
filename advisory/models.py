from django.db import models

class Advisory(models.Model):  # Renamed from ImportantContact
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    office_address = models.CharField(max_length=255, blank=True, null=True)
    timing = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name



class FertilizerShop(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=300)
    hours = models.CharField(max_length=100)
    products = models.TextField()
    contact_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)






# from django.db import models
# from django.contrib.gis.db import models as geomodels

# class Region(models.Model):
#     name = models.CharField(max_length=100)
#     lat = models.FloatField()
#     lng = models.FloatField()
#     point = geomodels.PointField()

#     def __str__(self):
#         return self.name

# class Advisory(models.Model):
#     crop = models.CharField(max_length=50)
#     region = models.ForeignKey(Region, on_delete=models.CASCADE)
#     message = models.TextField()
#     urgency = models.CharField(max_length=20, choices=[
#         ("low", "Low"), ("medium", "Medium"), ("high", "High"), ("critical", "Critical")
#     ])
#     date = models.DateField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.crop} - {self.urgency}"

# class ServiceProvider(models.Model):
#     name = models.CharField(max_length=100)
#     specialization = models.CharField(max_length=100)
#     latitude = models.FloatField()
#     longitude = models.FloatField()
#     location = geomodels.PointField()
#     products = models.JSONField()
#     hours = models.CharField(max_length=100)
#     region = models.ForeignKey(Region, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.name
