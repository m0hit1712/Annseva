from django.db import models

# Create your models here.
class FoodModel(models.Model):
        approx_weight = models.IntegerField(default=None)
        num_people = models.IntegerField(default=None)

        def __str__(self):
                return str(self.approx_weight)
        
        def get_id(self):
                return self.id

class RequestLocation(models.Model):
        content = models.TextField(default=None)
        address = models.CharField(max_length=2000, default=None)
        contact = models.CharField(max_length=12, default=None)
        num_people = models.IntegerField(default=None)
        ngo_username = models.CharField(max_length=200, default=None)
        expiration_date = models.DateTimeField(default=None)
        ngo_id = models.CharField(max_length=20, default=None, null=True)
        location_url = models.TextField(default=None)

        def __str__(self):
                return self.ngo_username
        
        def get_id(self):
                return self.id

class PostModel(models.Model):
        sender_id = models.CharField(max_length=10, default=None)
        content = models.TextField(default=None)
        packaging = models.BooleanField(default=False)
        date_time = models.DateTimeField(auto_now_add=True)
        pick_up_time = models.TimeField(default=None, null=True)
        dead_time = models.TimeField(default=None)
        status = models.CharField(max_length=100, default="Active")
        food_model = models.OneToOneField(FoodModel, on_delete=models.SET_NULL, null=True)
        receiver = models.CharField(max_length=100, default=None, null=True)
        location_url = models.TextField(default=None, null=True)
        destination = models.OneToOneField(RequestLocation, on_delete=models.SET_NULL, null=True)


class CommentModel(models.Model):
        commenter = models.CharField(max_length=10, default=None)
        date_time = models.DateTimeField(auto_now_add=True)
        content = models.CharField(max_length=400, default=None)
        post_model = models.ForeignKey(PostModel, on_delete=models.CASCADE)

        def __str__(self):
                return self.commenter + "at " + self.post_model.sender_id + "'s post"
        
        def get_id(self):
                return self.id
