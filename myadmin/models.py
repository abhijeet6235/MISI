
from django.db import models
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import reverse
from rest_framework.authtoken.models import Token
from django.conf import settings

from django import dispatch

# Create your models here.

class railwayLocationMaster(models.Model):
    rly_unit_code = models.AutoField(primary_key=True)
    location_code = models.CharField(max_length=10,null=True)
    location_type = models.CharField(max_length=5,null=True)
    location_description = models.CharField(max_length=50)
    parent_location_code = models.CharField(max_length=10)  
    last_update = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=30,null=True)
    station_code= models.CharField(max_length=5,null=True)
    rstype= models.CharField(max_length=15,null=True)
    location_type_desc= models.CharField(max_length=10,null=True)
# add pin code linking

class empmast(models.Model):
    empno=models.CharField(max_length=20,primary_key=True)
    empname=models.CharField(max_length=50,null=True)
    birthdate=models.DateField(null=True)
    appointmentdate=models.DateField(null=True)
    sex=models.CharField(max_length=10,null=True)
    marital_status=models.CharField(max_length=10,null=True)
    decode_paycategory=models.CharField(max_length=50,null=True)
    billunit=models.CharField(max_length=50,null=True)
    service_status=models.CharField(max_length=50,null=True)
    emp_status=models.CharField(max_length=50,null=True)
    rectt_category=models.CharField(max_length=50,null=True)
    payband=models.CharField(max_length=10,null=True)
    scalecode=models.CharField(max_length=50,null=True)
    pc7_level=models.CharField(max_length=10,null=True)
    payrate=models.CharField(max_length=50,null=True)
    office=models.CharField(max_length=50,null=True)
    office_orderno=models.CharField(max_length=100,null=True)
    station_des=models.CharField(max_length=50,null=True)
    emptype=models.CharField(max_length=10,null=True)
    medicalcode=models.CharField(max_length=50,null=True)
    tradecode=models.CharField(max_length=50,null=True)
    dept_desc=models.CharField(max_length=50,null=True)
    parentshop=models.CharField(max_length=50,null=True)
    shopno=models.CharField(max_length=50,null=True)
    desig_longdesc=models.CharField(max_length=50,null=True)
    wau=models.CharField(max_length=50,null=True)
    inc_category=models.CharField(max_length=50,null=True)
    emp_inctype=models.CharField(max_length=50,null=True)
    parent = models.CharField(max_length=50, blank=True, null=True)
    role = models.CharField(max_length=500, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    contactno = models.CharField(max_length=10, blank=True, null=True)
    ticket_no = models.CharField(max_length=12, blank=True, null=True)
    idcard_no= models.CharField(max_length=15, blank=True, null=True)
    shop_section = models.CharField(max_length = 9,null = True)
    division_id=models.CharField(max_length = 9,null = True)
    rly_unit_code=models.ForeignKey('railwayLocationMaster', on_delete=models.CASCADE, null=True)
    # new
    profile_modified_by = models.CharField(max_length=20, blank=True, null=True)
    profile_modified_on=models.DateField(auto_now=True,null=True,blank=True)
    date_of_promotion=models.DateField(null=True)
    date_of_joining=models.DateField(null=True)

class departMast(models.Model):
    
    department_code = models.CharField(primary_key=True, max_length =10)
    department_name=models.CharField(null = True,max_length =50, blank=True,unique=True)
    rly_unit_code=models.ForeignKey('railwayLocationMaster', on_delete=models.CASCADE, null=True)
    delete_flag=models.NullBooleanField(default=False,null=True)
    modified_by = models.CharField( max_length=20, blank=True, null=True)
    modified_on=models.DateTimeField(auto_now=True, null=True)
    created_on=models.DateTimeField(auto_now_add=True,null=True)


class Post_master(models.Model):
    post_id = models.AutoField(primary_key=True)
    department_code=models.ForeignKey('departMast', on_delete=models.CASCADE, null=True)
    post_desc= models.CharField(max_length=50, blank=True, null=True)
    rly_unit_code=models.ForeignKey('railwayLocationMaster', on_delete=models.CASCADE, null=True)
    delete_flag=models.BooleanField(default=False)
    modified_by = models.CharField( max_length=20, blank=True, null=True)
    modified_on=models.DateTimeField(auto_now=True, null=True)
    created_on=models.DateTimeField(auto_now_add=True,null=True)


class Level_Desig(models.Model):
    id=models.AutoField(primary_key=True)  
    cat_id=models.IntegerField(null=True)    
    designation=models.CharField(max_length=100,null=True)  
    department=models.CharField(max_length=50,null=True)   
    effectdate=models.CharField(max_length=20,null=True)
    un_officer_id=models.IntegerField(null=True)
    level=models.CharField(max_length=2,null=True)
    designation_code = models.CharField(max_length=15,null=True)
    parent_desig_code= models.CharField(max_length=15,null=True)
    department_code=models.ForeignKey('departMast', on_delete=models.CASCADE, null=True)
    rly_unit=models.CharField(max_length=15,null=True)
    pc7_level = models.IntegerField(null=True, blank=True)
    


class roless(models.Model):
    role = models.CharField(primary_key=True, max_length=50)
    parent = models.CharField(max_length=50, blank=True, null=True)
    # department_id=models.ForeignKey('department_master', on_delete=models.CASCADE, null=True)
    rly_unit=models.CharField(max_length=50, blank=True, null=True)
    modified_by = models.CharField( max_length=20, blank=True, null=True)
    modified_on=models.DateTimeField(auto_now=True,null=True,blank=True)
    created_on=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    delete_flag=models.NullBooleanField(default=False,null=True)
    department_code=models.ForeignKey('departMast', on_delete=models.CASCADE, null=True)
    designation_code= models.CharField( max_length=20, blank=True, null=True)
    role_code = models.CharField( max_length=5, blank=True, null=True)
    shop_code=models.CharField(null = True,max_length =50)



class Shop_section(models.Model):
    
    section_code = models.CharField( max_length =10)
    section_id = models.CharField(primary_key=True,max_length =10)
    section_desc = models.CharField(null = True,max_length =150)
    shop_code = models.CharField(null = True,max_length =50)
    shop_id = models.CharField(null = True,max_length =50)
    flag = models.CharField(null = True,max_length =1)
    rly_unit_code=models.CharField(max_length =3,null=True,blank=True)
    department_code=models.ForeignKey('departMast', on_delete=models.CASCADE, null=True)
    modified_by = models.CharField( max_length=20, blank=True, null=True)
    modified_on=models.DateTimeField(auto_now=True,null=True,blank=True)
    created_on=models.DateTimeField(auto_now_add=True,null=True,blank=True)

#     class Meta:
        
#         db_table = 'myadmin_shop_section'


class custom_menu(models.Model):
    m_id=models.IntegerField(null=True)
    menu=models.CharField(max_length=50,null=True)
    url=models.CharField(max_length=100,null=True)
    perent_id=models.IntegerField(null=True)
    role=models.CharField(max_length=200,null=True)


class empmastnew(models.Model):
    sno = models.IntegerField(primary_key=True)
    emp_id=models.ForeignKey(empmast, on_delete=models.CASCADE)
    shop_section = models.CharField(null = True,max_length =50)


class locationMaster(models.Model):
    pincode = models.IntegerField(primary_key=True)
    district = models.CharField(max_length=30)
    state = models.CharField(max_length=20)
    city  = models.CharField(max_length=50, default="NA")


    class Meta:
        db_table = 'locationMaster'

#change name to headquarteradminmater
class headquarterMaster(models.Model):
    headquarter_code = models.BigAutoField(primary_key=True)
 
    headquarter_address = models.CharField(max_length=100)
    pincode = models.ForeignKey(locationMaster, on_delete=models.CASCADE)
    headquarter_admin = models.CharField(max_length=30)
    admin_mobile = models.BigIntegerField(unique=True)
   
   
    # admin_phone = models.BigIntegerField(null=True)
    admin_phone = models.CharField(max_length=12,null=True)
    admin_email = models.EmailField(unique=True)
    headquarter_rly = models.ForeignKey(railwayLocationMaster, on_delete=models.CASCADE)
    headquarter_status = models.CharField(max_length=10)

    def _str_(self):
        return self.admin_email

    class Meta:
        db_table = 'headquarterMaster'

class divisonMaster(models.Model):
    divison_code = models.BigAutoField(primary_key=True)
 
    divison_address = models.CharField(max_length=100)
    pincode = models.ForeignKey(locationMaster, on_delete=models.CASCADE)
    divison_admin = models.CharField(max_length=30)
    admin_mobile = models.BigIntegerField(unique=True)
   
   
    # admin_phone = models.BigIntegerField(null=True)
    admin_phone = models.CharField(max_length=12,null=True)
    admin_email = models.EmailField(unique=True)
    divison_rly = models.ForeignKey(railwayLocationMaster, on_delete=models.CASCADE)
    divison_status = models.CharField(max_length=10)

    def _str_(self):
        return self.admin_email

    class Meta:
        db_table = 'divisonMaster'



