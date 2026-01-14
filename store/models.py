from django.db import models
from category.models import Category
from django.urls  import reverse
# Create your models here.
class product(models.Model):
    product_name=models.CharField(max_length=50)
    slug = models.SlugField(unique=True,max_length=50)
    description = models.TextField(max_length=200)
    price=models.IntegerField()
    images=models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


    def get_url(self):
        return reverse('product_detail',args=[self.category.slug,self.slug])

    def __str__(self):
        return self.product_name

