from django.db import models

# Create your models here.
class AddressModel(models.Model):
        country = models.CharField(max_length=100, default="India")
        state = models.CharField(max_length=100, default=None)
        city = models.CharField(max_length=100, default=None)
        pincode = models.CharField(max_length=8, default=None)
        landmark = models.CharField(max_length=100, default=None)
        house_no = models.CharField(max_length=100, default=None)
        area = models.CharField(max_length=200, default=None)
        landmark = models.CharField(max_length=200, default=None)
        street = models.CharField(max_length=200, default=None)
        def __str__(self):
                return self.city
        
        def get_id(self):
                return self.id

class NGOModel(models.Model):
        name = models.CharField(max_length=200, default=None)
        banner_image_url = models.CharField(max_length=200, default=None, null=True)
        admin_name = models.CharField(max_length=100, default=None)
        contact_number = models.CharField(max_length=100, default=None)
        email = models.CharField(max_length=200, default=None)
        password = models.CharField(max_length=100, default=None)
        website_url = models.CharField(max_length=200, default=None, null=True)
        address = models.OneToOneField(AddressModel, on_delete=models.SET_NULL, null=True)
        username = models.CharField(max_length=100, default=None, null=True)
        location_url = models.TextField(default=None, null=True)
        ngo_type = models.CharField(max_length=50, default=None, null=True)
        activation_status = models.BooleanField(default=True)
        verified = models.BooleanField(default=False)

        def __str__(self):
                return self.name
        
        def get_id(self):
                return self.id

class VolunteerModel(models.Model):
        full_name = models.CharField(max_length=200, default=None)
        username = models.CharField(max_length=200, default=None, null=True)
        password = models.CharField(max_length=200, default=None)
        email = models.CharField(max_length=200, default=None)
        contact_number = models.CharField(max_length=200, default=None)
        address = models.OneToOneField(AddressModel, on_delete=models.SET_NULL, null=True)
        pre_areas = models.CharField(max_length=200, default=None, null=True)
        points = models.CharField(max_length=50, default=None, null=True)
        activation_status = models.BooleanField(default=True)
        NGO_model = models.ForeignKey(NGOModel, default=None, on_delete=models.SET_NULL, null=True)
        verified = models.BooleanField(default=False)

        def __str__(self):
                return self.email
        
        def get_id(self):
                return self.id

class FoodDonorModel(models.Model):
        name = models.CharField(max_length=200, default=None)
        donor_type = models.CharField(max_length=100, default=None)
        username = models.CharField(max_length=200, default=None, null=True)
        password = models.CharField(max_length=200, default=None)
        email = models.CharField(max_length=200, default=None)
        contact_number = models.CharField(max_length=200, default=None)
        address = models.OneToOneField(AddressModel, on_delete=models.SET_NULL, null=True)
        location_url = models.TextField(default=None, null=True)
        verified = models.BooleanField(default=False)
        activation_status = models.BooleanField(default=True)

        def __str__(self):
                return self.name
        
        def get_id(self):
                return self.id
