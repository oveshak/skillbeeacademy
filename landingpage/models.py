from django.db import models
from ckeditor.fields import RichTextField

from lmsfeatures.models import Courses
from solo.models import SingletonModel

    
#valid models
class Product(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', default='products/default.jpg')  # Add this field
    course = models.ForeignKey(Courses,on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self):
        return self.name
class ExtraCharges(models.Model):
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    advance_payable = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Purchase(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('PARTIAL', 'Partial'),
        ('PURCHASE', 'Purchase'),
    ]

    name = models.CharField(max_length=255)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES,default="Pending")
    products = models.ManyToManyField(Product)
    extra_charges = models.ManyToManyField(ExtraCharges)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_id = models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)

    # def save(self, *args, **kwargs):
    #     # Calculate total amount
    #     product_total = sum([product.price for product in self.products.all()])
    #     extra_charges_total = sum([charge.amount for charge in self.extra_charges.all()])
    #     self.total_amount = product_total + extra_charges_total
    #     super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.payment_status}"
class BkashSettings(models.Model):  
    app_key = models.CharField(max_length=100)
    app_secret = models.CharField(max_length=100)
    # sandbox = models.BooleanField(default=True)
class BkashConfig(SingletonModel):
    # username =  models.CharField(max_length=100,null=True,blank=True)
    # password =  models.CharField(max_length=100,null=True,blank=True)
    app_key = models.CharField(max_length=100)
    app_secret = models.CharField(max_length=100)
    sandbox = models.BooleanField(default=True)
class BkashConfiguration(SingletonModel):
    username =  models.CharField(max_length=100,null=True,blank=True)
    password =  models.CharField(max_length=100,null=True,blank=True)
    app_key = models.CharField(max_length=100)
    app_secret = models.CharField(max_length=100)
    sandbox = models.BooleanField(default=True)

class Templates(SingletonModel):
    template_code = RichTextField()

    def __str__(self):
        return "Template Settings"
class Gallery(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to="images/",null=True,blank=True)
class Theme(models.Model):
    title = models.CharField(max_length=255)
    css_code = RichTextField(blank=True, null=True)  # CKEditor for CSS
    body_content = RichTextField(blank=True, null=True)  # CKEditor for Body Content
    js_code = RichTextField(blank=True, null=True)  # CKEditor for JS Code

    def __str__(self):
        return self.title
