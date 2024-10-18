from django.db import models
import uuid




class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    image = models.ImageField(upload_to='blog/', default="blog1.jpeg")
    intro = models.TextField()
    category = models.CharField(max_length=100, null=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    tag = models.CharField(max_length=400, null=True, blank=True)


    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return self.slug
    
