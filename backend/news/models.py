from django.db import models

class News(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateField()
    image = models.TextField(max_length=200)
    is_active = models.BooleanField(default=True)
    

    def __str__(self):
        return self.title
