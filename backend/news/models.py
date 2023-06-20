from django.db import models

class News(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField(max_length=200)
    date = models.DateField()
    image = models.ImageField(upload_to='news/images')
    
    

    def __str__(self):
        return self.title
