from django.db import models

# Create your models here.
class admin(models.Model):
    id = models.BigAutoField(primary_key=True)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.email

class rol(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
        
class user(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_rol = models.ForeignKey(rol, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    birth_date = models.DateField()

    def __str__(self):
        return self.name
    
class product(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    price = models.FloatField()
    
    def __str__(self):
        return self.name

class store(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class searchHistory(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_user = models.ForeignKey(user, on_delete=models.CASCADE)
    id_product = models.ForeignKey(product, on_delete=models.CASCADE)
    id_store = models.ForeignKey(store, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return self.id_user
    
class suggestion(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_product = models.ForeignKey(product, on_delete=models.CASCADE)
    product_option = models.JSONField()
    store_option = models.JSONField()

    def __str__(self):
        return self.id_user
