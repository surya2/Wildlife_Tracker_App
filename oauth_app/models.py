from django.db import models
from django_google_maps import fields as map_fields

# from: https://pypi.org/project/django-google-maps/
class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    google_id = models.CharField(max_length=200)
    is_admin = models.BooleanField(default=False)
    def __str__(self):
        return self.email

class Wildlife(models.Model):
    latitude = models.FloatField(null=True, default=0)
    longitude = models.FloatField(null=True, default=0)
    address = map_fields.AddressField(max_length=200)
    name = models.CharField(max_length=200, null=True)
    image = models.ImageField(upload_to='wildlife_images/', null=True, blank=True)

    def __str__(self):
        return self.name

class UploadImage(models.Model):
    image = models.ImageField(upload_to='wildlife_images/', null=True, blank=True)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wildlife = models.ForeignKey(Wildlife, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approval_statuses = (
        (0, 'Declined'),
        (1, 'Pending'),
        (2, 'Approved'),
    )
    approval_status = models.IntegerField(default=1, choices=approval_statuses)
    decline_reason = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    posting_name = models.CharField(null=True, max_length=200)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # below added from https://djangocentral.com/creating-comments-system-with-django/
    active = models.BooleanField(default=False)
    # also defined a name and email
    #name = models.TextField()
    #email = user.email
    
    class Meta:
        # 'created_on' changed to match 'created_at'
        ordering = ['created_at']

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    reacted_at = models.DateTimeField(auto_now_add=True)
    like = models.BooleanField(default=True)

class SavedPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} saved {self.post.title}"


    