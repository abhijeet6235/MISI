from __future__ import division
from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from inspects import models as m1
from myadmin import models
import json


from django.core.mail import EmailMessage
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mass_mail
import math
user = get_user_model()
from datetime import datetime
from inspects.utils import render_to_pdf

from xhtml2pdf import pisa
from django.template.loader import get_template
from .choices import INSPECTION_TYPE

import random
def generateOTP() :
     digits = "0123456789"
     OTP = ""
     for i in range(4) :
         OTP += digits[math.floor(random.random() * 10)]
     return OTP

from django.core.mail import send_mail


def send_otp(request):
    if request.method == 'GET':
        print('iiii_____')
        cuser=request.user
        email=request.GET.get("email")
        print(email)
       
        print(type(email),'-------email------')
        otp=generateOTP()
        print(otp,'___')
        htmlgen = 'Your OTP is '+otp
        #send_mail('OTP request',otp,'crisdlwproject@gmail.com',[email], html_message=htmlgen)
        # send_mail(
        #             'OTP request', #subject
        #              htmlgen, #message body
        #             'mfgcris@cris.org.in', # from email
        #             [email], fail_silently=False, #to email
                   
        #         )  
        return JsonResponse({'otp':otp}, safe = False)
    return JsonResponse({}, safe = False)

def draft_inspection_form(request):
    
    inspection=m1.Inspection_details.objects.filter(status_flag=None).values().order_by('-inspection_no')
    # list1=[]
    # for i in inspection:
    #     temp={}
    #     temp['inspection_note_no']=i['inspection_note_no']
    #     temp['inspection_no']=i['inspection_no']
    #     list1.append(temp)
    # print(list1)    

    return render(request,"draft_inspection.html",{'list1':inspection})


def fetch_email_id(request):
    empno=request.GET.get('empno')
    email_id=request.GET.get('email_id')
    flag=0
    if(m1.HRMS.objects.filter(empno=empno,email=email_id).exists()):
        flag=1
    else:
        flag=0   
        return JsonResponse({'flag':flag})

def fetch_emp(request):
    emp_id=request.GET.get('emp_id')
    print(emp_id)
    if(m1.HRMS.objects.filter(empno=emp_id).exists()):
        # designation_id=m1.HRMS.objects.filter(empno=emp_id)[0].designation_id
        # designation=models.Designation_Master.objects.filter(designation_master_no=designation_id)[0].master_name
        designation=m1.HRMS.objects.filter(empno=emp_id)[0].designation_id
        empname=m1.HRMS.objects.filter(empno=emp_id)[0].empname
        rly_id=m1.HRMS.objects.filter(empno=emp_id)[0].rly_id_id
        div_id=m1.HRMS.objects.filter(empno=emp_id)[0].div_id_id
        print(rly_id,'___________')
        print(div_id,'___________')
        rly_code=m1.railwayLocationMaster.objects.filter(rly_unit_code=rly_id)[0].location_code
        div_code=m1.railwayLocationMaster.objects.filter(rly_unit_code=div_id)[0].location_code
        context={
            'designation':str(designation),
            'empname':str(empname),
            'rly_code':str(rly_code),
            'div_code':str(div_code),
        }
        return JsonResponse(context)
# def signup(request):
#     if request.method == "POST":
#         submit_form=request.POST.get('submit_form')
#         if(submit_form=="submit_form"):
#             empno=request.POST.get('emp_id')
#             empname=request.POST.get('empname')
#             designation=request.POST.get('designation')
#             email_id=request.POST.get('email_id')
#             password=request.POST.get('password')
#             rly_code=request.POST.get('rly_id')
#             rly_id=models.railwayLocationMaster.objects.filter(location_code=rly_code)[0].rly_unit_code
#             div_code=request.POST.get('div_id')
#             div_id=models.railwayLocationMaster.objects.filter(location_code=div_code)[0].rly_unit_code
#             if(user.objects.filter(first_name=empname,email=email_id).exists()):
#                 messages.success(request,'User Already Exists.')
#             else:    
#                 user.objects.create_user(first_name=empname,email=email_id,password=password)
#                 myuser_id=user.objects.filter(first_name=empname,email=email_id)[0].id
#                 print(myuser_id,'___________-')
#                 models.empmast.objects.create(empno=empno,empname=empname,desig_longdesc=designation,email=email_id,myuser_id_id=myuser_id
#                 ,rly_id_id=rly_id,div_id_id=div_id)
#                 # send_mail(
#                 #             'OTP request', #subject
#                 #              htmlgen, #message body
#                 #             'amishu321@gmail.com', # from email
#                 #             [email], fail_silently=False, #to email
                        
#                 #         )
#                 messages.success(request,'User Created successfully.')
#     return render(request,"signup.html")


def signup(request):
    try:
        id=user.objects.filter().order_by('-id')[0].id
        id+=1
        print(id)
        if request.method == "POST":
            submit_form=request.POST.get('submit_form')
            if(submit_form=="submit_form"):
                empno=request.POST.get('emp_id')
                empname=request.POST.get('empname')
                designation=request.POST.get('designation')
                email_id=request.POST.get('email_id')
                password=request.POST.get('password')
                rly_code=request.POST.get('rly_id')
                print('1')
                print(rly_code)
                print(designation)
                div_code=request.POST.get('div_id')
                if div_code=='':
                    rly_id=m1.railwayLocationMaster.objects.filter(location_code=rly_code)[0].rly_unit_code
                else:
                    rly_id=m1.railwayLocationMaster.objects.filter(location_code=div_code)[0].rly_unit_code
                # 
                # div_id=models.railwayLocationMaster.objects.filter(location_code=div_code)[0].rly_unit_code
                print('2')
                print(rly_id)
                if(user.objects.filter(first_name=empname,email=email_id).exists()):
                    messages.success(request,'User Already Exists.')
                else:    
                    print('9')
                    print(empname,email_id)
                    id=user.objects.filter().order_by('-id')[0].id
                    id+=1
                    user.objects.create_user(first_name=empname,email=email_id,password=password, id=id,username=empno)
                    print('hlo')
                    myuser_id=user.objects.filter(first_name=empname,email=email_id)[0].id
                    print(myuser_id,'___________-')
                    # empno=int(empno)
                    m1.user_request.objects.create(empno=empno,myuser_id_id=myuser_id,requestDate=datetime.now(),
                    rly_id_id=rly_id,status='Pending')
                    # models.empmast.objects.create(empno=empno,empname=empname,desig_longdesc=designation,email=email_id,myuser_id_id=myuser_id
                    # ,rly_id_id=rly_id,div_id_id=div_id)
                    # send_mail(
                    #             'OTP request', #subject
                    #              htmlgen, #message body
                    #             'mfgcris@cris.org.in', # from email
                    #             [email], fail_silently=False, #to email
                            
                    #         )
                    messages.success(request,'User Request sent successfully.Kindly ask your admin to authorize your signup request')
        return render(request,"signup.html")
    except Exception as e:
        print(e)
def loginUser(request):
    # try:
        if request.method == "POST":
            _email = request.POST.get('email').strip()
            _password = request.POST.get('password').strip()
            print(_email,'____')
            print(_password,'_____')
            # obj3=models.rkvy_userEnrollment.objects.filter(user_id__email=_email).values('pending_stage')
            # check for existence
            userObj = authenticate(username=_email, password=_password)
            
            

           
            if userObj is not None:
                login(request, userObj)
                print("inside login&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
                print(userObj.username==None)
                print(userObj.username,'000000000')
                print(userObj.is_admin)
                if userObj.user_role == 'rkvy_superadmin':
                    return HttpResponseRedirect('/rkvy_superAdminHome')
                elif userObj.user_role == 'rkvy_headquarteradmin':
                    return HttpResponseRedirect('/rkvy_headquarterAdminHome')
                elif userObj.user_role == 'rkvy_instituteadmin':
                    
                    return HttpResponseRedirect('/rkvy_instituteAdminHome')
                elif userObj.user_role == 'rkvy_instructor':
                    return HttpResponseRedirect('/rkvy_instructorHome')
                elif userObj.is_admin==True and (userObj.username=='' or  userObj.username == None  ):
                    return HttpResponseRedirect('/adminuserHome')
                elif userObj.is_admin==True and models.railwayLocationMaster.objects.filter(rly_unit_code=userObj.username)[0].location_type!='DIV':
                    return HttpResponseRedirect('/zonaluserHome')
                elif userObj.is_admin==True and models.railwayLocationMaster.objects.filter(rly_unit_code=userObj.username)[0].location_type=='DIV':
                    return HttpResponseRedirect('/divisonuserHome')
                else:
                    
                    return HttpResponseRedirect('/userHome')
                    # return render(request,"list_create_inspection_report.html")
                    
            else:
                #change 21-10
                if user.objects.filter(email=_email,is_active=False).exists():
                    messages.error(request, 'Request is not accepted yet.')
                else:
                    messages.error(request, 'Invalid Credentials')#till here 21-10
                #return HttpResponseRedirect('/rkvy_login')
                return render(request, "login2.html")
        print('hhhh')
        return render(request, "login2.html")
def check(request):
    
    mail=request.POST.get('email')
    if user.objects.filter(email=mail).exists() == True:
        status=1
    else:
        status=0
    print(status)
    print(user.objects.filter(email=mail).exists())
    return JsonResponse({'status': status, })
#amisha140622    
def compliance_marked_forward(request):
    if request.method == "GET" and request.is_ajax():
        item_no=request.GET.get('item_no')
        inspection_no=request.GET.get('inspection_no')
        forward_to=request.GET.get('forward_to')
        user_id_forward=m1.empmast.objects.filter(desig_longdesc=forward_to)[0].myuser_id_id
        marked_to_forward=models.Level_Desig.objects.filter(designation=forward_to)[0].id
        id=request.user
        myuser_id=user.objects.filter(email=id)[0].id
        print(myuser_id,'_________________')
        empname=m1.empmast.objects.filter(myuser_id_id=myuser_id)[0].empname
        design=m1.empmast.objects.filter(myuser_id_id=myuser_id)[0].desig_longdesc
        marked_no=m1.Marked_Officers.objects.filter(myuser_id_id=myuser_id,item_no_id=item_no)[0].marked_no
        import datetime
        mark=int(m1.Marked_Officers_forward.objects.last().marked_no_forward)+1 if m1.Marked_Officers_forward.objects.last()!=None else 1
        m1.Marked_Officers_forward.objects.create(marked_no_forward=mark,marked_no_id=marked_no,marked_to_forward_id=marked_to_forward,created_on_forward=datetime.datetime.now(),myuser_id_id=user_id_forward)
        return JsonResponse({})

def compliance_forward_reply(request,item_no):
    print(item_no)
    inspection_no=m1.Item_details.objects.filter(item_no=item_no)[0].inspection_no_id
    cuser=request.user
    myuserid=m1.MyUser.objects.filter(email=cuser).values('id')
    marked_forward=[] 
    if(m1.Marked_Officers.objects.filter(item_no_id=item_no,myuser_id_id=myuserid[0]['id']).exists()):
        marked_no=m1.Marked_Officers.objects.filter(item_no_id=item_no,myuser_id_id=myuserid[0]['id'])[0].marked_no   
        if(m1.Marked_Officers_forward.objects.filter(marked_no_id=marked_no).exists()):
            marked_forward=m1.Marked_Officers_forward.objects.filter(marked_no_id=marked_no).values()
    list1=[]
    for i in marked_forward:
        temp={}
        temp['recieved_on']=i['compliance_recieved_on_forward'].strftime("%d/%m/%y") if i['compliance_recieved_on_forward'] != None else 'pending'
        name=m1.MyUser.objects.filter(id=i['myuser_id_id'])[0].first_name if m1.MyUser.objects.filter(id=i['myuser_id_id']).exists() == True else 'pending'
        temp['marked_to_forward']=name
        temp['reply']=i['compliance_forward'] if i['compliance_forward'] != None else 'pending'
        temp['compliance_recieved_on_forward']=i['compliance_recieved_on_forward'].strftime("%d/%m/%y") if i['compliance_recieved_on_forward'] != None else 'pending'
        list1.append(temp)
    designation=models.Level_Desig.objects.exclude(designation=None).values('designation')
       
    return render(request,"compliance_forward.html",{'list1':list1,'item_no':item_no,'inspection_no':inspection_no,'desig':designation})

def save_data(request):
    if request.method == 'GET':
        ins_id=request.GET.get('ins_id')
        m1.Inspection_details.objects.filter(inspection_no=ins_id).update(status_flag=1)
    return JsonResponse({}, safe = False) 













def getDesignation(request):

    if request.method == "GET" or request.is_ajax():
        dept_1=request.GET.get('dept_1')
        print(dept_1,'_________++++++++++++________________')
          
        division=list(Level_Desig.objects.filter(department=dept_1).values('designation'))
        l=[]
        for i in division:
            l.append(i['designation'])
        print(l)    
        context={
            'division':l,
        } 
        return JsonResponse(context,safe = False)
    return JsonResponse({"success":False}, status = 400)



def admin_inspection_form(request):
    import datetime
    _now = datetime.datetime.now()
    _year = _now.year
    today = datetime.date.today().strftime("%d-%m-%Y")
    rly=railwayLocationMaster.objects.filter(location_type='ZR').values('location_code')
    div=railwayLocationMaster.objects.filter(location_type='DIV').values('location_code')
    dept=departMast.objects.values('department_name')
    listw=empmast.objects.values('empname').order_by('empname').distinct()
   
       
    context={
        't':today,
        'rly':rly,
        'div':div, 
        'dept':dept,
        'listw':listw,
        # 'listw1':listw1,
    }
    
    
    
    return render(request,"admin_inspection.html",context)


def fetch_forward_reply(request):
    print('hi')
    item_no=request.GET.get('item_no')
    print(item_no)
    inspection_no=models.Item_details.objects.filter(item_no=item_no)[0].inspection_no_id
    cuser=request.user
    myuserid=models.MyUser.objects.filter(email=cuser).values('id')
    marked_forward=[] 
    if(models.Marked_Officers.objects.filter(item_no_id=item_no,myuser_id_id=myuserid[0]['id']).exists()):
        marked_no=models.Marked_Officers.objects.filter(item_no_id=item_no,myuser_id_id=myuserid[0]['id'])[0].marked_no   
        if(models.Marked_Officers_forward.objects.filter(marked_no_forward=marked_no).exists()):
            marked_forward=models.Marked_Officers_forward.objects.filter(marked_no_forward=marked_no).values()
    list1=[]
    for i in marked_forward:
        temp={}
        temp['recieved_on']=i['compliance_recieved_on_forward'].strftime("%d/%m/%y")
        name=models.MyUser.objects.filter(id=i['myuser_id_id'])[0].first_name
        temp['marked_to_forward']=name
        temp['reply']=i['compliance_forward']
        temp['compliance_recieved_on_forward']=i['compliance_recieved_on_forward'].strftime("%d/%m/%y")
        list1.append(temp)
    
    return JsonResponse({'list1':list1,'item_no':item_no,'inspection_no':inspection_no}, safe = False)

    

def admin_inspection_form(request):
    import datetime
    _now = datetime.datetime.now()
    _year = _now.year
    today = datetime.date.today().strftime("%d-%m-%Y")
    rly=models.railwayLocationMaster.objects.filter(location_type='ZR').values('location_code')
    div=models.railwayLocationMaster.objects.filter(location_type='DIV').values('location_code')
    dept=models.departMast.objects.values('department_name')
    listw=models.empmast.objects.values('empname').order_by('empname').distinct()
    context={
        't':today,
        'rly':rly,
        'div':div, 
        'dept':dept,
        'listw':listw,
    }
    
    
    
    return render(request,"admin_inspection.html",context)

def compliance_filterdata_ajax(request):
    if request.method == "GET" and request.is_ajax():
        str=request.GET.get('str')

        if(str=='filter'):
            print('b')
            rly_id=request.GET.get('rly_id')
            print(rly_id,'_________________________aaaaaa________________')
            if(rly_id==""):
                list3=models.railwayLocationMaster.objects.filter(location_type='DIV').values('location_code')
            else:    
                list3=models.railwayLocationMaster.objects.filter(location_type='DIV',parent_location_code=rly_id).values('location_code')
            list4=[]
            for i in list3:
                list4.append(i['location_code'])    
            print(list4,'__________________________llllllllll______________')
            return JsonResponse({'div':list4})
        if(str=='reply'):
            cuser=request.user
            myuserid=m1.MyUser.objects.filter(email=cuser).values('id')
            print(cuser,'cuser')
            inspection_id=request.GET.get('inspection_id')
            print(inspection_id,'_________________')
            print(myuserid[0]['id'],'__________________________')
            list1=m1.Inspection_details.objects.filter(inspection_no=inspection_id).values()
            list5=m1.Marked_Officers.objects.filter(item_no__inspection_no_id=inspection_id,myuser_id_id=myuserid[0]['id']).values('item_no_id')
            print('hiiiiiiiiiiiiiiiiii,,,,,')
            print(list5,'_____________')
            list6=[]
            for i in list5:
                list6.append(i['item_no_id'])
            list2=m1.Item_details.objects.filter(item_no__in=list6).values()
            list3=[]
            list4=[]
            for i in list1:
                temp={}
                temp['inspection_no']=i['inspection_no']
                temp['inspection_officer']=i['inspection_officer']
                temp['inspection_title']=i['inspection_title']
                temp['inspection_date']=i['inspected_on'].strftime("%d/%m/%y")
                list3.append(temp)
            for i in list2:
                temp={}
                temp['item_no']=i['item_no']  
                temp['observation']=i['observation']
                temp['compliance']=m1.Marked_Officers.objects.filter(item_no=i['item_no'])[0].compliance
                list4.append(temp)  
            print(list3,'__________________________list3')
            print(list4,'__________________________________list4')    
            return JsonResponse({'idetails':list3,'itemdetails':list4})
        if(str=='save'):
            item_no=request.GET.get('item_no')
            compliance=request.GET.get('compliance')
            m1.Marked_Officers.objects.filter(item_no_id=item_no).update(compliance=compliance)
            return JsonResponse({})    
def compliance_filterdata(request):
    print('a')
    if request.method == "GET" and request.is_ajax():
        print('b')
        div_id=request.GET.get('div_id')
        rly_id=request.GET.get('rly_id')
        dept_id=request.GET.get('dept_id')
        print(dept_id,'__________________________________________________')
        startDate=request.GET.get('startDate')
        print(startDate)
        startDate = datetime.strptime(startDate,'%Y-%m-%d')
        print(startDate)
        endDate=request.GET.get('endDate')
        print(endDate)
        endDate = datetime.strptime(endDate,'%Y-%m-%d')
        print(endDate)
        #inspect_details=models.Inspection_details.objects.filter(zone=rly_id,division=div_id,dept=dept_id,inspected_on__gte=startDate,inspected_on__lte=endDate).values()
        inspect_details=m1.Inspection_details.objects.filter(zone=rly_id,division=div_id,dept=dept_id).values()
        print(inspect_details,'______________')
        list1=[]
        count=1
        for i in inspect_details:
            marked=m1.Marked_Officers.objects.filter(item_no__inspection_no_id=i['inspection_no']).values()
            marked_to = set(mark['myuser_id_id'] for mark in marked)
            temp={}
            temp['sr_no']=count
            temp['inspection_title']=i['inspection_title']
            temp['inspection_no']=i['inspection_no']
            temp['inspection_officer']=i['inspection_officer'] if i['inspection_officer']!=None else ''
            # temp['inspected_on']=', '.join(marked_to)
            temp['inspected_on']=i['inspected_on'].strftime("%d/%m/%y") if i['inspected_on']!=None else ''
            temp['viewed_on']=i['modified_on'].strftime("%d/%m/%y") if i['modified_on']!=None else ''
            temp['file_path']=i['report_path']
            # temp['Complaince_Reaction']=i['compliance_recieved_on']
            list1.append(temp)

        return JsonResponse({'inspect_details':list1})
def compliance_form(request):
    
    list1=models.railwayLocationMaster.objects.filter(location_type='ZR').values('location_code')
    list2=[]
    for i in list1:
        print(i['location_code'],'_________')
        list2.append(i['location_code'])
    list3=models.railwayLocationMaster.objects.filter(location_type='DIV').values('location_code')
    list4=[]
    for i in list3:
        print(i['location_code'],'_________')
        list4.append(i['location_code'])  
    list5=models.departMast.objects.all().values('department_name')
    list6=[]
    for i in list5:
        print(i['department_name'],'_________')
        list6.append(i['department_name'])        
    context={
        'zone':list2 ,
        'division':list4,
        'dept':list6,
    }
    print(list2,'_____________')
    return render(request,'compliance_form.html',context)



def home(request):
    if request.method == "POST":
        firstName=request.POST.get('firstName')
        middleName=request.POST.get('middleName')
        lastName=request.POST.get('lastName')
        email=request.POST.get('official_emailID')
        official_mobileNo=request.POST.get('official_mobileNo')
        personal_emailID=request.POST.get('personal_emailID')
        personal_mobileNo=request.POST.get('personal_mobileNo')
        faxNo=request.POST.get('faxNo')
        aadhaarNo=request.POST.get('aadhaarNo')
        password=request.POST.get('password')
        user.objects.create_user(first_name=firstName,middle_name=middleName,last_name=lastName
        ,email=email,official_mobileNo=official_mobileNo,personal_emailID=personal_emailID,
        personal_mobileNo=personal_mobileNo,faxNo=faxNo,aadhaar_no=aadhaarNo,password=password)
    return render(request, 'home.html')

#furqan
def dash_home(request):
    # data = Inspection.objects.values('zone','dept','officer_name').distinct('dept').distinct('zone')
    total_report = m1.Inspection_details.objects.all()
    # zone_data = Inspection.objects.filter(zone='central zone').distinct()
    # # cz_count = Inspection.objects.filter(zone='central zone').count()
    # ncr_id = Inspection.objects.filter(zone='ncr').count()
    # cz_pend= Inspection.objects.filter(zone='central zone', pending =True).count()
    # cz_completed= Inspection.objects.filter(zone='central zone', pending=False).count()
    report_count = total_report.count()
    # pend_count = Inspection_details.objects.filter(status_flag=0).count()
    # ncr_count = Inspection.objects.filter(zone='ncr').count()
    # cz_count = Inspection.objects.filter(zone='central zone').count()
    # emr_count = Inspection.objects.filter(dept='EMR').count()
    # mfo_count = Inspection.objects.filter(dept='MFO').count()
    
    context = {
      'report_count':report_count}
    #      'cz_count':cz_count,'mfo_count':mfo_count,"data":data,'ncr_id':ncr_id,'zone_data':zone_data,
    #      'cz_pend':cz_pend,'cz_completed':cz_completed
    # }
    
    return render(request, 'dash_home.html',context)

def railway_zone(request):
    data = m1.railwayLocationMaster.objects.filter(location_type='ZR').values('location_description','location_code').order_by('location_code')
    #data1 = m1.railwayLocationMaster.objects.filter(location_type='DIV').values('location_description','location_code')
    list1=[]

        
    for i in data:
        temp={}
        c1=0
        c2=0
        c3=0
        t= m1.Inspection_details.objects.filter(zone=i['location_code']).values('inspection_no')
        if len(t)>0:
            for j in t:
                temp1=m1.Item_details.objects.filter(inspection_no=j['inspection_no']).values()
                for c in temp1:
                    if c['status_flag'] ==1:
                        c1 +=1
                    elif c['status_flag'] ==2:
                        c2+=1
                    elif c['status_flag'] ==3:
                        c3+=1
                        
            temp3=len(temp1)     
        else:
            temp3=0
        
        temp['ins_no']=temp3
        temp['location_description']=i['location_description']
        temp['location_code']=i['location_code']
        temp['c1']= c1
        temp['c2']= c2
        temp['c3']= c3
        list1.append(temp)
    return JsonResponse({'data':list1}, safe=False)

def item_divsion(request):
    data1 = m1.railwayLocationMaster.objects.filter(location_type='DIV').values('location_description','parent_location_code','location_code').order_by('parent_location_code','location_code')
    #print(data1)
    list2=[]
    for i in data1:
        temp1={}
        c1=0
        c2=0
        c3=0
        t1 = m1.Inspection_details.objects.filter(division=i['location_code']).values()
        print(t1)
        if len(t1)>0:
            for j in t1:
               temp2 = m1.Item_details.objects.filter(inspection_no=j['inspection_no']).values()
               for c in temp2:
                    if c['status_flag'] ==1:
                        c1 +=1
                    elif c['status_flag'] ==2:
                        c2+=1
                    elif c['status_flag'] ==3:
                        c3+=1
            temp4 = len(temp2)
        else:
            temp4=0
        
        
        temp1['ins_no']=temp4
        temp1['location_description']=i['location_description']
        temp1['location_code']=i['location_code']
        temp1['parent_location_code']=i['parent_location_code']
        temp1['c1'] = c1
        temp1['c2'] = c2
        temp1['c3'] = c3
        list2.append(temp1)
       
    return JsonResponse({'data1':list2}, safe=False)
#24.06.22
def item_detail_view(request):
    itdv = m1.Item_details.objects.values('inspection_no','inspection_no__inspection_title','inspection_no__dept','inspection_no__inspected_on','status','inspection_no__inspection_officer','target_date','observation', 'item_no') 
    return render(request,'items_dt_view.html', context={'itdv':itdv})
#27-06-22
def item_view_inspect(request, item):
    ivi = m1.Item_details.objects.filter(item_no=item).values('item_no','inspection_no','inspection_no__zone','inspection_no__dept','inspection_no__location','item_title','modified_on','modified_by','status_flag','status','created_on','observation','marked_officers','created_by','target_date')

    return render(request,'item_view_inspect.html',context={'ivi':ivi})
# end furqan

def create_inspection_details(request):
    if request.method == "POST" and request.is_ajax():
        from datetime import datetime
        final=request.POST.get('final_partinspected')
        final_id=request.POST.get('id_partinspected')
        rly=request.POST.get('zone')
        div=request.POST.get('division')
        dept=request.POST.get('department')
        loc=request.POST.get('location')
        insdt=request.POST.get('txtDate2')
        inspection_date = datetime.strptime(insdt, '%d-%m-%Y').strftime('%Y-%m-%d')
        title=request.POST.get('titleinsp')
        
        
        
        finalval = json.loads(final)
        final_allid = json.loads(final_id)

        from datetime import datetime 
        year = str(datetime.now().year)
        desig = m1.empmast.objects.get(myuser_id=request.user).desig_longdesc
        last_note = m1.Inspection_details.objects.all().last()
        if last_note.inspection_note_no == '' or last_note.inspection_note_no == None:
            note_no = year+'/'+desig+'/Insp'+'/1'
        else:
            note_no = year+'/'+desig+'/Insp'+'/'+ str(last_note.inspection_no)


        m1.Inspection_details.objects.create(inspection_title=title,inspection_note_no=note_no, status_flag=1, zone=rly,division=div,dept=dept,location=loc,inspected_on=inspection_date)
        inspection_id=m1.Inspection_details.objects.all().last().inspection_no
        for f, b in zip(finalval, final_allid):
            print(finalval[f], final_allid[b])
            for x,y in zip(finalval[f], final_allid[b]):
                s = y.split('.')
                if len(s) == 1:
                    hed = 'heading'+y
                    heading = finalval[f][hed]
                    m1.Item_details.objects.create(item_title=heading, type='H',des_id=y, inspection_no_id=inspection_id)
                elif len(s) == 2:
                    ob = 'observation'+y
                    trz = 'targetdate'+y
                    officm = 'markeofficer'+y

                    observation = finalval[f][ob]
                    targetd = finalval[f][trz]
                    markof = finalval[f][officm]
                    markeofficer = markof.split(',')
                    

                    targetdate = datetime.strptime(targetd, '%d-%m-%Y').strftime('%Y-%m-%d')
                    print(observation)
                    m1.Item_details.objects.create(observation=observation,inspection_no_id=inspection_id, des_id=y, target_date=targetdate, type='SH')
                    
                    item_id=m1.Item_details.objects.all().last().item_no
                    #mark officer
                    if markof:
                        for i in markeofficer:
                            myuser_id=m1.empmast.objects.filter(empno=i)[0].myuser_id_id
                            desig_longdesc=m1.empmast.objects.filter(empno=i)[0].desig_longdesc
                            print('uuuuuuuuuuuuuuuuuu', desig_longdesc)
                            Desig=m1.Designation_Master.objects.filter(master_name=desig_longdesc)[0].designation_master_no
                            marked_no_id=(m1.Marked_Officers.objects.all().last().marked_no)+1
                            m1.Marked_Officers.objects.create(marked_no=marked_no_id,myuser_id_id=myuser_id,item_no_id=item_id,marked_to_id=int(Desig))
                    else:
                        markeofficer=""
                else:
                    subdes = 'subdes'+y
                    subdes1 = finalval[f][subdes]
                    m1.Item_details.objects.create(item_subtitle=subdes1, type='SSH',des_id=y, inspection_no_id=inspection_id)


        #=============
        # for i in range(len(list1)):
            
        #     item_id=m1.Item_details.objects.all().last().item_no
        #     for j in range(len(list7[i])):
        #         print(list7[i],'__')
        #         myuser_id=m1.empmast.objects.filter(empno=list7[i][j])[0].myuser_id_id
        #         desig_longdesc=m1.empmast.objects.filter(empno=list7[i][j])[0].desig_longdesc
        #         Desig=m1.Designation_Master.objects.filter(master_name=desig_longdesc)[0].designation_master_no
        #         marked_no_id=(m1.Marked_Officers.objects.all().last().marked_no)+1
        #         m1.Marked_Officers.objects.create(marked_no=marked_no_id,myuser_id_id=myuser_id,item_no_id=item_id,marked_to_id=int(Desig))
        # print("@@@@@@@@@@@@@@@@@@@",rly,dept,div,loc,inspection_date)
           
        return JsonResponse({"status": 1 })
    return JsonResponse({"success":False}, status=400)
    # except Exception as e:
    #     print("e==",e)  
    #     return render(request, "commonerrorpage.html", {})



# def create_inspection_details(request):
#     try:
       
#         if request.method=="GET" and request.is_ajax():
#             rly=request.GET.get('zone')
#             div=request.GET.get('division')
#             dept=request.GET.get('department')
#             loc=request.GET.get('location')
#             target_date=request.GET.get('target_date')
#             title=request.GET.get('title')
#             inspection_date=request.GET.get('inspection_date')
#             final_partinspected1=request.GET.get('final_partinspected1')
          
#             final_partinspected3=request.GET.get('final_partinspected3')
#             list1=final_partinspected1.split(',')
        
#             list3=final_partinspected3.split(',')
#             print(list1,list3)
#             # email=request.user.email()
#             print("@@@@@@@@@@@@@@@@@@@",rly,dept,div,loc,inspection_date,target_date)
           
          
#             obj=m1.Inspection_details.objects.create(inspection_title=title,zone=rly,division=div,dept=dept,location=loc,
#                 inspected_on=inspection_date,target_date=target_date)
#             for i in range(len(list1)):
#                 print("&&&&&&&&&&&")
#                 models.Item_details.objects.create(status_flag=0,observation=list3[i][1:-1])
            
#             return JsonResponse({
#                     "status": 1})
#     except Exception as e:
#         print("e==",e)  
#         return render(request, "commonerrorpage.html", {})


def MailSend(subject,email_body1,To):
    try:
        # subject = "Verify Your Mail"
        email = 'mfgcris@cris.org.in'

        html_content= MIMEText(email_body1+'<br><div class="container"><img src="cid:myimage"/></div><div style="text-align:center"><a href="#"> Unsubscribe</a></div>', _subtype='html')
        text_content = strip_tags(html_content) # Strip the html tag. So people can see the pure text at least.

        text_file = open("mail.txt", "a") # opening my file
        time=datetime.now()
        date_time=time.strftime("%m/%d/%Y,%H:%M:%S")

        text_file.write("\n\n"+date_time+"\n"+email+'\n'+To+"\n"+subject+"\n"+text_content) 
        text_file.write(text_content) 
        text_file.close() #file close

        img_data = open('rkvy/static/rkvy/images/logo_rkvy.png', 'rb').read()

        html_part = MIMEMultipart(_subtype='related')

        # Create the body with HTML. Note that the image, since it is inline, is 
        # referenced with the URL cid:myimage... you should take care to make
        # "myimage" unique
        html_part.attach(html_content)

        # Now create the MIME container for the image
        img = MIMEImage(img_data, 'png')
        img.add_header('Content-Id', '<myimage>')  # angle brackets are important
        img.add_header("Content-Disposition", "inline", filename="myimage") # David Hess recommended this edit
        html_part.attach(img)

        # Configure and send an EmailMessage
        # Note we are passing None for the body (the 2nd parameter). You could pass plain text
        # to create an alternative part for this message
        msg = EmailMessage(subject, None, email, [To])
        msg.attach(html_part) # Attach the raw MIMEBase descendant. This is a public method on EmailMessage
        msg.send()
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="MailSend",err_details=str(e))
        except:
            print("Internal Error!!!")


# def loginUser(request):
#     # try:
#         if request.method == "POST":
#             _email = request.POST.get('email').strip()
#             _password = request.POST.get('password').strip()
#             print(_email,'____')
#             print(_password,'_____')
#             # obj3=models.rkvy_userEnrollment.objects.filter(user_id__email=_email).values('pending_stage')
#             # check for existence
#             userObj = authenticate(username=_email, password=_password)
#             print(userObj.username)

#             print("22222222222222222222222227777777777777777777777777777777777777777777777^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^",userObj)
#             if userObj is not None:
#                 login(request, userObj)
#                 print("inside login&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
#                 if userObj.user_role == 'rkvy_superadmin':
#                     return HttpResponseRedirect('/rkvy_superAdminHome')
#                 elif userObj.user_role == 'rkvy_headquarteradmin':
#                     return HttpResponseRedirect('/rkvy_headquarterAdminHome')
#                 elif userObj.user_role == 'rkvy_instituteadmin':
                    
#                     return HttpResponseRedirect('/rkvy_instituteAdminHome')
#                 elif userObj.user_role == 'rkvy_instructor':
#                     return HttpResponseRedirect('/rkvy_instructorHome')
#                 elif userObj.username=='admin':
#                     return HttpResponseRedirect('/adminuserHome')
#                 else:
#                     # return HttpResponseRedirect('/userHome')
#                     print("11111111111111111111111")
#                     return render(request, "base.html")
#                     # return render(request,"list_create_inspection_report.html")
                    
#             else:
#                 #change 21-10
#                 if user.objects.filter(email=_email,user_role='rkvy_trainee',is_active=False).exists():
#                     messages.error(request, 'Email is not verified yet. Please verify first then login again.')
#                 else:
#                     messages.error(request, 'Invalid Credentials.')#till here 21-10
#                 #return HttpResponseRedirect('/rkvy_login')

#                 return render(request, "login.html")
#         print('hhhh')
#         return render(request, "login2.html")
    # except Exception as e: 
    #     try:
    #         models.error_Table.objects.create(fun_name="login",user_id=request.user,err_details=str(e))
    #     except:
            
    #         print("Internal Error->>>>>>>>>4!!!")
    #     #messages.error(request, 'Error : '+str(e))
    #     return render(request, "login.html", {})
def userHome(request):
    return render(request,"userHome.html")

def zonaluserHome(request):
    return render(request,"zonaluserHome.html")


def divisonuserHome(request):
    return render(request,"divisonHome.html")

def requests(request):
    lst=m1.user_request.objects.filter(rly_id=request.user.username,status='Pending').values('id','empno','myuser_id__first_name','requestDate','status')
    if request.method== 'POST':
        req_id=request.POST.get('req_id')
        print(req_id)
        action=request.POST.get('action_1')
        if action=='Accept':
            m1.user_request.objects.filter(id=req_id).update(status='Accepted')
            myuser_id_id=m1.user_request.objects.filter(id=req_id)[0].myuser_id_id
            user.objects.filter(id=myuser_id_id).update(is_active=True)
        else:
            models.user_request.objects.filter(id=req_id).update(status='Rejected')

    r=True
    context={'result':lst,'r':r}

    return render(request,"requestList.html",context)

def Divisonrequests(request):
    lst=m1.user_request.objects.filter(rly_id=request.user.username,status='Pending').values('id','empno','myuser_id__first_name','requestDate','status')
    print(lst)
    if request.method== 'POST':
        req_id=request.POST.get('req_id')
        print(req_id)
        action=request.POST.get('action_1')
        if action=='Accept':
            m1.user_request.objects.filter(id=req_id).update(status='Accepted')
            myuser_id_id=m1.user_request.objects.filter(id=req_id)[0].myuser_id_id
            user.objects.filter(id=myuser_id_id).update(is_active=True)
        else:
            m1.user_request.objects.filter(id=req_id).update(status='Rejected')

    r=True
    context={'result':lst,'r':r}

    return render(request,"requestList.html",context)


def forgotPassword(request):
    # try:
        if request.method == "POST":
            _email = request.POST.get('email').strip()

            try:
                userObj = user.objects.get(email=_email)
                #print(userObj)
            except Exception as e:
                messages.error(request, 'Please enter registed email.')
                return HttpResponseRedirect('/forgotPassword')

            email_context = {
                "email": userObj.email,
                'domain': 'railkvy.indianrailways.gov.in',
                'site_name': 'Kaushal Vikas',
                "uid": urlsafe_base64_encode(force_bytes(userObj.pk)),
                "user": userObj,
                'token': default_token_generator.make_token(userObj),
                'protocol': 'http',
            }
            email_template_name = "email_forgotPassword_body.txt"
            email_body = render_to_string(email_template_name, email_context)
            try:
                #print("trying to send mail")
                #print(userObj.email)
                try:
                    # send_mail("Verify Your Mail", email_body, 'crisdlwproject@gmail.com',
                    #          [f'{userObj.email}'], fail_silently=False)


                    #saud faisal (28-08-2021) -----
                    subject="Reset password for RKVY login"
                    To=userObj.email
                    email_body1='<p>'+email_body+'</p>'
                    MailSend(subject,email_body1,To)
                    #end here
                    return HttpResponse('Verification Email has been successfully sent.(see also spam folder)')
                except:
                    print("error on sending")
                    messages.error(
                        request, 'Verification Email failed. Please Try Again.')
            except:
                messages.error(
                    request, 'Something went wrong.')
            return render(request, "inspects_forgotPassword.html")

        return render(request, "inspects_forgotPassword.html")
    # except Exception as e: 
    #     try:
    #         models.error_Table.objects.create(fun_name="forgotPassword",user_id=request.user,err_details=str(e))
    #     except:
    #         print("Internal Error!!!")
    #     #messages.error(request, 'Error : '+str(e))
    #     return render(request, "commanerrorpage.html", {})


#bhartistart

def create_inspection_form(request):
    # try:
    if request.method=="POST" :
        rly=request.POST.get('zone')
        div=request.POST.get('division')
        dept=request.POST.get('department')
        loc=request.POST.get('location')
        inspection_date=request.POST.get('start')
        # print("@@@@@@@@@@@@@@@@@@@")
    
    
    empdata=m1.empmast.objects.filter(myuser_id=request.user).values('empname','empno', 'desig_longdesc')
    desig_longdesc = empdata[0]['desig_longdesc']
    # print('ttttttttttttttttttttttttttttttttttttttttttttttttttttttt', desig_longdesc)
    list1=models.railwayLocationMaster.objects.filter(location_type='ZR').values('location_code')
    list2=[]
    for i in list1:
        # print(i['location_code'],'_________')
        list2.append(i['location_code'])
    list3=models.railwayLocationMaster.objects.filter(location_type='DIV').values('location_code')
    list4=[]
    for i in list3:
        # print(i['location_code'],'_________')
        list4.append(i['location_code']) 
    try:
        
        list5=list(m1.Designation_Master.objects.all().values('master_name','designation_master_no','master_email'))  
    except Exception as e:
        print("e==",e)  
    list6=models.departMast.objects.all().values('department_name')
    
    context={
        'Zone':list2 ,
        'division':list4,
        'marked_to':list5,
        'department':list6,
        'desig': desig_longdesc
        
        }
    # print(list2,'_____________')
    ins_id=request.GET.get('ins_id')
    # print(ins_id,'______________________________')
    ins_detail=[]
    item_id=[]
    length = 0
    if ins_id!=None:
        # print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        ins_detail=list(m1.Inspection_details.objects.filter(inspection_no=ins_id).values())
        item_details1= list(m1.Item_details.objects.filter(inspection_no_id=ins_id).values())
        for x in item_details1:
            item_id.append(x['des_id'])
            if x['type'] == 'H':
                length = m1.Item_details.objects.filter(inspection_no_id=ins_id, type="H").count()
                
                print('lengh_of h',length)
        for j in item_details1:
            
            if j['type'] == 'SH':
                mark=m1.Marked_Officers.objects.filter(item_no=j['item_no']).values()
                print('---------', j['item_no'])
                mrkoffi = {}
                desig_longdesc1 =''
                marked_officers1 = ''
                for x in mark:
                    print('xxxxxxxxx', x['myuser_id_id'])
                    
                    marked=m1.empmast.objects.filter(myuser_id=x['myuser_id_id'])
                    print('yyyyyyyy', marked[0].desig_longdesc)
                    desig_longdesc1 += marked[0].desig_longdesc+','
                    marked_officers1 += marked[0].empno+','
                print('kkkkkkkkkkkkkkk', desig_longdesc1)
                mrkoffi.update({'marked_officers': marked_officers1, 'desig_longdesc': desig_longdesc1})
                
                j.update({'mrkoffi': mrkoffi})
                # print('mmmmmmmm', desig_longdesc1)
            
        ins_detail[0].update({'item_details1': item_details1})
        # print('00000000', ins_detail)
        print('00000000', ins_detail)
        # for i in ins:
            # temp={}
            # temp['inspection_no']=i['inspection_no']
            # temp['zone']=i['zone']
            # temp['division']=i['division']
            # temp['location']=i['location']
            # temp['inspected_on']= i['inspected_on'].strftime("%d-%m-%Y")
            # temp['inspection_note_no']=i['inspection_note_no']
            # temp['dept']=i['dept']
            # temp['inspection_title']=i['inspection_title']
            # ins_detail.append(temp)
            # ins_detail.extend({:})
        
        # item_details=m1.Item_details.objects.filter(inspection_no_id=ins_id, type='SH').values()
        # # print(item_details)
        # item=[]
        # for i in  item_details:
        #     temp={}
        #     temp['item_no']=i['item_no']
        #     temp['observation']=i['observation']
        #     temp['target_date']=i['target_date'].strftime("%d-%m-%Y")
        #     mark=m1.Marked_Officers.objects.filter(item_no=i['item_no']).values()
        #     # print('mark', mark)
        #     marked_officers=''
        #     desig_longdesc =''
            
        #     for j in mark:
        #         marked=m1.empmast.objects.filter(myuser_id=j['myuser_id_id'])[0]
        #         marked_officers = marked.empno+','
        #         desig_longdesc = marked.desig_longdesc+','
        #     temp['marked_officers']=marked_officers

        #     temp['desig_longdesc']=desig_longdesc
        #     item.append(temp)
        print('rrrrrrrrrrrrrrr', item_id)
        context={
            # 'Zone':list2,
            # 'division':list4,
            # 'marked_to':list5,
            # 'department':list6,
            'ins_detail':ins_detail,
            'item_id': item_id,
            'length_of_h': length
            # 'item':item
            }  
        # print(ins_detail[0],'0000000000000000000000000000000000000000000000000')  
        # print(item)
        # print('zone', list2)
        return render(request,"edit_inspection_form.html",context)
    else:     
        return render(request,"create_inspection_form.html", context)

    # except Exception as e:
    #     print("e==",e)  

def autoFetchLocation(request):
    if request.method == 'GET' and request.is_ajax():
        list1=list(models.locationMaster.objects.values_list('city', flat=True).order_by('city').distinct('city'))
        # print(list1)
        return JsonResponse(list1, safe=False)
    return JsonResponse({'success': False})



def save_draft_data(request):
    if request.method == "POST" and request.is_ajax():
        from datetime import datetime
        final=request.POST.get('final_partinspected')
        final_id=request.POST.get('id_partinspected')
        rly=request.POST.get('zone')
        div=request.POST.get('division')
        dept=request.POST.get('department')
        loc=request.POST.get('location')
        insdt=request.POST.get('txtDate2')
        inspection_date = datetime.strptime(insdt, '%d-%m-%Y').strftime('%Y-%m-%d')
        title=request.POST.get('titleinsp')
        
        
        
        finalval = json.loads(final)
        final_allid = json.loads(final_id)

     
        m1.Inspection_details.objects.create(inspection_title=title, zone=rly,division=div,dept=dept,location=loc,inspected_on=inspection_date)
        inspection_id=m1.Inspection_details.objects.all().last().inspection_no
        for f, b in zip(finalval, final_allid):
            print(finalval[f], final_allid[b])
            for x,y in zip(finalval[f], final_allid[b]):
                s = y.split('.')
                if len(s) == 1:
                    hed = 'heading'+y
                    heading = finalval[f][hed]
                    m1.Item_details.objects.create(item_title=heading, type='H',des_id=y, inspection_no_id=inspection_id)
                elif len(s) == 2:
                    ob = 'observation'+y
                    trz = 'targetdate'+y
                    officm = 'markeofficer'+y

                    observation = finalval[f][ob]
                    targetd = finalval[f][trz]
                    markof = finalval[f][officm]
                    
                    markeofficer = markof.split(',')
                    targetdate = datetime.strptime(targetd, '%d-%m-%Y').strftime('%Y-%m-%d')
                    print(observation)
                    m1.Item_details.objects.create(observation=observation,inspection_no_id=inspection_id, des_id=y, target_date=targetdate, type='SH')
                    
                    item_id=m1.Item_details.objects.all().last().item_no
                    if markof:
                        #mark officer
                        for i in markeofficer:
                            myuser_id=m1.empmast.objects.filter(empno=i)[0].myuser_id_id
                            desig_longdesc=m1.empmast.objects.filter(empno=i)[0].desig_longdesc
                            print('eeeeeeeeeeeeeee', desig_longdesc)
                            Desig=m1.Designation_Master.objects.filter(master_name=desig_longdesc)[0].designation_master_no
                            marked_no_id=(m1.Marked_Officers.objects.all().last().marked_no)+1
                            m1.Marked_Officers.objects.create(marked_no=marked_no_id,myuser_id_id=myuser_id,item_no_id=item_id,marked_to_id=int(Desig))
                    else:
                        markeofficer=''
                
                else:
                    subdes = 'subdes'+y
                    subdes1 = finalval[f][subdes]
                    m1.Item_details.objects.create(item_subtitle=subdes1, type='SSH',des_id=y, inspection_no_id=inspection_id)

        return JsonResponse({"status": 1 })
    return JsonResponse({"success":False}, status=400)
    # except Exception as e:
    #     print("e==",e)  
    #     return render(request, "commonerrorpage.html", {})


def nominate_officer(request):
    try:
        print("$%^%*()&*^%")
        officers_list=list(m1.empmast.objects.all().values('empname','empno', 'desig_longdesc'))
        print(officers_list)
        context={
            'officers_list':officers_list
        }
            
        return JsonResponse(context, safe = False)
    except Exception as e:
        print("e==",e)  
        


#bhartiend

#niyati



def employeeList(request):
    current_user = request.user
    emp=models.empmast.objects.get(pk=current_user.username) 
    employees=models.empmast.objects.all().order_by('empname') 
    category = models.empmast.objects.filter(decode_paycategory__isnull=False).values('decode_paycategory').distinct()
    department=models.departMast.objects.filter(delete_flag=False).values('department_name').order_by('department_name').distinct()
    context={
        'emp':emp,
        'department':department,
        'employees':employees,
        'sub':0,
        'category':category,
       
        'user':usermaster,
        
     }
    return render(request, 'employeeList.html',context)


def viewEmployee_Det(request):
    
    if request.method == "GET" and request.is_ajax():
        empno = request.GET.get('empno') 
        emp = models.empmast.objects.filter(empno=empno)[0]
        print(empno,'empno')
        context={  
        'empno':emp.empno,
        'empname':emp.empname,
        'birthdate':emp.birthdate,
        'dateapp':emp.appointmentdate,
        'office_or':emp.office_orderno,
        'sex':emp.sex,
        'emp_inctype':emp.emp_inctype,
        'marital_status':emp.marital_status,
        'email':emp.email,
        'contactno':emp.contactno,
        'ticket_no':emp.ticket_no,
        'idcard_no':emp.idcard_no,
        'emp_inctype':emp.emp_inctype,
        'inc_category':emp.inc_category,
        'desig':emp.desig_longdesc,
        'status':emp.emp_status,
        'dept':emp.dept_desc,
        'category':emp.decode_paycategory,
        'payband':emp.payband,
        'scalecode':emp.scalecode,
        'paylevel':emp.pc7_level,
        'gradepay':emp.payrate,
        'date_of_joining':emp.date_of_joining,
        'date_of_promotion':emp.date_of_promotion,
        'station_dest':emp.station_des,
        'wau':emp.wau,
        'billunit':emp.billunit,
        'service':emp.service_status,
        'emptype':emp.emptype,
        'medicalcode':emp.medicalcode,
        'tradecode':emp.tradecode,
        'role':emp.role,
        'shop_section':emp.shop_section,

        
    
        }  
    
    
        return JsonResponse(context, safe = False)
    return JsonResponse({"success":False}, status=400)


def  get_emp_detNew(request):
    if request.method == "GET" and request.is_ajax():
        empno = request.GET.get('empno') 
        obj = models.empmast.objects.filter(empno=empno).all() 
        rno=len(obj)
        if rno==0:            
           context={            
            'rno':rno ,
           }  
        else:          
           context={  
            'rno':rno ,          
            'empno':obj[0].empno,
            'empname':obj[0].empname,
            'birthdate':obj[0].birthdate,
            'dateapp':obj[0].appointmentdate,
            'office_orderno':obj[0].office_orderno,
            'sex':obj[0].sex,
            
            'marital_status':obj[0].marital_status,
            'email':obj[0].email,
            'contactno':obj[0].contactno,
            
            'desig':obj[0].desig_longdesc,
            'status':obj[0].emp_status,
            'dept':obj[0].dept_desc,
            'category':obj[0].decode_paycategory,
            'payband':obj[0].payband,
            'scalecode':obj[0].scalecode,
            'paylevel':obj[0].pc7_level,
            'gradepay':obj[0].payrate,
            'joining_date':obj[0].date_of_joining,
            'date_of_promotion':obj[0].date_of_promotion,
            'station_dest':obj[0].station_des,
            'wau':obj[0].wau,
            'billunit':obj[0].billunit,
            'service':obj[0].service_status,
            'emptype':obj[0].emptype,
            'ticket_no':obj[0].ticket_no,
            'idcard_no':obj[0].idcard_no,
            'emp_inctype':obj[0].emp_inctype,
            'inc_category':obj[0].inc_category,
            
       
           }  
       
       
        return JsonResponse(context, safe = False)
    return JsonResponse({"success":False}, status=400)

import json
def assign_role(request):
    
    if request.method=='GET' or request.is_ajax():
        print('hiiiii')
        empno1 = request.GET.get('empno1')
        print(empno1,'-------')
        emprole = request.GET.get('emprole')
        print(emprole,'----ttttt---')
        department = request.GET.get('department')
        print(department,'----uuuuuutt---')
        designation = request.GET.get('designation')
        print(designation,'---5555555t---')
        parentdesig = request.GET.get('parentdesig')
        print(parentdesig,'===================--------=========')
      
        s_section = request.GET.get('s_section')
        print(s_section,'___________________________')
        s_section = json.loads(s_section)
        sop =''
        for o in s_section:
            sop=sop+o+", "

        print(sop,'---------', designation)
       
        
        parent=models.Level_Desig.objects.filter(designation=parentdesig).values('designation_code')
        print(parent)
        employeeUpdate=models.empmast.objects.filter(empno=empno1).first()
        var1=models.Level_Desig.objects.filter(designation=designation).first()
        print(employeeUpdate,'----number')
        var1.parent_desig_code=parent[0]['designation_code']
        var1.save()
        employeeUpdate.role=emprole
        print(employeeUpdate.role)
        empl=models.empmast.objects.filter(empno=empno1).first()
        print(empl)
        sno=models.empmastnew.objects.all().last().sno
        
        models.empmastnew.objects.create(sno=sno+1,emp_id=empl,shop_section=sop)
        employeeUpdate.parent=emprole 
        employeeUpdate.dept_desc=department
       
        employeeUpdate.desig_longdesc=designation
        
        employeeUpdate.save()
       
        messages.success(request, 'Successfully Activate!')
        
        
    return JsonResponse({'saved':'save'})


def getDesigbyDepartment(request):
    if request.method == "GET" and request.is_ajax():
        department = request.GET.get('department')
        print(department)  
         
        obj=list(models.Level_Desig.objects.filter(department=department).values('designation').order_by('designation').distinct('designation'))
        print(obj,'____________________________________')
        return JsonResponse(obj, safe = False)
    return JsonResponse({"success":False}, status=400)


# def officer_bydiv(request):
#     if request.method == "GET" and request.is_ajax():
#         div_1 = request.GET.get('div_1')
         
#         div_id=railwayLocationMaster.objects.filter(location_code=div_1)[0].rly_unit_code
#         obj=list(models.empmast.objects.filter(division_id=div_id).values('empname').order_by('empname'))
#         context={
#             'obj':obj,
#         }
#         return JsonResponse(context, safe = False)
#     return JsonResponse({"success":False}, status=400)


 

def getsection_byshop1(request):
    if request.method == "GET" and request.is_ajax():
        shop = request.GET.get('shop')
        print(shop)  
         
        shop_id=models.shop_section.objects.filter(shop_code=shop).values('section_code')
        
       
        l=[]
        for i in shop_id:
            l.append(i['section_code'])
        print(l)    
        context={
            'shop_id':l,
        } 
        return JsonResponse(context, safe = False)
    return JsonResponse({"success":False}, status=400)
 


def getrole_bydesig(request):
    if request.method == "GET" and request.is_ajax():
        designation = request.GET.get('designation')
        print(designation)  
         
        desig_id=models.Level_Desig.objects.filter(designation=designation)[0].designation_code
        print(desig_id)
        role=list(models.roles.objects.filter(designation_code=desig_id).values('role').distinct('role'))
        print(role)
        l=[]
        for i in role:
            l.append(i['role'])
        print(l)    
        context={
            'role':l,
        } 
        return JsonResponse(context, safe = False)
    return JsonResponse({"success":False}, status=400)



def get_parentdesig(request):
    if request.method == "GET" and request.is_ajax():
        department = request.GET.get('department')
        print(department)  
        paylevel1 = request.GET.get('paylevel1')
        print(paylevel1)  
        
        desig_id=models.Level_Desig.objects.filter(department=department,pc7_level__gte=paylevel1).values('designation')
        print(desig_id,'------')
        #parent=models.Level_Desig.objects.filter(designation=desig_id).values('designation')
        l=[]
        for i in desig_id:
            l.append(i['designation'])
        print(l)    
        context={
            'desig_id':l,
        } 
        return JsonResponse(context,safe = False)
    return JsonResponse({"success":False}, status=400)


def getshopcode_bydept(request):
    if request.method == "GET" and request.is_ajax():
        department = request.GET.get('department')
        print(department)  
         
        dept_id=models.departMast.objects.filter(department_name=department)[0].department_code
        print(dept_id)
        shop_code=list(models.shop_section.objects.filter(department_code_id=dept_id).values('shop_code').distinct('shop_code'))
        
        l=[]
        for i in shop_code:
            l.append(i['shop_code'])
        print(l)    
        context={
            'shop_code':l,
        } 
        return JsonResponse(context, safe = False)
    return JsonResponse({"success":False}, status=400)


def empregistNew(request): 
    current_user = request.user
    # emp=empmast.objects.get(pk=current_user.username)  
    emp=models.empmast.objects.all()
    empst=models.empmast.objects.all().distinct('emp_status','dept_desc').distinct('emp_status') 
    depart=models.empmast.objects.all().values('dept_desc').distinct('dept_desc').order_by('dept_desc')
    railway=models.railwayLocationMaster.objects.all().values('location_code').distinct('location_code').order_by('location_code') 
    # shop=shop_section.objects.all().order_by('section_code') 
    employees=models.empmast.objects.all().order_by('empname')
    # shoplist=list(shop_section.objects.filter().values('shop_code','shop_id').order_by('shop_code').distinct()) 
    category = models.empmast.objects.filter(decode_paycategory__isnull=False).values('decode_paycategory').distinct()
    context={
        'emp':emp,
        'employees':employees,
        'sub':0,
        'category':category,
        'lenm' :2,
        # 'shoplist':shoplist,
        'nav':nav,
        
        'railway':railway,         
        'empst':empst,
        'subnav':subnav,
        'user':usermaster,
        'depart':depart,
    }
    if request.method=="POST":
        Submit=request.POST.get('Submit')
        empno=request.POST.get('empno')
        empname=request.POST.get('empname')
        id_card=request.POST.get('id_card')
        ticket=request.POST.get('ticket')
        emp_inctype=request.POST.get('emp_inctype')
        inc_category=request.POST.get('inc_category')
        sex=request.POST.get('empsex')
        marital_status=request.POST.get('empmarital')            
        email=request.POST.get('empemail')            
        contactno=request.POST.get('empphone')
        shopno=request.POST.get('shop_sec')  
        sub_shop_sec=request.POST.get('sub_shop_sec')
        emp_inctype=request.POST.get('emptype') 
        empdesignation=request.POST.get('empdesignation') 
        emptdepartment=request.POST.get('emptdepartment') 
        empstatus=request.POST.get('empstatus') 
        office_orderno=request.POST.get('office_orderno') 
        birthdate=request.POST.get('dobdate')
        dateapp=request.POST.get('dateapp')
        gradepay=request.POST.get('gradepay') 
        paylevel=request.POST.get('paylevel')
        payband=request.POST.get('payband') 
        scalecode=request.POST.get('scalecode')
        category=request.POST.get('category')
        medicalcode=request.POST.get('medicalcode') 
        tradecode=request.POST.get('tradecode')
        joining_date=request.POST.get('joining_date')
        date_of_promotion=request.POST.get('date_of_promotion')
        station_dest=request.POST.get('station_dest') 
        wau=request.POST.get('wau')
        billunit=request.POST.get('billunit') 
        service=request.POST.get('service')
        emptype=request.POST.get('emptype')
        try:
            if(dateapp != None):
                dateapp=datetime.datetime.strptime(dateapp, "%d-%m-%Y")
            
            if(birthdate != None):
                birthdate=datetime.datetime.strptime(birthdate, "%d-%m-%Y")

            if(joining_date != None):
                joining_date=datetime.datetime.strptime(joining_date, "%d-%m-%Y")
            
            if(date_of_promotion != None):
                date_of_promotion=datetime.datetime.strptime(date_of_promotion, "%d-%m-%Y")
        except:
            messages.success(request,'Please enter valid date !')
        print('Submit',Submit)
        import datetime
        cuser=request.user
        now = datetime.datetime.now()
        

        p=str(now).split(' ')
        
        s=p[0].split('-')
        day2 = s[0]
        month2 = s[1]
        year2 = s[2]
        
        date1 = year2+""+month2+""+day2
        
        time=str(p[1]).replace(':','')
        
        if(cuser != None):
            uniquid= str(cuser)+""+date1+""+time[:6]
        password="dlw@123"
        if Submit=='Submit':
            if User.objects.filter(username=empno).exists():
                messages.info(request, "User Already exists!")
            else:
               
    
                models.empmast.objects.create(decode_paycategory=category, empno=empno, empname=empname, birthdate=birthdate,appointmentdate=dateapp,sex=sex,marital_status=marital_status,email=email,contactno=contactno,parentshop=shopno,shopno=sub_shop_sec,emp_inctype=emp_inctype,inc_category=inc_category,desig_longdesc=empdesignation,emp_status=empstatus,dept_desc=emptdepartment,office_orderno=office_orderno, date_of_joining=joining_date, date_of_promotion=date_of_promotion, pc7_level=paylevel, payrate=gradepay,payband=payband, scalecode=scalecode,wau=wau, station_des=station_dest,billunit=billunit, service_status=service, emptype=emptype,idcard_no=id_card,ticket_no=ticket, profile_modified_by=emp.empno ,profile_modified_on=now,medicalcode=medicalcode,tradecode=tradecode)
                newuser = models.User.objects.create_user(username=empno, password=password,email=email, first_name=empname)
                newuser.is_staff= True
                newuser.is_superuser=True
                newuser.save()
            
            messages.success(request,'Record has successfully inserted !')
        else:
            models.empmast.objects.filter(empno=empno).update(decode_paycategory=category, emp_status=empstatus, sex=sex,marital_status=marital_status,email=email,contactno=contactno,emp_inctype=emp_inctype,inc_category=inc_category,  date_of_joining=joining_date, date_of_promotion=date_of_promotion,  empname=empname, birthdate=birthdate,appointmentdate=dateapp, desig_longdesc=empdesignation,dept_desc=emptdepartment,office_orderno=office_orderno, pc7_level=paylevel, payrate=gradepay,payband=payband, scalecode=scalecode,wau=wau,  station_des=station_dest,billunit=billunit, service_status=service, emptype=emptype,idcard_no=id_card,ticket_no=ticket, profile_modified_by=emp.empno, profile_modified_on=now,medicalcode=medicalcode,tradecode=tradecode)
            messages.error(request,'Record has successfully updated ')

         
    return render(request, 'empRegistrationnew.html',context)


def open_empregistNew(request, empno):
    emplist=models.empmast.objects.get(empno=empno)
    context={
        'emplist':emplist,
        'empno':empno,
    }
    return render(request, 'empRegistrationNew.html',context)


def add_designation(request):
    unit=models.departMast.objects.filter(delete_flag=False).values('department_name').order_by('department_name').distinct('department_name')
    submitvalue = request.POST.get('submit')
    current_user = request.user
    emp=models.empmast.objects.filter(pk=current_user.username).values('wau')
    print(emp,'_____________________________________________________')
    print(emp[0]['wau'],'__________________________________________')
    post=Post_master.objects.values()
    context={
        'unit':unit,
        'post':post,
        'wau':emp[0]['wau'],
    }
    
    return render(request,'add_designation.html', context)



def getsection_byshop(request):
     if request.method == "GET" and request.is_ajax():
        shop = request.GET.get('shop')
        print(shop)  
         
        shop=list(models.shop_section.objects.filter(shop_code=shop).values('section_code').distinct('section_code'))
        print(shop)
    
        l=[]
        for i in shop:
            l.append(i['section_code'])
        print(l)    
        context={
            'shop':l,
        } 
        return JsonResponse(context, safe = False)
     return JsonResponse({"success":False}, status=400)

    

def getshop_bydept(request):
    if request.method == "GET" and request.is_ajax():
        dept = request.GET.get('dept')
        print(dept)  
         
        dept_id=models.departMast.objects.filter(department_name=dept)[0].department_code
        print(dept_id)
        shop=list(models.shop_section.objects.filter(department_code_id=dept_id).values('shop_code').distinct('shop_code'))
        print(shop)
        l=[]
        for i in shop:
            l.append(i['shop_code'])
        print(l)    
        context={
            'shop':l,
        } 
        return JsonResponse(context, safe = False)
    return JsonResponse({"success":False}, status=400)


def post_bydept(request):
    if request.method == "GET" and request.is_ajax():
        dept1 = request.GET.get('dept1')
        print(dept1)
        dept_id=models.departMast.objects.filter(department_name=dept1)[0].department_code
        print(dept_id)
        post=list(models.Post_master.objects.filter(department_code_id=dept_id).values('post_desc').distinct('post_desc'))
        print(post)
        context={
            'post':post,
        }
       
        
       
        return JsonResponse(context, safe = False)
    return JsonResponse({"success":False}, status=400)


def getpost_bydept(request):
    if request.method == "GET" and request.is_ajax():
        dept = request.GET.get('dept')
        print(dept)  
         
        dept_id=models.departMast.objects.filter(department_name=dept)[0].department_code
        print(dept_id)
        post=list(models.Post_master.objects.filter(department_code_id=dept_id).values('post_desc').distinct('post_desc'))
        print(post)
        l=[]
        for i in post:
            l.append(i['post_desc'])
        print(l)    
        context={
            'post':l,
        } 
        return JsonResponse(context, safe = False)
    return JsonResponse({"success":False}, status=400)


def add_post(request):
    if request.method == 'POST' or request.is_ajax():
        current_user = request.user
        emp=models.empmast.objects.get(pk=current_user.username)  
        
        dept1 = request.POST.get('dept1')
        post_name = request.POST.get('post_name')
        print(dept1)
        print(post_name)
        dept_id=models.departMast.objects.filter(department_name=dept1)[0].department_code
        print(dept_id)

      
        models.Post_master.objects.create(department_code_id=dept_id,post_desc=post_name,modified_by=emp.empno)
        messages.success(request,'Data saved successfully')
        
            
    return JsonResponse({'saved':'save'})


def save_designation(request):
    if request.method == 'POST' or request.is_ajax():
        current_user = request.user
        emp=models.empmast.objects.get(pk=current_user.username) 
        wau = request.POST.get('wau')
        print(wau)
        dept = request.POST.get('dept')
        print(dept,'--------')

        design = request.POST.get('design')
        print(design,'___------')

        level = request.POST.get('level')
        level_=int(level)
        
        c = ('%02d' % level_)
        level1=c
        
        print(level1,'uuuuvar1-----')


        dept_id=models.departMast.objects.filter(department_name=dept)[0].department_code
        print(dept_id,'-----------------------')

        section=request.POST.get('section')
        print(section,'---------------------------------------------')

        shop=request.POST.get('shop')
        print(shop,'_____hhhhh')
        deptpost=request.POST.get('deptpost')
        print(deptpost,'[[[[[[[[')


        post=int(models.Post_master.objects.filter(department_code_id=dept_id)[0].post_id)
        a = ('%02d' % post)
        level2=a
        
        print(level2,'-------level2-----')

        print(post,'___________________________')
        
        section_id=list(models.shop_section.objects.filter(department_code_id=dept_id,shop_code=shop,section_code=section).values('section_id'))
        print(section_id,'gggggggggggggttttttttttggggg')

        
       
        sec_id=str(section_id[0]['section_id'])+level1+level2
        print(sec_id)
        id=models.Level_Desig.objects.all().last().id
        print(id,'___________________________________')
        
        if models.Level_Desig.objects.filter(department=dept,designation=design).exists():
            messages.error(request, 'Designation already present in this department')
        else:

            models.Level_Desig.objects.create(id=id+1,department=dept,designation=design,pc7_level=level1,department_code_id=dept_id,designation_code=sec_id,rly_unit=wau)
            messages.success(request, 'Data Saved')
        
        

      
        
        
            
    return JsonResponse({'saved':'save'})



def shop_data(request):
    if request.method == 'POST' or request.is_ajax():
        
        dept = request.POST.get('dept')
        shop = request.POST.get('shop')
        print(dept)
        print(shop)
        dept_id=models.departMast.objects.filter(department_name=dept)[0].department_code
        print(dept_id)
        count=1
        shopcode=models.shop_section.objects.filter(department_code_id=dept_id).distinct('shop_code').count()+1
        print(shopcode,"+++++++++")
        c = ('%02d' % shopcode)
        shopcode1=c

        # for i in shopcode:
        #     c = ('%02d' % shopcode)
        #     shopcode1=c
        #     count+1
        #     print(shopcode1)
       
        print(shopcode1)
        
        shop_id=str(120)+str(dept_id)+str(shopcode1)
        print(shop_id)
        section_id=shop_id+'00'
        print(section_id)
        section_code=int(section_id[5:9])
        
        
        print(section_code,'--------------__________--------------------')
        models.shop_section.objects.create(department_code_id=dept_id,shop_code=shop,shop_id=shop_id,section_id=section_id,rly_unit_code=120,section_code=section_code)
        messages.success(request,'Data saved successfully')
        
            
    return JsonResponse({'saved':'save'})

def created_checklist(request):
    try:
        print('@@@@@@@@@@@@@')
        rly=request.POST.get('zone')
        div=request.POST.get('division')
        dept=request.POST.get('department')
        loc=request.POST.get('loc')
        start_date=request.POST.get('start')
        end_date=request.POST.get('txtDate2')
        get_designation=request.POST.get('get_designation')
        print(rly,div,dept,loc,start_date,end_date,get_designation,"~~~~~~~~~")
        
        list3=models.railwayLocationMaster.objects.filter(location_type='DIV').values('location_code')
        # else:    
        #     list3=models.railwayLocationMaster.objects.filter(location_type='DIV',parent_location_code=rly).values('location_code')
        list4=[]
        for i in list3:
            list4.append(i['location_code'])    
        # print(list4,'_________llllllllll_____')
        list1=models.railwayLocationMaster.objects.filter(location_type='ZR').values('location_code')
        list2=[]
        for i in list1:
            # print(i['location_code'],'_________')
            list2.append(i['location_code'])
            
        list5=list(models.departMast.objects.all().values('department_name')) 
        item=[] 
        # print(list5)
        try: 
            
            if rly is None:
                print("########")
                
                mydata=list(m1.Inspection_details.objects.all().values('inspection_no','inspection_title','zone','inspected_on','division','dept','location','report_path').order_by('inspection_no'))
                print(mydata)
                # for i in range(len(mydata)):
                #    item.append(mydata[i]['inspection_no'])
                #    print(item)
            else:
                print("-------")
                mydata=m1.Inspection_details.objects.filter(zone=rly,division=div,dept=dept).values('inspection_no','inspection_title','inspected_on', 'zone','division','dept','location','report_path').order_by('inspection_no')
               

        except Exception as e:
            print("e==",e)  
       
        context={
           'Zone':list2 ,
           'division':list4,
           'department':list5,
           'mydata':mydata,
           'item':item,
        }
       
        
        
        return render(request,"list_create_inspection_report.html",context)
    except Exception as e:
        print("e==",e)  
        
        


def section_data(request):
    if request.method == 'POST' or request.is_ajax():
        
        dept1 = request.POST.get('dept1')
        print(dept1)
        sectiondept = request.POST.get('sectiondept')
        print(sectiondept)
        sec = request.POST.get('sec')
        print(sec)
        dept_id=models.departMast.objects.filter(department_name=dept1)[0].department_code
        print(dept_id)
        shopcode=models.shop_section.objects.filter(department_code_id=dept_id,shop_code=sectiondept).last().section_id
        shopcode_id=models.shop_section.objects.filter(department_code_id=dept_id,shop_code=sectiondept).last().shop_id
        section_code=models.shop_section.objects.filter(department_code_id=dept_id,shop_code=sectiondept).last().section_code
        print(shopcode)
        #shop_id=str(int(shopcode[0:-2]))+str(int(shopcode[-2:-1])+1)
        #print(shop_id,'____________________________________________________shop_id___________')
        shop_id=int(shopcode)+1
        sec_code=int(section_code)+1
        if models.shop_section.objects.filter(department_code_id=dept_id,shop_code=sectiondept).exists():

            models.shop_section.objects.filter(department_code_id=dept_id,shop_code=sectiondept).create(section_id=shop_id,section_desc=sec,shop_code=sectiondept,department_code_id=dept_id,shop_id=shopcode_id,section_code=sec_code)
            messages.success(request,'Data saved successfully')
        
            
    return JsonResponse({'saved':'save'})


def dept_data(request):
    if request.method == 'POST' or request.is_ajax():
        current_user = request.user
        emp=models.empmast.objects.get(pk=current_user.username).values('wau')
        emp['wau']
        department = request.POST.get('department')
        now = datetime.datetime.now()
        

        p=str(now).split(' ')
        
        s=p[0].split('-')
        day2 = s[0]
        month2 = s[1]
        year2 = s[2]
        
        date1 = year2+""+month2+""+day2
        
        time=str(p[1]).replace(':','')
        obj=list(models.departMast.objects.filter(department_name=department).values('department_name').distinct())
        sc_1=int(models.departMast.objects.last().department_code)
        print(sc_1)
           
        print(obj,'obj')
        if len(obj)==0:
            print('a')
            models.departMast.objects.create(department_name=department, department_code=sc_1+1,modified_by=emp.empno,rly_unit_code_id=emp['wau'])
            messages.success(request,'Data saved successfully')
        else:
            messages.error(request,'Department Already Exists!')
            print('b')
            # railwayLocationMaster.objects.filter(location_code=location_code).update(location_type=location_type, location_description=desc, parent_location_code=ploco_code, location_type_desc=type_desc, rstype=rstype, station_code=st_code)
           
    return JsonResponse({'saved':'save'})

def shop_section(request):
    current_user = request.user
    emp=models.empmast.objects.get(pk=current_user.username) 
    unit=models.departMast.objects.filter(delete_flag=False).values('department_name').order_by('department_name').distinct('department_name')
    list=[]
    cur= connection.cursor()
    cur.execute('''select department_name,shop_code,shop_id,section_code,section_id from dlw_shop_section a join dlw_departMast b on
    a.department_code_id=b.department_code order by (b.department_name,a.shop_code,a.section_code) ''')
    d=cur.fetchall()
    print(d,'________________')
    for i in d:
        temp={}
        temp['department_name']=i[0]
        temp['shop_code']=i[1]
        temp['shop_id']=i[2]
        temp['section_code']=i[3]
        temp['section_id']=i[4]
        list.append(temp)
    print('list',list,'_____________________________')    
    # val = models.shop_section.objects.filter(department_code_id__isnull=False).values('shop_code','shop_id','section_code','section_id','department_code_id').distinct() 
    # for i in val:
    #     temp={}
    #     temp['shop_code']=i['shop_code']
    #     temp['shop_id']=i['shop_id']
    #     temp['section_code']=i['section_code']
    #     temp['section_id']=i['section_id']
    #     if models.departMast.objects.filter(department_code=i['department_code_id']).exists():
    #         temp['department_name']=models.departMast.objects.filter(department_code=i['department_code_id'])[0].department_name 
    #     else:
    #         temp['department_name']='None'     
    #     list.append(temp)

    # mylist = []
    # for i in unit:
    #     temp={}
    #     #y = models.department_master.objects.filter(department_name=i['department_name'],delete_flag=False).order_by('shop_code').values('shop_code')
    #     print(y,'--------')
    #     temp['department_name']=i['department_name']
    #     str=""
    #     for j in y:
    #         print(j,'-----------')
    #         if(j['shop_code']!=None):
    #             str+=j['shop_code'] + "\r\n"
    #     temp['shop_code']=str
    #     mylist.append(temp)
    # print(mylist,'_________')
           
   
    context={
        'emp':emp,
        'list':list,
        # 'val':val,
        'unit':unit,
       
    }
    
    return render(request, 'shop_section.html',context)


def shop_bydept(request):
    if request.method == "GET" and request.is_ajax():
        dept = request.GET.get('dept')
        print("===================",dept)
        dept_id=models.departMast.objects.filter(department_name=dept)[0].department_code
        print("========id===========",dept_id)
        shop_code=list(models.shop_section.objects.filter(department_code_id=dept_id).values('shop_code').distinct('shop_code'))
        print(shop_code)
        context={
            'shop_code':shop_code,
        }
       
        
       
        return JsonResponse(context, safe = False)
    return JsonResponse({"success":False}, status=400)

def section_bydept(request):
    if request.method == "GET" and request.is_ajax():
        dept = request.GET.get('dept')
        sectiondept = request.GET.get('sectiondept')
        print(sectiondept)
        dept_id=models.departMast.objects.filter(department_name=dept)[0].department_code
        print(dept_id)
        section_desc=list(models.shop_section.objects.filter(department_code_id=dept_id,shop_code=sectiondept).values('section_desc').distinct('section_desc'))
        print(section_desc)
        context={
            'section_desc':section_desc,
        }
       
        
       
        return JsonResponse(context, safe = False)
    return JsonResponse({"success":False}, status=400)


def RoleAdd(request):
    cuser=request.user
    usermaster=models.empmast.objects.filter(empno=cuser).first()
    current_user = request.user
    emp=models.empmast.objects.filter(pk=current_user.username).values('wau')
    rolelist=usermaster.role.split(", ")  
    list=[]
    
    val = models.roles.objects.all().filter(delete_flag=False).values('role','parent','department_code_id').order_by('role').distinct() 
    for i in val:
        temp={}
        temp['role']=i['role']
        temp['parent']=i['parent']
        if models.departMast.objects.filter(department_code=i['department_code_id']).exists():
            temp['department_name']=models.departMast.objects.filter(department_code=i['department_code_id'])[0].department_name 
        else:
            temp['department_name']='None'     
        list.append(temp)
    role = models.roles.objects.all().filter(delete_flag=False).values('role').order_by('role').distinct()
    empdep = models.departMast.objects.all().values('department_name').order_by('department_name').distinct()
    shop = models.shop_section.objects.values('shop_code').order_by('shop_code').distinct()
    users = []
    if request.method=="POST":
        rolename = request.POST.get('roldel')
        print(rolename)
        if rolename:
          
            models.custom_menu.objects.all().filter(role=rolename).delete()
            models.roles.objects.all().filter(role=rolename).update(delete_flag=True)
            userremove = models.empmast.objects.all().values('empno').filter(role=rolename)
            for i in range(len(userremove)):
                # users.append(userremove[i]['empno'])
                models.empmast.objects.filter(empno=userremove[i]['empno']).update(role=None,parent=None)
            # User.objects.filter(username__in=users).delete()
            messages.success(request, 'Successfully Deleted!')
        else:
            messages.error(request,"Error")
    context = {
       
        'nav':nav,
        'subnav':subnav,
        'roles' : role,
        'val':val,
        'empdep':empdep,
        'shop':shop,
        'list':list,
        'wau':emp[0]['wau'],
    }
    return render(request,'RoleAdd.html',context)


def ajaxDeleteRoleUser(request):
    if request.method == 'POST' or request.is_ajax():

        rolename= request.POST.get('roledel')
        if rolename:
            perlist = models.custom_menu.objects.filter(role=rolename).values('url').distinct()   
            models.custom_menu.objects.all().filter(role=rolename).delete()
            models.roles.objects.all().filter(role=rolename).update(delete_flag=True)
            userremove = models.empmast.objects.all().values('empno').filter(role=rolename)
            for i in range(len(userremove)):
               
                models.empmast.objects.filter(empno=userremove[i]['empno']).update(role=None,parent=None)
            
       
    return JsonResponse({'deleted':'delete'})


def ajaxRoleGen(request):
    
    if request.method=='POST' or request.is_ajax():
        current_user = request.user
        emp=models.empmast.objects.get(pk=current_user.username)  
        rolename = request.POST.get('rolename')
        department = request.POST.get('department')
        designation = request.POST.get('designation')
        shop = request.POST.get('shop1')
        shop1 = json.loads(shop)
        sop =''
        for o in shop1:
            sop=sop+o+", "

        print(sop,'---------', designation)
        role=models.roles.objects.filter(role=rolename)
        desig_id=models.Level_Desig.objects.filter( designation= designation)[0].designation_code
        print(desig_id)
        dept_id=models.departMast.objects.filter(department_name=department)[0].department_code
        print(dept_id)
        if len(role)==0:
            models.roles.objects.create(role=rolename,parent=rolename,department_code_id=dept_id,modified_by=emp.empno, rly_unit=emp.wau,shop_code=sop, designation_code=desig_id)            
            messages.success(request,"succesfully added!")
        else:
            messages.error(request,"This role already exists")
    return JsonResponse({'saved':'save'})


def getDepartmentbyroles(request):
    if request.method == "GET" and request.is_ajax():
        emptdepartment = request.GET.get('emptdepartment')
               
        if emptdepartment !=None: 
            obj=list(models.departMast.objects.filter(department=emptdepartment).values('designation').order_by('designation').distinct())
            
        return JsonResponse(obj, safe = False)
    return JsonResponse({"success":False}, status=400)


def getDesigbyDepartment(request):
    if request.method == "GET" and request.is_ajax():
        department = request.GET.get('department')
        print(department)  
         
        obj=list(models.Level_Desig.objects.filter(department=department).values('designation').order_by('designation').distinct('designation'))
        print(obj,'____________________________________')
        return JsonResponse(obj, safe = False)
    return JsonResponse({"success":False}, status=400)


def getshopcode_bydept(request):
    if request.method == "GET" and request.is_ajax():
        department = request.GET.get('department')
        print(department)  
         
        dept_id=models.departMast.objects.filter(department_name=department)[0].department_code
        print(dept_id)
        shop_code=list(models.shop_section.objects.filter(department_code_id=dept_id).values('shop_code').distinct('shop_code'))
        
        l=[]
        for i in shop_code:
            l.append(i['shop_code'])
        print(l)    
        context={
            'shop_code':l,
        } 
        return JsonResponse(context, safe = False)
    return JsonResponse({"success":False}, status=400)

def inspect_logout(request):
    try:
        logout(request)
        return HttpResponseRedirect('/login')
    except Exception as e: 
       print(e)

def inspect_changePassword(request):
    print('jjjjj')
    try:
        if request.method == "POST":
            try:
                oldpass = request.POST.get('oldPassword').strip()
                newpass = request.POST.get('confirmNewPassword').strip()
                loguser = request.user.pk

                if len(str(newpass).strip()) < 8 or oldpass == None or newpass == None:
                    # make an error manually to go into except block
                    raise ValueError('Password must be 8 chars')

                loguser = user.objects.get(pk=loguser)
                if loguser.check_password(oldpass):
                    loguser.set_password(newpass)
                    loguser.save()
                    print('jjjjj')
                    messages.success(request, "Password Changed successfully.")
                    print('done')
                else:
                    messages.error(request, "Invalid Credentials.")

            except Exception as e: 
                print(e,'aaaaaaaaaaaaaaa')
                messages.error(request, "Something went wrong.")
                return HttpResponseRedirect('/inspect_changePassword')
        return render(request, "inspect_changePassword.html")
    except Exception as e: 
        print(e)

#niyati 150622
  
def board_officers(request):
    if request.method == "GET" and request.is_ajax():
        rly_1=request.GET.get('rly_1')
        print(rly_1,'_________________________railways________________')
        
        
        hq=m1.railwayLocationMaster.objects.filter(location_code=rly_1,parent_location_code='RB')[0].rly_unit_code
        print(hq)
        allboard=list(m1.empmast.objects.filter(rly_id_id=hq).values('empname','empno').order_by('empname'))
        print(allboard)
        context={
           'allboard':allboard,
        } 
        return JsonResponse(context,safe = False)
    return JsonResponse({"success":False}, status = 400)


def getdiv_rly(request):

    if request.method == "GET" or request.is_ajax():
        rly=request.GET.get('rly')
        print(rly,'_________++++++++++++++++++++++________________')
          
        division=list(m1.railwayLocationMaster.objects.filter(location_type='DIV',parent_location_code=rly).order_by('location_code').values('location_code').distinct('location_code'))
        l=[]
        for i in division:
            l.append(i['location_code'])
        print(l)    
        context={
            'division':l,
        } 
        return JsonResponse(context,safe = False)
    return JsonResponse({"success":False}, status = 400)



def division_wise(request):
    if request.method == "GET" and request.is_ajax():
        rly_1=request.GET.get('rly_1')
        print(rly_1,'_________________________railways________________')
        div_1=request.GET.get('div_1')
        print(div_1,'___________________div________________') 
        if rly_1=="All":
            if div_1=="All":
            # hq=railwayLocationMaster.objects.filter(location_code=rly_1,location_type='ZR')[0].rly_unit_code
            # print(hq)
            # hqwise=list(empmast.objects.filter(rly_unit_code_id=hq).values('empname').order_by('empname'))
            # print(hqwise)
                divwise=list(m1.empmast.objects.filter(rly_id_id__isnull=False,div_id_id__isnull=False).values('empname','empno').order_by('empname'))
                print(divwise)
            else:
                hq=m1.railwayLocationMaster.objects.filter(location_code=div_1,location_type='DIV')[0].rly_unit_code
                print(hq)
                divwise=list(m1.empmast.objects.filter(rly_id_id__isnull=False,div_id_id=hq).values('empname','empno').order_by('empname'))
                print(divwise)
        else:
            print('jjjjj')
            if div_1=="All":
                print('amishaaaaaaaaaaa')
                hq=m1.railwayLocationMaster.objects.filter(location_code=rly_1,location_type='ZR')[0].rly_unit_code
                print(hq)
                divwise=list(m1.empmast.objects.filter(rly_id_id=hq).values('empname','empno').order_by('empname'))
                print(divwise)
            else:
                print('niyatiiiiiiiiiiiiiii')
                hq=m1.railwayLocationMaster.objects.filter(parent_location_code=rly_1,location_code=div_1)[0].rly_unit_code
                print(hq)
                divwise=list(m1.empmast.objects.filter(div_id_id=hq).values('empname','empno').order_by('empname'))
                print(divwise)


        # hq=railwayLocationMaster.objects.filter(location_code=div_1)[0].rly_unit_code
        # print(hq)
        # divwise=list(empmast.objects.filter(division_id=hq).values('empname').order_by('empname'))
        # print(divwise)
        context={
           'divwise':divwise,
        } 
        return JsonResponse(context,safe = False)
    return JsonResponse({"success":False}, status = 400)



def gm_list_officers(request):
    if request.method == "GET" and request.is_ajax():
        rly_1=request.GET.get('rly_1')
        print(rly_1,'_________________________railways________________')
        div_1=request.GET.get('div_1')
        print(div_1,'___________________div________________') 
        # hq=railwayLocationMaster.objects.filter(parent_location_code=rly_1,location_code=div_1)[0].rly_unit_code
        # print(hq)
        allgm=list(m1.empmast.objects.filter(desig_longdesc='GM').values('empname','desig_longdesc','empno').order_by('empname'))
        print(allgm)
        context={
           'allgm':allgm,
        } 
        return JsonResponse(context,safe = False)
    return JsonResponse({"success":False}, status = 400)


def drm_officers(request):
    if request.method == "GET" and request.is_ajax():
        rly_1=request.GET.get('rly_1')
        print(rly_1,'_________________________railways________________')
        div_1=request.GET.get('div_1')
        print(div_1,'___________________div________________') 
       
        rail=m1.railwayLocationMaster.objects.filter(location_code=rly_1,location_type='ZR')[0].rly_unit_code
        print(rail)
        hq=m1.railwayLocationMaster.objects.filter(location_code=div_1,parent_location_code=rly_1)[0].rly_unit_code
        print(hq)
        if div_1=="All":

            alldrm=list(m1.empmast.objects.filter(rly_id_id=rail,desig_longdesc='DRM').values('empname','desig_longdesc').order_by('empname'))
            print(alldrm)
        else:
            alldrm=list(m1.empmast.objects.filter(div_id_id=hq,desig_longdesc='DRM').values('empname','desig_longdesc').order_by('empname'))
            print(alldrm)

        context={
           'alldrm':alldrm,
        } 
        return JsonResponse(context,safe = False)
    return JsonResponse({"success":False}, status = 400)


def phod_officers(request):
    if request.method == "GET" and request.is_ajax():
        rly_1=request.GET.get('rly_1')
        print(rly_1,'_________________________railways________________')
        dept_1=request.GET.get('dept_1')
        print(dept_1,'___________________dept________________') 
       
        rail=m1.railwayLocationMaster.objects.filter(location_code=rly_1,location_type='ZR')[0].rly_unit_code
        print(rail)
       
        if dept_1=="All":

            allphod=list(m1.empmast.objects.filter(rly_id_id=rail,desig_longdesc='PHOD').values('empname','desig_longdesc','empno').order_by('empname'))
            print(allphod)
        else:
            allphod=list(m1.empmast.objects.filter(rly_id_id=rail,desig_longdesc='PHOD',dept_desc=dept_1).values('empname','desig_longdesc','empno').order_by('empname'))
            print(allphod)

        context={
           'allphod':allphod,
        } 
        return JsonResponse(context,safe = False)
    return JsonResponse({"success":False}, status = 400)


def headqwise(request):
    if request.method == "GET" and request.is_ajax():
        rly_1=request.GET.get('rly_1')
        print(rly_1,'_________________________railways________________')
        dept_1=request.GET.get('dept_1')
        print(dept_1,'_________________________department________________')
       
        if rly_1=="All":
            if dept_1=="All":
            # hq=railwayLocationMaster.objects.filter(location_code=rly_1,location_type='ZR')[0].rly_unit_code
            # print(hq)
            # hqwise=list(empmast.objects.filter(rly_unit_code_id=hq).values('empname').order_by('empname'))
            # print(hqwise)
                hqwise=list(m1.empmast.objects.filter(rly_id_id__isnull=False).values('empname','empno', 'desig_longdesc').order_by('empname'))
                print(hqwise)
            else:
                hqwise=list(m1.empmast.objects.filter(dept_desc=dept_1).values('empname','empno', 'desig_longdesc').order_by('empname'))
                print(hqwise)

        else:
            if dept_1=="All":
                hq=m1.railwayLocationMaster.objects.filter(location_code=rly_1,location_type='ZR')[0].rly_unit_code
                print(hq)
                hqwise=list(m1.empmast.objects.filter(rly_id_id=hq).values('empname','empno', 'desig_longdesc').order_by('empname'))
                print(hqwise)
            else:
                hq=m1.railwayLocationMaster.objects.filter(location_code=rly_1,location_type='ZR')[0].rly_unit_code
                print(hq)
                hqwise=list(m1.empmast.objects.filter(rly_id_id=hq,dept_desc=dept_1).values('empname','empno', 'desig_longdesc').order_by('empname'))
                print(hqwise)

       
        # else:
        #     hq=railwayLocationMaster.objects.filter(location_code=rly_1,location_type='ZR')[0].rly_unit_code
        #     print(hq)
        #     hqwise=list(empmast.objects.filter(rly_unit_code_id=hq,dept_desc=dept_1).values('empname').order_by('empname'))
        #     print(hqwise)
        context={
           'hqwise':hqwise,
        } 
        return JsonResponse(context,safe = False)
    return JsonResponse({"success":False}, status = 400)

def division_by_rly1(request):
    if request.method == "GET" and request.is_ajax():
        rly_1=request.GET.get('rly_1')
        print(rly_1,'_________________________aaaaaa________________')
          
        division=list(m1.railwayLocationMaster.objects.filter(location_type='DIV',parent_location_code=rly_1).order_by('location_code').values('location_code').distinct('location_code'))
        l=[]
        for i in division:
            l.append(i['location_code'])
        print(l)    
        context={
            'division':l,
        } 
        return JsonResponse(context,safe = False)
    return JsonResponse({"success":False}, status = 400)

# niyati 150622 end     

from django.db.models import Q
from django.contrib import messages
#vishnu  location searching function
def search_location(request):
    
    
    # if request.method== 'POST':
    #     person = request.POST['person']
    #     print(person)
        
    #     des_location=models.MyUser.objects.filter(username__icontains=person )
    #     print('des_location', des_location)
    #     return render(request,'keyword_location_search.html', {'des_location':des_location})
    # else:
    #     person = False
    # all_location=models.railwayLocationMaster.objects.all()
        
    #     print('HELLO')
        
    #     # all_location=models.railwayLocationMaster.objects.none()
    # else:
    #     all_unit=models.railwayLocationMaster.objects.filter(rly_unit_code__icontains=query)
    #     all_location_code=models.railwayLocationMaster.objects.filter(location_code__icontains=query)
    #     all_location_type=models.railwayLocationMaster.objects.filter(location_type__icontains=query)
    #     all_location=all_unit.union(all_location_code).union(all_location_type)
    # # if all_location.count()== 0:
    #     messages.warning(request, "No search result found. Please refine your query ")
    
    #searching filter data
    # insp = []
    # if request.method == 'POST':
    #     q=request.POST.get('location')
    #     q1=request.POST.get('location1')
    #     multiple_q=Q(Q(location_description__contains=q) | Q(parent_location_code__contains=q1))
    #     insp=models.railwayLocationMaster.objects.filter(multiple_q, location_type__in=['DIV','ZR']).values('location_code','location_type','last_update','rly_unit_code')
    #     print('ghhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh', insp)
    # else:
    #     print('hehhhhhhhhhhhhhhhhhhhhhh')
        
    #Find railway location/Zone
    list1=m1.railwayLocationMaster.objects.filter(location_type='ZR').values('location_code')
    list2=[]
    for i in list1:
        # print(i['location_code'],'_________')
        list2.append(i['location_code'])
    
    list3=m1.railwayLocationMaster.objects.filter(location_type='DIV').values('location_code')
    list4=[]
    for i in list3:
        # print(i['location_code'],'_________')
        list4.append(i['location_code'])  
    list5=m1.departMast.objects.all().values('department_name')
    list6=[]
    for i in list5:
        # print(i['department_name'],'_________')
        list6.append(i['department_name'])
    
    list7=m1.Level_Desig.objects.all().values('designation')
    list8=[]
    for i in list7:
        # print(i['designation'],'_________')
        list8.append(i['designation'])

    if request.method== 'POST':
        query = request.POST['query']
        print(query)
        que=Q()
        for word in query.split():
            que &=Q(observation__icontains=word)
        
        des_location=m1.Item_details.objects.filter(que)
        # par_location=models.railwayLocationMaster.objects.filter()
        # all_location=des_location.union(par_location)
        # query=[]
        print('des_location', des_location)
        return render(request,'keyword_location_search.html', {'des_location':des_location})
    else:
        query = False
    
    
    #Find division
    # ins=[]
    # if request.method =="POST":
    #     s=request.POST.get('location')
    #     list3=models.railwayLocationMaster.objects.filter(location_type='DIV', parent_location_code=s).values('location_code', 'parent_location_code')
    #     list4=[]
    #     for i in list3:
    #         print(i['location_code'],'_________')
    #         list4.append(i['location_code'])
    #     print('dhhddddddddddddddddddd',ins)
    # else:
    #     print('hhhhhhhhhhhhhh',ins)
        
    #find all list data 
    # insp=models.Level_Desig.objects.filter(rly_unit__location_type__in=['DIV', 'ZR']).values('cat_id','designation','rly_unit__location_code','rly_unit__location_type','rly_unit__last_update','rly_unit__rly_unit_code','department_code__department_name')
    # insp=models.Level_Desig.objects.all().values('cat_id','rly_unit__location_type','designation','rly_unit__last_update','department_code__department_name')
    # print("insp",insp)
    
    design=m1.Item_details.objects.all().values('item_no','inspection_no__inspection_note_no','modified_on','observation','inspection_no__division','inspection_no__zone')
    
    context={'zone':list2,'division':list4,'dept':list6, 'desi':list8,  'design':design }
    return render(request, 'search_location.html', context)


def keyword_location_search(request):
    if request.method== 'POST':
        query = request.POST.get('query')
        que=Q()
        for word in query.split():
            que &=Q(observation__icontains=word)
            
        des_location=list(m1.Item_details.objects.filter(que).values())
        print(des_location)
        
        # des_location=list(m1.Item_details.objects.filter().values('modified_on'))
        for i in range(len(des_location)):
            if des_location[i]['modified_on']!=None:
                x=des_location[i]['modified_on'].strftime('%d'+'-'+'%m'+'-'+'%Y')
                des_location[i].update({'modified_on':x})

        #des_location=m1.Item_details.objects.filter(Q(observation__icontains=query) |Q(item_no__icontains=query) |Q(inspection_no__division__icontains=query) |Q(inspection_no__zone__icontains=query) )
        # render(request,'keyword_location_search.html', {'des_location':des_location})
        
        context={'des_location':des_location}

        return render(request,'keyword_location_search.html',context )
    else:
        return render(request,'keyword_location_search.html')
        
    
    

def search_locat_ajax(request):
    try:
        if request.method== 'GET' and request.is_ajax():
            grou=request.GET.get("group")
            ins=list(m1.railwayLocationMaster.objects.filter(location_type='DIV',parent_location_code=grou).values('location_code', 'rly_unit_code'))
            return JsonResponse({'ins':ins}, safe=False)
        return JsonResponse({'success':False}, status=400)
    except Exception as e:
        print(e)
        
    
def search_desig_ajax(request):
    try:
        if request.method== 'GET' and request.is_ajax():
            grou=request.GET.get("groupss")
            ins=list(m1.Level_Desig.objects.filter(rly_unit=grou).values('designation'))
            return JsonResponse({'ins':ins}, safe=False)
        return JsonResponse({'success':False}, status=400)
    except Exception as e:
        print(e)


from django.template.loader import get_template
from xhtml2pdf import pisa




def fetch_desig_ajax(request):
    try:
        if request.method == 'GET' and request.is_ajax():
            location_code=request.GET.get("location_code")
            location_type=request.GET.get("location_type")
            dept=request.GET.get("dept")
            inspected_on=request.GET.get('inspected_on')
            print(inspected_on)
            mydata={}
            grou=(location_code, location_type, dept, inspected_on)
            print(grou,'tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt')
            ins=list(m1.Inspection_details.objects.filter(zone=location_code).values('inspection_no','inspection_note_no','dept','division','zone','created_on','inspected_on'))
            for i in range(len(ins)):
                if ins[i]['inspected_on']!=None:
                    x=ins[i]['inspected_on'].strftime('%d'+'-'+'%m'+'-'+'%Y')
                    ins[i].update({'inspected_on':x})
            #print(ins, 'inspection_no')
            
            # ins_no=list(m1.Inspection_details.objects.filter(zone=location_code, location=location_type,dept=dept,).values('inspection_no'))
            for i in ins:
                
                # ins_no=list(m1.Item_details.objects.filter(inspection_no=i['inspection_no']).values('observation','inspection_no_id__zone','inspection_no_id__dept', 'inspection_no_id__division', 'inspection_no_id__location','inspection_no_id__inspected_on','inspection_no_id__created_on','inspection_no_id__inspection_no','inspection_no_id__inspection_note_no'))
                # print(ins_no, 'dddddddddddddddddddddddddddddddddddddddddddddddddddddddd')
                mydata.update({'ins':ins,'grou':grou,'location_code':location_code, 'location_type':location_type,'dept':dept,})
            print(mydata,'444444444444444444444444444444444444444444444444444444')
            return JsonResponse(ins, safe=False)
        return JsonResponse({'success':False}, status=400)
    except Exception as e:
        print(e)


from xhtml2pdf import pisa

def search_location_detail(request, pk):
    info=list(m1.Inspection_details.objects.filter(inspection_no=pk).values().distinct())
    #convert date dd-mm-yyyy
    for i in range(len(info)):
        if info[i]['inspected_on']!=None:
            x=info[i]['inspected_on'].strftime('%d'+'-'+'%m'+'-'+'%Y')
            info[i].update({'inspected_on':x})
    
    # pdf generate code
    # inspectionDetails=m1.Inspection_details.objects.filter(inspection_no=pk)
    # itemDetails=m1.Item_details.objects.filter(inspection_no=inspectionDetails[0].inspection_no)
    
    # print(itemDetails[0].observation)
    

    obj={}
    total=1
    for m2 in info:
        #convert date dd-mm-yyyy
        # x=m1.Inspection_details.objects.filter(inspection_no=m2['inspection_no_id'])[0].inspected_on
        # x=x.strftime('%d'+'-'+'%m'+'-'+'%Y')
        # inspectionDetails=m1.Inspection_details.objects.filter(inspection_no=pk)
        # itemDetails=m1.Item_details.objects.filter(inspection_no=inspectionDetails[0].inspection_no)
        #print(itemDetails[0].observation)
    
        
        # print(itemDetails[0].modified_on)
        
        temdata = {str(total):{"inspection_no":m2['inspection_no'], 
                               'inspection_note_no':m2['inspection_note_no'],
                               'inspection_officer':m2['inspection_officer'],
                               'zone':m2['zone'],
                            #    'observation':itemDetails[0].observation,
                            #    'modified_on':itemDetails[0].modified_on,
                               'division':m2['division'],
                               'location':m2['location'],
                               'inspected_on':m2['inspected_on'],
                               'modified_on':m2['modified_on']}}
        print(temdata, 'gfggggggggggggggggggggggggggggggggg')
        
    
        
        obj.update(temdata)
        total=total+1
        # print(temdata,"********************") 
    
    # print(obj,'tyyytytytytytytytytyty')
    lent=len(obj)
    # print(lent, 'xxxxxxxxxxxxxxxxxxxxxxxxxxxx')

    context={'info':info, 'obj': obj, 'lent':lent,}
    pdf=render_to_pdf('search_location_detail.html', context) 
    return HttpResponse(pdf, content_type='application/pdf')



def search_list_created_checklist(request):
    obj=m1.Inspection_Checklist.objects.all().values('checklist_id', 'checklist_title','inspection_type','status','created_by','created_on')[::-1]
    # print(obj)
    for i in range(len(obj)):
        if obj[i]['created_on']!=None:
            x=obj[i]['created_on'].strftime('%d'+'-'+'%m'+'-'+'%Y')
            obj[i].update({'created_on':x})
            
    context={'obj':obj}
    template_name='search_list_created_checklist.html'
        
    return render(request, template_name, context)

from .forms import *
import  json



def search_createchecklist(request):
    if request.method =='POST':
        # import pdb
        # pdb.set_trace()
        checklist_title=request.POST.get('checklist_title')
        print(checklist_title)
        inspection_type=request.POST.get('inspection_type')
        print(inspection_type)
        activities=request.POST.getlist('activities')
        print(activities)
        status=request.POST.get('draft')
        print(status)
        # activities = ['test1','test2']
        # contex={'checklist_title','inspection_type'}
        
        createchecklist=m1.Inspection_Checklist(checklist_title=checklist_title, inspection_type=inspection_type, status=status)
        
        createchecklist.save()
        print(createchecklist)
        # inspection_Activity
        for i in range(len(activities)):
            inspection_Activity=m1.Inspection_Activity(activities=activities[i])
            inspection_Activity.checklist_id=Inspection_Checklist.objects.get(checklist_id=createchecklist.checklist_id)
            inspection_Activity.save()
        
        return redirect('/search_list_created_checklist/')
 
    return render(request, 'search_createchecklist.html', {"INSPECTION_TYPE":INSPECTION_TYPE })


def search_editchecklist(request, pk):    
    inspection_Checklist=m1.Inspection_Checklist.objects.get(checklist_id=pk)
    print(inspection_Checklist)
    ass=m1.Inspection_Activity.objects.filter(checklist_id=int(inspection_Checklist.checklist_id)).values('activities')
    print(ass, 'ddddddddddddddddddddddddddddd')
    if request.method =='POST':
        # import pdb
        # pdb.set_trace()
        checklist_title=request.POST.get('checklist_title')
        inspection_type=request.POST.get('inspection_type')
        activities=request.POST.getlist('activities')
        status=request.POST.get('draft')
        # activities = ['test1','test2']
        # contex={'checklist_title','inspection_type'}
        inspection_Checklist=m1.Inspection_Checklist.objects.filter(checklist_id=pk).update(checklist_title=checklist_title, inspection_type=inspection_type, status=status)
        

        inspection_Activity
        for i in range(len(activities)):
            inspection_Activity=m1.Inspection_Activity(activities=activities[i])
            inspection_Activity.checklist_id=Inspection_Checklist.objects.get(checklist_id=inspection_Checklist.checklist_id)
            inspection_Activity=m1.Inspection_Activity.objects.filter(activity_id=pk).update(checklist_id=inspection_Checklist.checklist_id)
        
        return redirect('/search_list_created_checklist/')
    
    
    
    return render(request, 'search_createchecklist.html',{'ass':ass, 'inspection_Checklist':inspection_Checklist, "INSPECTION_TYPE":INSPECTION_TYPE })


def search_delete_flag(request, pk):
    flag=m1.Inspection_Checklist.objects.get(checklist_id=pk)
    flag.delete_flag=True
    flag.save()
    return HttpResponseRedirect('/search_list_created_checklist/')  
 



def search_checklist_detail(request, pk):
    info=list(m1.Inspection_Checklist.objects.filter(checklist_id=pk).values().distinct())
    #convert date dd-mm-yyyy
    for i in range(len(info)):
        if info[i]['created_on']!=None:
            x=info[i]['created_on'].strftime('%d'+'-'+'%m'+'-'+'%Y')
            info[i].update({'created_on':x})
            
    obj={}
    total=1
    for m2 in info:

        
        temdata = {str(total):{"checklist_id":m2['checklist_id'], 
                               'checklist_title':m2['checklist_title'],
                               'created_on':m2['created_on'],
                               'created_by':m2['created_by'],
                               
                               'inspection_type':m2['modified_on']}}
        print(temdata, 'gfggggggggggggggggggggggggggggggggg')
        obj.update(temdata)
        total=total+1
        # print(temdata,"********************") 
    
    # print(obj,'tyyytytytytytytytytyty')
    lent=len(obj)
    # print(lent, 'xxxxxxxxxxxxxxxxxxxxxxxxxxxx')

    context={'info':info, 'obj': obj, 'lent':lent,}
    pdf=render_to_pdf('search_checklist_detail.html', context) 
    return HttpResponse(pdf, content_type='application/pdf')

def search_checklist_views(request, pk):
    inspection_Checklist=m1.Inspection_Checklist.objects.get(checklist_id=pk)
    print(inspection_Checklist)
    
    return render(request, 'search_checklist_views.html',{'inspection_Checklist':inspection_Checklist, "INSPECTION_TYPE":INSPECTION_TYPE })
    


# def search_location_detail(request, pk):
   
#     info=list(m1.Item_details.objects.filter(item_no=pk).values().distinct())
#     # print(info,'shhhhhhhhhhhh')

    
#     #convert date dd-mm-yyyy
#     for i in range(len(info)):
#         if info[i]['modified_on']!=None:
#             x=info[i]['modified_on'].strftime('%d'+'-'+'%m'+'-'+'%Y')
#             info[i].update({'modified_on':x})
    
    
    
#     # pdf generate code

#     obj={}
#     total=1
#     for m2 in info:
#         #convert date dd-mm-yyyy
#         x=m1.Inspection_details.objects.filter(inspection_no=m2['inspection_no_id'])[0].inspected_on
#         x=x.strftime('%d'+'-'+'%m'+'-'+'%Y')
#         temdata = {str(total):{"item_no":m2['item_no'], 
#                                'inspection_note_no':m1.Inspection_details.objects.filter(inspection_no=m2['inspection_no_id'])[0].inspection_note_no,
#                                'inspection_officer':m1.Inspection_details.objects.filter(inspection_no=m2['inspection_no_id'])[0].inspection_officer,
#                                'zone':m1.Inspection_details.objects.filter(inspection_no=m2['inspection_no_id'])[0].zone,
#                                'location':m1.Inspection_details.objects.filter(inspection_no=m2['inspection_no_id'])[0].location,
#                                'division':m1.Inspection_details.objects.filter(inspection_no=m2['inspection_no_id'])[0].division,
#                                'inspected_on':x,
                               
#                                'observation':m2['observation'], 'modified_on':m2['modified_on']}}
#         # print(temdata, 'gfggggggggggggggggggggggggggggggggg')
        
    
        
#         obj.update(temdata)
#         total=total+1
#         # print(temdata,"********************") 
    
#     # print(obj,'tyyytytytytytytytytyty')
#     lent=len(obj)
#     # print(lent, 'xxxxxxxxxxxxxxxxxxxxxxxxxxxx')

#     context={'info':info, 'obj': obj, 'lent':lent,}
#     pdf=render_to_pdf('search_location_detail.html', context) 
#     return HttpResponse(pdf, content_type='application/pdf')
#     # return render(request, template_name, context)


# def fetch_desig_ajax(request):
#     try:
#         if request.method == 'GET' and request.is_ajax():
#             location_code=request.GET.get("location_code")
#             location_type=request.GET.get("location_type")
#             dept=request.GET.get("dept")
#             mydata={}
#             grou=(location_code, location_type, dept)
#             print(grou,'tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt')
#             ins=list(m1.Inspection_details.objects.filter(zone=location_code).values('inspected_on'))
#             ins=list(m1.Inspection_details.objects.filter(zone=location_code).values('inspection_no','inspection_note_no','dept','division','zone','created_on','inspected_on'))
#             print(ins, 'inspection_no')
#             # ins_no=list(models.Inspection_details.objects.filter(zone=location_code, location=location_type,dept=dept,).values('inspection_no'))
#             for i in ins:
                
#                 ins_no=list(m1.Item_details.objects.filter(inspection_no=i['inspection_no']).values('observation','inspection_no_id__zone','inspection_no_id__dept', 'inspection_no_id__division', 'inspection_no_id__location','inspection_no_id__inspected_on','inspection_no_id__created_on','inspection_no_id__inspection_no','inspection_no_id__inspection_note_no'))
#                 print(ins_no, 'dddddddddddddddddddddddddddddddddddddddddddddddddddddddd')
#                 mydata.update({'ins':ins,'grou':grou,'location_code':location_code, 'location_type':location_type,'dept':dept,})
#             print(mydata)
#             return JsonResponse(ins, safe=False)
#         return JsonResponse({'success':False}, status=400)
#     except Exception as e:
#         print(e)


#end here vishnu

#bhart start
def view_inspection_draft(request):
    try:

        print("#########################")
        # result=list(m1.Item_details.objects.filter(status_flag=1).values('inspection_no_id','observation','item_title'))
        # result1=list(m1.Inspection_details.objects.filter(inspection_no=result[0]['inspection_no_id']).values('zone','dept','division'))
        # print(result,result1)
        context={
            # 'result':result,
            # 'zone':result1[0]['zone'],
            # 'dept':result1[0]['dept'],
            # 'division':result1[0]['division'],
        }
        return render(request, 'view_draft.html',context)
    except Exception as e:
        print("e==",e) 


#bharti end


def forgotPassword(request):
    try:
        if request.method == "POST":
            _email = request.POST.get('email').strip()

            try:
                userObj = user.objects.get(email=_email)
                #print(userObj)
            except Exception as e:
                messages.error(request, 'Please enter registed email.')
                return HttpResponseRedirect('/rkvy_forgotPassword')

            email_context = {
                "email": userObj.email,
                'domain': 'railkvydev.indianrailways.gov.in',
                'site_name': 'Kaushal Vikas',
                "uid": urlsafe_base64_encode(force_bytes(userObj.pk)),
                "user": userObj,
                'token': default_token_generator.make_token(userObj),
                'protocol': 'http',
            }
            email_template_name = "accounts/email_forgotPassword_body.txt"
            email_body = render_to_string(email_template_name, email_context)
            try:
                #print("trying to send mail")
                #print(userObj.email)
                try:
                    # send_mail("Verify Your Mail", email_body, 'crisdlwproject@gmail.com',
                    #          [f'{userObj.email}'], fail_silently=False)


                    #saud faisal (28-08-2021) -----
                    subject="Reset password for RKVY login"
                    To=userObj.email
                    email_body1='<p>'+email_body+'</p>'
                    MailSend(subject,email_body1,To)
                    #end here
                    return HttpResponse('Verification Email has been successfully sent.(see also spam folder)')
                except:
                    print("error on sending")
                    messages.error(
                        request, 'Verification Email failed. Please Try Again.')
            except:
                messages.error(
                    request, 'Something went wrong.')
            return HttpResponseRedirect('/forgotPassword')

        return render(request, "forgotPassword.html")
    except Exception as e: 
       print(e)


def passwordVerification(request):
    email2=request.POST.get('email2')
    print('email2')
    return render(request, "resetPassword.html",{'validLink': True,'email':email2, })

def forgotPasswordVerification(request):
    try:
        try:
            print('00000000')
            print(request.POST.get('email2'))
            userObj = user.objects.get(email= request.POST.get('email2'))
            print(userObj)
            
        except(TypeError, ValueError, OverflowError, user.DoesNotExist):
            print("%&^%&^%&^%&^@#%&^@#%&^@%#&@%#&")
            userObj = None

        if userObj is not None:
            print('1111')

            # return HttpResponseRedirect('/reset_password')
            if request.method == "POST":
                try:
                    _password = request.POST.get('new_password')
                    userObj.set_password(_password)
                    userObj.save()
                    
                    messages.success(request, "Password Updated Successfully")
                except Exception as e:
                    print(e)
                    messages.error(request, "Password Change Failed.")
                return HttpResponseRedirect('/login')

            return render(request, "resetPassword.html", {'validLink': True, })
        else:
            return HttpResponse('Email not registered')
    except Exception as e: 
        print(e)

# Aman start
def new_page(request):
    return render(request,'new_page.html')

def new_data(request):
    railway = request.GET.get('railway')
    s = request.GET.get('status')
    print(railway,s)
    data=[]
    if int(s)==0:
        print("yes")
        t = m1.Inspection_details.objects.filter(zone=railway).values('inspection_note_no','inspected_on','inspection_officer','zone','division','dept','status_flag')
        print(t)
        for i in t:
            if i['status_flag']!=None:
                temp={}
                temp['ins_no']=i['inspection_note_no']
                temp['ins_date']=i['inspected_on'].strftime("%d-%b-%Y")
                temp['desig']=i['inspection_officer']
                t1=m1.railwayLocationMaster.objects.filter(location_code=i['zone']).values('location_description')
                temp['railway']=t1[0]['location_description']
                t1=m1.railwayLocationMaster.objects.filter(location_code=i['division']).values('location_description')
                temp['division']=t1[0]['location_description']
                temp['dept']=i['dept']
                if i['status_flag']==1:
                    temp['status']="Pending Compliance"
                elif i['status_flag']==2:
                    temp['status']="Partial Compliance"
                elif i['status_flag']==3:
                    temp['status']="Closed"
                data.append(temp)
    elif int(s)==1:
        t = m1.Inspection_details.objects.filter(zone=railway,status_flag=s).values('inspection_note_no','inspected_on','inspection_officer','zone','division','dept','status_flag')
        for i in t:
            temp={}
            temp['ins_no']=i['inspection_note_no']
            temp['ins_date']=i['inspected_on'].strftime("%d-%b-%Y")
            temp['desig']=i['inspection_officer']
            t1=m1.railwayLocationMaster.objects.filter(location_code=i['zone']).values('location_description')
            temp['railway']=t1[0]['location_description']
            t1=m1.railwayLocationMaster.objects.filter(location_code=i['division']).values('location_description')
            temp['division']=t1[0]['location_description']
            temp['dept']=i['dept']
            temp['status']="Pending Compliance"
            data.append(temp)
    elif int(s)==2:
        t = m1.Inspection_details.objects.filter(zone=railway,status_flag=s).values('inspection_note_no','inspected_on','inspection_officer','zone','division','dept','status_flag')
        for i in t:
            temp={}
            temp['ins_no']=i['inspection_note_no']
            temp['ins_date']=i['inspected_on'].strftime("%d-%b-%Y")
            temp['desig']=i['inspection_officer']
            t1=m1.railwayLocationMaster.objects.filter(location_code=i['zone']).values('location_description')
            temp['railway']=t1[0]['location_description']
            t1=m1.railwayLocationMaster.objects.filter(location_code=i['division']).values('location_description')
            temp['division']=t1[0]['location_description']
            temp['dept']=i['dept']
            temp['status']="Partial Compliance"
            data.append(temp)
    elif int(s)==3:
        t = m1.Inspection_details.objects.filter(zone=railway).values('inspection_note_no','inspected_on','inspection_officer','zone','division','dept','status_flag')
        for i in t:
            temp={}
            temp['ins_no']=i['inspection_note_no']
            temp['ins_date']=i['inspected_on'].strftime("%d-%b-%Y")
            temp['desig']=i['inspection_officer']
            t1=m1.railwayLocationMaster.objects.filter(location_code=i['zone']).values('location_description')
            temp['railway']=t1[0]['location_description']
            t1=m1.railwayLocationMaster.objects.filter(location_code=i['division']).values('location_description')
            temp['division']=t1[0]['location_description']
            temp['dept']=i['dept']
            temp['status']="Closed"
            data.append(temp)
    context={'data':data}
    return JsonResponse(context,safe=False)

def new_data1(request):
    railway = request.GET.get('div')
    s = request.GET.get('status')
    print(railway,s)
    data=[]
    if int(s)==0:
        print("yes")
        t = m1.Inspection_details.objects.filter(division=railway).values('inspection_note_no','inspected_on','inspection_officer','zone','division','dept','status_flag')
        print(t)
        for i in t:
            if i['status_flag']!=None:
                temp={}
                temp['ins_no']=i['inspection_note_no']
                temp['ins_date']=i['inspected_on'].strftime("%d-%b-%Y")
                temp['desig']=i['inspection_officer']
                t1=m1.railwayLocationMaster.objects.filter(location_code=i['zone']).values('location_description')
                temp['railway']=t1[0]['location_description']
                t1=m1.railwayLocationMaster.objects.filter(location_code=i['division']).values('location_description')
                temp['division']=t1[0]['location_description']
                temp['dept']=i['dept']
                if i['status_flag']==1:
                    temp['status']="Pending Compliance"
                elif i['status_flag']==2:
                    temp['status']="Partial Compliance"
                elif i['status_flag']==3:
                    temp['status']="Closed"
                data.append(temp)
    elif int(s)==1:
        t = m1.Inspection_details.objects.filter(division=railway,status_flag=s).values('inspection_note_no','inspected_on','inspection_officer','zone','division','dept','status_flag')
        for i in t:
            temp={}
            temp['ins_no']=i['inspection_note_no']
            temp['ins_date']=i['inspected_on'].strftime("%d-%b-%Y")
            temp['desig']=i['inspection_officer']
            t1=m1.railwayLocationMaster.objects.filter(location_code=i['zone']).values('location_description')
            temp['railway']=t1[0]['location_description']
            t1=m1.railwayLocationMaster.objects.filter(location_code=i['division']).values('location_description')
            temp['division']=t1[0]['location_description']
            temp['dept']=i['dept']
            temp['status']="Pending Compliance"
            data.append(temp)
    elif int(s)==2:
        t = m1.Inspection_details.objects.filter(division=railway,status_flag=s).values('inspection_note_no','inspected_on','inspection_officer','zone','division','dept','status_flag')
        for i in t:
            temp={}
            temp['ins_no']=i['inspection_note_no']
            temp['ins_date']=i['inspected_on'].strftime("%d-%b-%Y")
            temp['desig']=i['inspection_officer']
            t1=m1.railwayLocationMaster.objects.filter(location_code=i['zone']).values('location_description')
            temp['railway']=t1[0]['location_description']
            t1=m1.railwayLocationMaster.objects.filter(location_code=i['division']).values('location_description')
            temp['division']=t1[0]['location_description']
            temp['dept']=i['dept']
            temp['status']="Partial Compliance"
            data.append(temp)
    elif int(s)==3:
        t = m1.Inspection_details.objects.filter(division=railway).values('inspection_note_no','inspected_on','inspection_officer','zone','division','dept','status_flag')
        for i in t:
            temp={}
            temp['ins_no']=i['inspection_note_no']
            temp['ins_date']=i['inspected_on'].strftime("%d-%b-%Y")
            temp['desig']=i['inspection_officer']
            t1=m1.railwayLocationMaster.objects.filter(location_code=i['zone']).values('location_description')
            temp['railway']=t1[0]['location_description']
            t1=m1.railwayLocationMaster.objects.filter(location_code=i['division']).values('location_description')
            temp['division']=t1[0]['location_description']
            temp['dept']=i['dept']
            temp['status']="Closed"
            data.append(temp)
    context={'data':data}
    return JsonResponse(context,safe=False)

def new_data2(request):
    railway = request.GET.get('dept')
    s = request.GET.get('status')
    print(railway,s)
    data=[]
    if int(s)==0:
        print("yes")
        t = m1.Inspection_details.objects.filter(dept=railway).values('inspection_note_no','inspected_on','inspection_officer','zone','division','dept','status_flag')
        print(t)
        for i in t:
            if i['status_flag']!=None:
                temp={}
                temp['ins_no']=i['inspection_note_no']
                temp['ins_date']=i['inspected_on'].strftime("%d-%b-%Y")
                temp['desig']=i['inspection_officer']
                t1=m1.railwayLocationMaster.objects.filter(location_code=i['zone']).values('location_description')
                temp['railway']=t1[0]['location_description']
                t1=m1.railwayLocationMaster.objects.filter(location_code=i['division']).values('location_description')
                temp['division']=t1[0]['location_description']
                temp['dept']=i['dept']
                if i['status_flag']==1:
                    temp['status']="Pending Compliance"
                elif i['status_flag']==2:
                    temp['status']="Partial Compliance"
                elif i['status_flag']==3:
                    temp['status']="Closed"
                data.append(temp)
    elif int(s)==1:
        t = m1.Inspection_details.objects.filter(dept=railway,status_flag=s).values('inspection_note_no','inspected_on','inspection_officer','zone','division','dept','status_flag')
        for i in t:
            temp={}
            temp['ins_no']=i['inspection_note_no']
            temp['ins_date']=i['inspected_on'].strftime("%d-%b-%Y")
            temp['desig']=i['inspection_officer']
            t1=m1.railwayLocationMaster.objects.filter(location_code=i['zone']).values('location_description')
            temp['railway']=t1[0]['location_description']
            t1=m1.railwayLocationMaster.objects.filter(location_code=i['division']).values('location_description')
            temp['division']=t1[0]['location_description']
            temp['dept']=i['dept']
            temp['status']="Pending Compliance"
            data.append(temp)
    elif int(s)==2:
        t = m1.Inspection_details.objects.filter(dept=railway,status_flag=s).values('inspection_note_no','inspected_on','inspection_officer','zone','division','dept','status_flag')
        for i in t:
            temp={}
            temp['ins_no']=i['inspection_note_no']
            temp['ins_date']=i['inspected_on'].strftime("%d-%b-%Y")
            temp['desig']=i['inspection_officer']
            t1=m1.railwayLocationMaster.objects.filter(location_code=i['zone']).values('location_description')
            temp['railway']=t1[0]['location_description']
            t1=m1.railwayLocationMaster.objects.filter(location_code=i['division']).values('location_description')
            temp['division']=t1[0]['location_description']
            temp['dept']=i['dept']
            temp['status']="Partial Compliance"
            data.append(temp)
    elif int(s)==3:
        t = m1.Inspection_details.objects.filter(dept=railway).values('inspection_note_no','inspected_on','inspection_officer','zone','division','dept','status_flag')
        for i in t:
            temp={}
            temp['ins_no']=i['inspection_note_no']
            temp['ins_date']=i['inspected_on'].strftime("%d-%b-%Y")
            temp['desig']=i['inspection_officer']
            t1=m1.railwayLocationMaster.objects.filter(location_code=i['zone']).values('location_description')
            temp['railway']=t1[0]['location_description']
            t1=m1.railwayLocationMaster.objects.filter(location_code=i['division']).values('location_description')
            temp['division']=t1[0]['location_description']
            temp['dept']=i['dept']
            temp['status']="Closed"
            data.append(temp)
    context={'data':data}
    return JsonResponse(context,safe=False)

def new_data3(request):
    railway = request.GET.get('dept')
    s = request.GET.get('status')
    print(railway,s)
    data=[]
    if int(s)==0:
        print("yes")
        t = m1.Inspection_details.objects.filter(inspection_officer__contains=railway).values('inspection_note_no','inspected_on','inspection_officer','zone','division','dept','status_flag')
        print(t)
        for i in t:
            if i['status_flag']!=None:
                temp={}
                temp['ins_no']=i['inspection_note_no']
                temp['ins_date']=i['inspected_on'].strftime("%d-%b-%Y")
                temp['desig']=i['inspection_officer']
                t1=m1.railwayLocationMaster.objects.filter(location_code=i['zone']).values('location_description')
                temp['railway']=t1[0]['location_description']
                t1=m1.railwayLocationMaster.objects.filter(location_code=i['division']).values('location_description')
                temp['division']=t1[0]['location_description']
                temp['dept']=i['dept']
                if i['status_flag']==1:
                    temp['status']="Pending Compliance"
                elif i['status_flag']==2:
                    temp['status']="Partial Compliance"
                elif i['status_flag']==3:
                    temp['status']="Closed"
                data.append(temp)
    elif int(s)==1:
        t = m1.Inspection_details.objects.filter(dept=railway,status_flag=s).values('inspection_note_no','inspected_on','inspection_officer','zone','division','dept','status_flag')
        for i in t:
            temp={}
            temp['ins_no']=i['inspection_note_no']
            temp['ins_date']=i['inspected_on'].strftime("%d-%b-%Y")
            temp['desig']=i['inspection_officer']
            t1=m1.railwayLocationMaster.objects.filter(location_code=i['zone']).values('location_description')
            temp['railway']=t1[0]['location_description']
            t1=m1.railwayLocationMaster.objects.filter(location_code=i['division']).values('location_description')
            temp['division']=t1[0]['location_description']
            temp['dept']=i['dept']
            temp['status']="Pending Compliance"
            data.append(temp)
    elif int(s)==2:
        t = m1.Inspection_details.objects.filter(dept=railway,status_flag=s).values('inspection_note_no','inspected_on','inspection_officer','zone','division','dept','status_flag')
        for i in t:
            temp={}
            temp['ins_no']=i['inspection_note_no']
            temp['ins_date']=i['inspected_on'].strftime("%d-%b-%Y")
            temp['desig']=i['inspection_officer']
            t1=m1.railwayLocationMaster.objects.filter(location_code=i['zone']).values('location_description')
            temp['railway']=t1[0]['location_description']
            t1=m1.railwayLocationMaster.objects.filter(location_code=i['division']).values('location_description')
            temp['division']=t1[0]['location_description']
            temp['dept']=i['dept']
            temp['status']="Partial Compliance"
            data.append(temp)
    elif int(s)==3:
        t = m1.Inspection_details.objects.filter(dept=railway).values('inspection_note_no','inspected_on','inspection_officer','zone','division','dept','status_flag')
        for i in t:
            temp={}
            temp['ins_no']=i['inspection_note_no']
            temp['ins_date']=i['inspected_on'].strftime("%d-%b-%Y")
            temp['desig']=i['inspection_officer']
            t1=m1.railwayLocationMaster.objects.filter(location_code=i['zone']).values('location_description')
            temp['railway']=t1[0]['location_description']
            t1=m1.railwayLocationMaster.objects.filter(location_code=i['division']).values('location_description')
            temp['division']=t1[0]['location_description']
            temp['dept']=i['dept']
            temp['status']="Closed"
            data.append(temp)
    context={'data':data}
    return JsonResponse(context,safe=False)

def dashboard(request):
    return render(request,'dashboard.html')
# connection = psycopg2.connect("dbname=200622 user=postgres password=9911772843")
def get_data(request):
    sd = request.GET.get('sd')
    ed = request.GET.get('ed')
    data=m1.railwayLocationMaster.objects.filter(location_type='ZR').values('location_description','location_code').order_by('location_description')
    data1=m1.railwayLocationMaster.objects.filter(location_type='DIV').values('location_description','location_code').order_by('location_description')
    data2=m1.departMast.objects.values('department_name').distinct().order_by('department_name')
    data3=m1.Designation_Master.objects.values('master_name').distinct().order_by('master_name')
    list1=[]
    list2=[]
    list3=[]
    list4=[]
    for i in data:
        temp={}
        c1=0
        c2=0
        c3=0
        c4=0
        t = m1.Inspection_details.objects.filter(zone=i['location_code'],inspected_on__gte=sd,inspected_on__lte=ed).values()
        if len(t)>0:
            for k in t:
                if k['status_flag']!=None and k['status_flag']>0 and k['status_flag']<=3:
                    c4+=1
            temp['count']=c4
        else:
            temp['count']=0
        for j in t:
            if j['status_flag']==3:
                c1+=1
            elif j['status_flag']==2:
                c2+=1
            elif j['status_flag']==1:
                c3+=1
        temp['c1']=c1
        temp['c2']=c2
        temp['c3']=c3     
        temp['loc']=i['location_description']
        temp['id']=i['location_code']
        list1.append(temp)
    for i in data1:
        temp={}
        t = m1.Inspection_details.objects.filter(division=i['location_code'],inspected_on__gte=sd,inspected_on__lte=ed).values()
        c1=0
        c2=0
        c3=0
        c4=0
        if len(t)>0:
            for k in t:
                if k['status_flag']!=None and k['status_flag']>0 and k['status_flag']<=3:
                    c4+=1
            temp['count']=c4
        else:
            temp['count']=0
        for j in t:
            if j['status_flag']==3:
                c1+=1
            elif j['status_flag']==2:
                c2+=1
            elif j['status_flag']==1:
                c3+=1
        temp['c1']=c1
        temp['c2']=c2
        temp['c3']=c3 
        temp['loc']=i['location_description']
        temp['id']=i['location_code']
        list2.append(temp)
    for i in data2:
        temp={}
        c1=0
        c2=0
        c3=0
        c4=0
        t = m1.Inspection_details.objects.filter(dept=i['department_name'],inspected_on__gte=sd,inspected_on__lte=ed).values()
        if len(t)>0:
            for k in t:
                if k['status_flag']!=None and k['status_flag']>0 and k['status_flag']<=3 :
                    c4+=1
            temp['count']=c4
        else:
            temp['count']=0
        temp['loc']=i['department_name']
        for j in t:
            if j['status_flag']==3:
                c1+=1
            elif j['status_flag']==2:
                c2+=1
            elif j['status_flag']==1:
                c3+=1
        temp['c1']=c1
        temp['c2']=c2
        temp['c3']=c3 
        list3.append(temp)
    for i in data3:
        temp={}
        c1=0
        c2=0
        c3=0
        t = m1.Inspection_details.objects.filter(inspection_officer__contains=i['master_name'],inspected_on__gte=sd,inspected_on__lte=ed).values()
        if len(t)>0:
            for k in t:
                if k['status_flag']!=None and k['status_flag']>0 and k['status_flag']<=3:
                    c4+=1
            temp['count']=c4
        else:
            temp['count']=0
        for j in t:
            if j['status_flag']==3:
                c1+=1
            elif j['status_flag']==2:
                c2+=1
            elif j['status_flag']==1:
                c3+=1
        temp['loc']=i['master_name']
        temp['c1']=c1
        temp['c2']=c2
        temp['c3']=c3 
        list4.append(temp)
    context={
        'list1':list1,
        'list2':list2,
        'list3':list3,
        'list4':list4,
    }
    return JsonResponse(context, safe = False)
# AMAN end

