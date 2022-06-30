from django.db import models
from asyncio.windows_events import NULL
from inspects import managers
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.core.exceptions import ValidationError
import datetime
from django.utils import timezone
from .choices import INSPECTION_TYPE
from myadmin.models import Level_Desig
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




    
# class Level_Desig(models.Model):
#     id=models.AutoField(primary_key=True)  
#     cat_id=models.IntegerField(null=True)    
#     designation=models.CharField(max_length=100,null=True)  
#     department=models.CharField(max_length=50,null=True)   
#     effectdate=models.CharField(max_length=20,null=True)
#     un_officer_id=models.IntegerField(null=True)
#     level=models.CharField(max_length=2,null=True)
#     designation_code = models.CharField(max_length=15,null=True)
#     parent_desig_code= models.CharField(max_length=15,null=True)
#     department_code=models.ForeignKey('departMast', on_delete=models.CASCADE, null=True)
#     rly_unit=models.CharField(max_length=15,null=True)
#     pc7_level = models.CharField(max_length=2,null=True)
    



class departMast(models.Model):
    
    department_code = models.CharField(primary_key=True, max_length =10)
    department_name=models.CharField(null = True,max_length =50, blank=True,unique=True)
    rly_unit_code=models.ForeignKey('railwayLocationMaster', on_delete=models.CASCADE, null=True)
    delete_flag=models.BooleanField(default=False)
    modified_by = models.CharField( max_length=20, blank=True, null=True)
    modified_on=models.DateTimeField(auto_now=True, null=True)
    created_on=models.DateTimeField(auto_now_add=True,null=True)



class error_Table(models.Model):
    log_no=models.BigAutoField(primary_key=True)
    fun_name=models.CharField(max_length=255,null=True,blank=True)
    user_id=models.CharField(max_length=40,null=True,blank=True)
    err_details=models.TextField(null=True,blank=True)
    err_date=models.DateField(auto_now_add=True)

    class meta:
        db_table="error_Table"
#till here Ritika 02-09

class MyUser(AbstractBaseUser):

    username = models.CharField(
        max_length=50, blank=True, null=True)
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    aadhaar_no = models.CharField(max_length=12, null=True)
    email = models.EmailField(verbose_name='email address', unique=True)
    personal_emailID=  models.EmailField(verbose_name='email address', unique=True,null=True)
    official_mobileNo = models.CharField(max_length=10, unique=True,null=True)
    personal_mobileNo= models.CharField(max_length=10, unique=True,null=True)
    faxNo = models.CharField(max_length=10, unique=True,null=True)
    date_of_birth = models.DateField(null=True)
    user_role = models.CharField(max_length=30)

    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    last_update = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = managers.MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['mobile_no', ]

    def __str__(self):
        return self.email

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

class Inspection_details(models.Model):
    inspection_no=models.BigAutoField(primary_key=True)
    inspection_note_no=models.CharField(max_length=40, blank=True, null=True)
    inspection_officer=models.CharField(max_length=20, blank=False, null=True)
    inspection_title=models.CharField(max_length=200, blank=False, null=True)
    zone=models.CharField(max_length=10, blank=False, null=False)
    division=models.CharField(max_length=10, blank=False, null=False)
    dept=models.CharField(max_length=20, blank=False, null=True)
    location=models.CharField(max_length=20, blank=False, null=False)
    inspected_on=models.DateField(auto_now=False, null=False)
    target_date=models.DateField(null=True)
    modified_on=models.DateTimeField(auto_now=False, null=True)
    created_on=models.DateTimeField(auto_now=False, null=True)
    modified_by=models.CharField(max_length=10, blank=False, null=True)
    created_by=models.CharField(max_length=10, blank=False, null=True)
    report_path=models.CharField(max_length=50, blank=False, null=True)
    #new amisha
    status_flag=models.IntegerField(null=True)



class Item_details(models.Model):
    item_no=models.BigAutoField(primary_key=True)   
    item_title=models.CharField(max_length=20, blank=False, null=True)
    inspection_no=models.ForeignKey('Inspection_details', on_delete=models.CASCADE, null=True)
    status=models.CharField(max_length=10, blank=False, null=True)
    status_flag=models.IntegerField(blank=False, null=True)
    observation=models.CharField(max_length=500, blank=False, null=True)
    modified_on=models.DateTimeField(auto_now=False, null=True)
    created_on=models.DateTimeField(auto_now=False, null=True)
    modified_by=models.CharField(max_length=10, blank=False, null=True)
    created_by=models.CharField(max_length=10, blank=False, null=True)
    target_date=models.DateField(null=True)
    item_subtitle=models.CharField(max_length=300, blank=False, null=True)
    type=models.CharField(max_length=3, blank=False, null=True)
    item_link=models.CharField(max_length=20, blank=False, null=True)
    des_id=models.CharField(max_length=8, blank=False, null=True)

class Marked_Officers(models.Model):
    marked_no=models.BigAutoField(primary_key=True)
    marked_to=models.ForeignKey('Designation_Master', on_delete=models.CASCADE, null=True)
    item_no=models.ForeignKey('Item_details', on_delete=models.CASCADE, null=True)
    compliance=models.CharField(max_length=50, blank=False, null=True)
    compliance_recieved_on=models.DateTimeField(auto_now=False, null=True)
    modified_on=models.DateTimeField(auto_now=False, null=True)
    created_on=models.DateTimeField(auto_now=False, null=True)
    modified_by=models.CharField(max_length=10, blank=False, null=True)
    created_by=models.CharField(max_length=10, blank=False, null=True)
    #new amisha
    myuser_id=models.ForeignKey('MyUser', on_delete=models.CASCADE, null=True)

class Marked_Officers_forward(models.Model):
    marked_no_forward=models.BigAutoField(primary_key=True)
    marked_to_forward=models.ForeignKey('Designation_Master', on_delete=models.CASCADE, null=True)
    marked_no=models.ForeignKey('Marked_Officers', on_delete=models.CASCADE, null=True)
    compliance_forward=models.CharField(max_length=50, null=True)
    compliance_recieved_on_forward=models.DateTimeField(auto_now=False, null=True)
    modified_on_forward=models.DateTimeField(auto_now=False, null=True)
    created_on_forward=models.DateTimeField(auto_now=False, null=True)
    modified_by_forward=models.CharField(max_length=10, blank=False, null=True)
    created_by_forward=models.CharField(max_length=10, blank=False, null=True)
    myuser_id=models.ForeignKey('MyUser', on_delete=models.CASCADE, null=True)

class roles(models.Model):
    role = models.CharField(primary_key=True, max_length=50)
    parent = models.CharField(max_length=50, blank=True, null=True)
    # department_id=models.ForeignKey('department_master', on_delete=models.CASCADE, null=True)
    rly_unit=models.CharField(max_length=50, blank=True, null=True)
    modified_by = models.CharField( max_length=20, blank=True, null=True)
    modified_on=models.DateTimeField(auto_now=True,null=True,blank=True)
    created_on=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    delete_flag=models.BooleanField(default=False)
    department_code=models.ForeignKey('departMast', on_delete=models.CASCADE, null=True)
    designation_code= models.CharField( max_length=20, blank=True, null=True)
    role_code = models.CharField( max_length=5, blank=True, null=True)
    shop_code=models.CharField(null = True,max_length =50)
    class Meta:
        
        db_table = 'dlw_roles'



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
    op_read = models.BooleanField(default=True)
    op_create= models.BooleanField(default=False)
    op_delete= models.BooleanField(default=False)
    op_update= models.BooleanField(default=False)
    shop_section = models.CharField(max_length = 9,null = True)
    # new
    profile_modified_by = models.CharField( max_length=20, blank=True, null=True)
    profile_modified_on=models.DateField(null=True,blank=True)
    date_of_promotion=models.DateField(null=True)
    date_of_joining=models.DateField(null=True)
    myuser_id=models.ForeignKey('MyUser', on_delete=models.CASCADE, null=True)
    rly_id=models.ForeignKey('railwayLocationMaster', on_delete=models.CASCADE, null=True,related_name='empmast_rly_id')
    div_id=models.ForeignKey('railwayLocationMaster', on_delete=models.CASCADE, null=True,related_name='empmast_div_id')

class Post_master(models.Model):
    post_id = models.AutoField(primary_key=True)
    department_code=models.ForeignKey('departMast', on_delete=models.CASCADE, null=True)
    post_desc= models.CharField(max_length=50, blank=True, null=True)
    rly_unit_code=models.ForeignKey('railwayLocationMaster', on_delete=models.CASCADE, null=True)
    delete_flag=models.BooleanField(default=False)
    modified_by = models.CharField( max_length=20, blank=True, null=True)
    modified_on=models.DateTimeField(auto_now=True, null=True)
    created_on=models.DateTimeField(auto_now_add=True,null=True)





class Designation_Master(models.Model):
    designation_master_no=models.BigAutoField(primary_key=True)
    master_name=models.CharField(max_length=40, blank=False, null=False)
    master_email=models.EmailField(verbose_name='email address', unique=True)
    

class HRMS(models.Model):
    empno=models.CharField(max_length=20,primary_key=True)
    empname=models.CharField(max_length=50,null=True)
    designation=models.ForeignKey('myadmin.Level_Desig', on_delete=models.CASCADE, null=True)
    pay_level=models.CharField(max_length=10,null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    rly_id=models.ForeignKey('railwayLocationMaster', on_delete=models.CASCADE, null=True,related_name='rly_id')
    div_id=models.ForeignKey('railwayLocationMaster', on_delete=models.CASCADE, null=True,related_name='div_id')


class user_request(models.Model):
    rly_id=models.ForeignKey('railwayLocationMaster', on_delete=models.CASCADE, null=True,related_name='empmast_rly_id1')
    myuser_id=models.ForeignKey('MyUser', on_delete=models.CASCADE, null=True)
    empno=models.BigIntegerField(max_length=12, null=True)
    requestDate=models.DateField(null=True)
    remarks=models.CharField(max_length=200, null=True)
    request_type=models.CharField(max_length=50, null=True)
    status=models.CharField(max_length=20, null=True)




class Inspection_Checklist(models.Model):
    checklist_id=models.AutoField(primary_key=True)  
    checklist_title=models.CharField(max_length=100, blank=False, null=False)
    inspection_type=models.CharField(max_length=15, choices=INSPECTION_TYPE, default = '1' )
    status=models.CharField(max_length=10, blank=False, null=False)
    delete_flag=models.BooleanField(default=False)
    created_by=models.CharField(max_length=12, blank=False, null=True)
    created_on=models.DateTimeField(auto_now_add=True,null=True)
    last_modified_by=models.CharField(max_length=12, blank=False, null=True)
    last_modified_on=models.DateTimeField(auto_now_add=True, null=True)
    


class Inspection_Activity(models.Model):
    activity_id=models.AutoField(primary_key=True)  
    checklist_id=models.ForeignKey('Inspection_Checklist', on_delete=models.CASCADE)
    activities=models.CharField(max_length=200, blank=False, null=False)
    delete_flag=models.BooleanField(default=False)
    created_by=models.CharField(max_length=12, blank=False, null=True)
    created_on=models.DateTimeField(auto_now_add=True, null=True)
    last_modified_by=models.CharField(max_length=12, blank=False, null=True)
    last_modified_on=models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.checklist_id
    

    