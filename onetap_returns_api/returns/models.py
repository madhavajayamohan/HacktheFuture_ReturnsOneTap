from django.db import models

class ProductCondition(models.TextChoices):
    NEW = "NEW", "Unused"
    LIGHT_USE = "LIGHT_USE", "Lightly Used"
    MOD_USE = "MOD_USE", "Moderately Used"
    HEAVY_USE = "H_USE", "Heavily Used"
    USER_DAMAGED = "USER_DAMAGED", "Damaged by User"
    MAN_DEFECT = "MAN_DEFECT", "Manufacturing Defect"


class Products(models.Model):
    class ProductClasses(models.TextChoices):
        apparel = "apparel", "Apparel"
        elec = "elec", "Electronics"
        home_goods = "home_goods", "Home Goods"
        personal_care = "personal_care", "Beauty & Personal Care"
        toys = "toys", "Toys & Games"
        media = "media", "Books & Media"
        health = "health", "Health & Fitness"
        auto = "auto", "Automotive"
        office = "office", "Office Supplies"
        pet = "pet", "Pet Supplies"
        other = "other", "Other"

    product_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    product_type = models.CharField(max_length=100, choices=ProductClasses.choices)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    stock = models.IntegerField()

class Customer(models.Model):
    cust_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

class OrderHistory(models.Model):
    order_id = models.AutoField(primary_key=True)

    purchase_date = models.DateTimeField()

    cust_id = models.ForeignKey(
        Customer,  # The related model
        on_delete=models.CASCADE,  # What happens when the related object is deleted
        related_name='orders'
    )

    prod_id = models.ForeignKey(
        Products,  # The related model
        on_delete=models.DO_NOTHING,  # What happens when the related object is deleted
        related_name='orders'
    )

class ReturnRequest(models.Model):
    class ReturnStatus(models.TextChoices):
        COMPLETED = "completed", "Completed"
        IN_PROGRESS = "inpr", "In Progress"
        REJECTED = "rej", "Rejected"

    ret_req_id = models.AutoField(primary_key=True)

    cust_id = models.ForeignKey(
        Customer,  # The related model
        on_delete=models.DO_NOTHING,  # What happens when the related object is deleted
        related_name='return_request'
    )

    order_id = models.ForeignKey(
        OrderHistory,  # The related model (OrderHistory)
        on_delete=models.DO_NOTHING,  # What happens when the related object is deleted
        related_name='return_requests'  # Plural for related_name
    )

    prod_id = models.ForeignKey(
        Products,  # The related model (Products)
        on_delete=models.DO_NOTHING,  # What happens when the related object is deleted
        related_name='return_requests'  # Plural for related_name
    )

    image = models.ImageField(upload_to='product_images/')

    ret_reason = models.TextField()

    request_status = models.CharField(max_length=50, choices=ReturnStatus.choices)








