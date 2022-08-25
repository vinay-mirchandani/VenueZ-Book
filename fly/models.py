from django.db import models

# Create your models here.

"""class Area(models.Model):
    area_id = models.AutoField(primary_key = True)
    area_name = models.CharField(null=False, max_length=20)

    class Meta:
        db_table = "area"


class Customer(models.Model):
    cid = models.AutoField(primary_key=True)
    cname = models.CharField(null=False, max_length=20)
    cemail = models.EmailField(unique=True, max_length=30)
    contact = models.IntegerField(max_length=13)
    cpass = models.CharField(max_length=20)
   
    reg_date = models.DateField()
    models.FileField()
    area_id =models.ForeignKey(Area, on_delete=models.PROTECT)

    class Meta:
        db_table = "customer"
"""


#Admin-table

class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    admin_name = models.CharField(null=False, max_length=20)
    email = models.EmailField(null=False, max_length=20)
    password = models.CharField(null=False, max_length=30)
    contact = models.IntegerField(null=False)
    otp = models.CharField(max_length=10, null=True)
    otp_used = models.IntegerField()

    class Meta:
        db_table = "Admin"


#Area-table

class Area(models.Model):
    area_id = models.AutoField(primary_key=True)
    area_name = models.CharField(null=False, max_length=15)
    pincode = models.IntegerField(null=False)

    class Meta:
        db_table = "Area"


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(null=False, max_length=20)
    email = models.EmailField(null=False, max_length=100)
    password = models.CharField(null=False, max_length=30)
    contact = models.IntegerField(null=True)
    area_id = models.ForeignKey(Area, on_delete=models.PROTECT)
    otp = models.CharField(max_length=10, null=False)
    otp_used = models.IntegerField()

    class Meta:
        db_table = "User"


class Services(models.Model):
    service_id = models.AutoField(primary_key=True)
    service_type = models.CharField(null=False, max_length=20)

    class Meta:
        db_table = "Services"




    #booking_table



#category_table

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(null=False, max_length=15)

    class Meta:
        db_table = "Category"


class Owner(models.Model):
    owner_id = models.AutoField(primary_key=True)
    owner_name = models.CharField(null=False, max_length=20)
    owner_email = models.EmailField(null=False, max_length=100)
    owner_password = models.CharField(null=False, max_length=30)
    owner_contact = models.IntegerField(null=True)
    area_id = models.ForeignKey(Area, on_delete=models.PROTECT)
    otp = models.CharField(max_length=10, null=False)
    otp_used = models.IntegerField()

    class Meta:
        db_table = "Owner"


class Hall(models.Model):
    hall_id = models.AutoField(primary_key=True)
    hall_name = models.CharField(null=False, max_length=15)
    contact = models.IntegerField(null=False)
    address = models.CharField(null=True, max_length=100)
    h_path = models.CharField(max_length=200)
    hall_desc = models.CharField(max_length=1000)
    category_id = models.ForeignKey(Category, on_delete=models.PROTECT)
    area_id = models.ForeignKey(Area, on_delete=models.PROTECT)
    owner_id = models.ForeignKey(Owner, on_delete=models.PROTECT)

    class Meta:
        db_table = "Hall"


class Packages(models.Model):
    package_id = models.AutoField(primary_key=True)
    package_name = models.CharField(null=False, max_length=10)
    package_type = models.CharField(null=False, max_length=20)
    package_desc = models.CharField(null=False, max_length=30)
    package_price = models.IntegerField(null=False)
    hall_id = models.ForeignKey(Hall, on_delete=models.PROTECT)
    service_id = models.ForeignKey(Services, on_delete=models.PROTECT)

    class Meta:
        db_table = "Packages"


class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    booking_date = models.DateTimeField(null=False, auto_now=True)
    total = models.IntegerField(null=False)
    payment_status = models.IntegerField(null=False)
    order_status = models.IntegerField(null=False)
    req_date = models.DateField(null=False)
    package_id = models.ForeignKey(Packages, on_delete=models.PROTECT)
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
    owner_id = models.ForeignKey(Owner, on_delete=models.PROTECT)





    class Meta:
        db_table = "Booking"


class Feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    feedback_date = models.DateField(null=False)
    description = models.CharField(null=False, max_length=30)
    rate = models.IntegerField(5)
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
    hall_id = models.ForeignKey(Hall, on_delete=models.PROTECT)

    class Meta:
        db_table = "Feedback"


class Gallery(models.Model):
    gallery_id = models.AutoField(primary_key=True)
    g_path = models.CharField(max_length=200)
    hall_id = models.ForeignKey(Hall, on_delete=models.PROTECT)

    class Meta:
        db_table = "Gallery"
        
        












