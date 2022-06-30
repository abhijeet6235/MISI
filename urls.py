"""inspection URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from inspects import views
# from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from myadmin import views as v2
from myadmin.views import *

from django.conf.urls import url  #by yashika restapi 24_feb_22
from rest_framework.authtoken import views as authviews #by yashika restapi 24_feb_22
from rest_framework import routers #app
# from myadmin import views
from rest_framework.authtoken.views import obtain_auth_token

from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('', views.home,name='home'),
    path('',views.loginUser,name='loginUser'),
    path('login/',views.loginUser,name='loginUser'),
    path('forgotPassword/',views.forgotPassword,name='forgotPassword'),

    #bharti start
    path('created_checklist/',views.created_checklist,name="created_checklist"),
    path('create_inspection_form/',views.create_inspection_form,name="create_inspection_form"),
    path('save_draft_data/',views.save_draft_data,name="save_draft_data"),
    path('nominate_officer/',views.nominate_officer,name="nominate_officer"),
    path('compliance_form/',views.compliance_form,name="compliance_form"),
    path('compliance_filterdata/',views.compliance_filterdata,name="compliance_filterdata"),
    path('compliance_filterdata_ajax',views.compliance_filterdata_ajax,name="compliance_filterdata_ajax"),
    path('admin_inspection_form/',views.admin_inspection_form,name='admin_inspection_form'),
    path('compliance_forward_reply/<int:item_no>/',views.compliance_forward_reply,name="compliance_forward_reply"),
    path('signup/',views.signup,name="signup"),
    path('fetch_emp/',views.fetch_emp,name="fetch_emp"),
    path('fetch_email_id/',views.fetch_email_id,name="fetch_email_id"),
    path('send_otp/',views.send_otp,name="send_otp"),
    path('employeeList/',v2.employeeList,name='employeeList'),
    path('viewEmployee_Det/',v2.viewEmployee_Det,name='viewEmployee_Det'),
    path('ajax/get_emp_detNew/',v2.get_emp_detNew,name='get_emp_detNew'),
    path('assign_role/', v2.assign_role, name='assign_role'),
    path('getDesigbyDepartment/',v2.getDesigbyDepartment,name='getDesigbyDepartment'),
    path('getsection_byshop1/', v2.getsection_byshop1, name="getsection_byshop1"),
    path('getrole_bydesig/', v2.getrole_bydesig, name="getrole_bydesig"),
    path('get_parentdesig/', v2.get_parentdesig, name="get_parentdesig"),
    path('getshopcode_bydept/', v2.getshopcode_bydept, name="getshopcode_bydept"),
    path('empregistNew/',v2.empregistNew,name='empregistNew'),
    path('ajax/get_emp_detNew/',v2.get_emp_detNew,name='get_emp_detNew'),

    path('open_empregistNew/<int:empno>/',v2.open_empregistNew,name='open_empregistNew'),
    path('add_designation/',v2.add_designation,name='add_designation'),
    path('getsection_byshop/', v2.getsection_byshop, name="getsection_byshop"),
    path('getshop_bydept/', v2.getshop_bydept, name="getshop_bydept"),
    path('post_bydept/', v2.post_bydept, name="post_bydept"),
    path('getpost_bydept/', v2.getpost_bydept, name="getpost_bydept"),
    path('add_post/', v2.add_post, name="add_post"),
    path('ajax/save_designation/',v2.save_designation,name='save_designation'),
    path('shop_section/',v2.shop_section,name='shop_section'),
    path('dept_data/', v2.dept_data, name="dept_data"),
    path('shop_data/', v2.shop_data, name="shop_data"),
    path('section_data/', v2.section_data, name="section_data"),
    path('shop_bydept/', v2.shop_bydept, name="shop_bydept"),
    path('section_bydept/',v2.section_bydept, name="section_bydept"),
    path('RoleAdd/',RoleAdd,name='RoleAdd'),
    path('division_by_rly/',v2.division_by_rly,name='division_by_rly'),
    path('ajaxDeleteRoleUser/', v2.ajaxDeleteRoleUser, name='ajaxDeleteRoleUser'),
    path('ajax/getDepartmentbyroles/',v2.getDepartmentbyroles,name='getDepartmentbyroles'),
    path('getDesigbyDepartment/',v2.getDesigbyDepartment,name='getDesigbyDepartment'),
    path('getshopcode_bydept/', v2.getshopcode_bydept, name="getshopcode_bydept"),
    path('div_by_rly/', v2.div_by_rly, name="div_by_rly"),

    path('ajaxRoleGen/', ajaxRoleGen, name='ajaxRoleGen'),
    path('userHome/', views.userHome,
         name="userHome"),
    path('adminuserHome/', v2.adminuserHome,
         name="adminuserHome"),
    path('inspect_logout/',views.inspect_logout,
         name="inspect_logout"),
    path('admin_logout/',v2.admin_logout,
         name="admin_logout"),
    path('inspect_logout/',views.inspect_logout,
         name="inspect_logout"),
    path('admin_changePassword/',v2.admin_changePassword,
        name="admin_changePassword"),
    path('inspect_changePassword/',views.inspect_changePassword,
    name="inspect_changePassword"),
    path('getdiv_rly/',views.getdiv_rly,
    name="getdiv_rly"),
    path('division_wise/',views.division_wise,
    name="division_wise"),
    path('create_inspection_details/',views.create_inspection_details,
    name="create_inspection_details"),
    path('headqwise/',views.headqwise,
    name="headqwise"),
    path('division_by_rly1/',views.division_by_rly1,
    name="division_by_rly1"),
    path('save_data/',views.save_data,
    name="save_data"),
    path('fetch_forward_reply/',views.fetch_forward_reply,
    name="fetch_forward_reply"),
    #niyati_start
    path('gm_list_officers/',views.gm_list_officers,name='gm_list_officers'),
    path('drm_officers/',views.drm_officers,name='drm_officers'),
    path('phod_officers/',views.phod_officers,name='phod_officers'),
    path('headqwise/',views.headqwise,name='headqwise'),
    path('getDesignation/',views.getDesignation,name='getDesignation'),
    path('division_wise/',views.division_wise,name='division_wise'),
    path('division_by_rly1/',views.division_by_rly1,name='division_by_rly1'), 

    path('getdiv_rly/',views.getdiv_rly,name='getdiv_rly'), 
    path('admin_inspection_form/',views.admin_inspection_form,name="admin_inspection_form"),
#niyati_end
    

    #bharti end
    path('view_inspection_draft/',views.view_inspection_draft,name="view_inspection_draft"),
   

    #amisha new
    path('compliance_marked_forward/',views.compliance_marked_forward,name="compliance_marked_forward"),
    path('board_officers/',views.board_officers,name="board_officers"),

    #vishnu new
    path('search_location/',views.search_location,name="search_location"),
    path('search_desig_ajax/',views.search_desig_ajax, name='search_desig_ajax'),
    path('search_locat_ajax/',views.search_locat_ajax, name='search_locat_ajax'),
    path('keyword_location_search/',views.keyword_location_search,name="keyword_location_search"),

    path('search_location_detail/<str:pk>/',views.search_location_detail,name="search_location_detail"),
    path('fetch_desig_ajax',views.fetch_desig_ajax, name='fetch_desig_ajax'),
    path('draft_inspection_form/',views.draft_inspection_form,name="draft_inspection_form"),
    path('search_createchecklist/',views.search_createchecklist,name="search_createchecklist"),
    path('search_editchecklist/<str:pk>/',views.search_editchecklist,name="search_editchecklist"),
    path('search_list_created_checklist/',views.search_list_created_checklist,name="search_list_created_checklist"),
    path('search_checklist_detail/<str:pk>/',views.search_checklist_detail,name="search_checklist_detail"),
    path('search_delete_flag/<str:pk>/',views.search_delete_flag,name="search_delete_flag"),
    path('search_checklist_views/<str:pk>/',views.search_checklist_views,name="search_checklist_views"),


    #vishnu end
    path('zonaluserHome/', views.zonaluserHome,
         name="zonaluserHome"),
    path('Divisonrequests/',views.Divisonrequests,
        name="Divisonrequests"),
    path('requests/',views.requests,
        name="requests"),
    path('Divisonrequests/',views.Divisonrequests,
        name="Divisonrequests"),
    

    #furqn
    path('dash_home/', views.dash_home, name='dash_home'),
    path('railway_zone/', views.railway_zone, name='railway_zone'),
    path('item_divsion/', views.item_divsion, name='item_divsion'),
    path('item_detail_view', views.item_detail_view, name='item_detail_view'),
    path('item_view_inspect/<str:item>/', views.item_view_inspect, name='item_view_inspect'),   #27.06.22

    # end furqan
    path('forgotPassword/', views.forgotPassword,
          name="forgotPassword"),
    path('check/',views.check,
        name="check"),
    path('forgotPasswordVerification',
        views.forgotPasswordVerification, name="forgotPasswordVerification"),
    path('passwordVerification',
        views.passwordVerification, name="passwordVerification"),
    # Aman
    path('dashboard/',views.dashboard,name="dashboard"),
    path('get_data',views.get_data,name="get_data"),
    path('new_page/',views.new_page,name="new_page"),
    path('new_data/',views.new_data,name="new_data"),
    path('new_data1/',views.new_data1,name="new_data1"),
    path('new_data2/',views.new_data2,name="new_data2"),
    path('new_data3/',views.new_data3,name="new_data3"),
    # Aman end 
    path('headquarterMaster/',v2.headquarterMaster,
        name="headquarterMaster"),
    path('deleteHeadQuarter/',v2.deleteHeadQuarter,
        name="deleteHeadQuarter"),
    path('editHeadquarter/',v2.editHeadquarter,
        name="editHeadquarter"), 
    path('getParentZones/',v2.getParentZones,
        name="getParentZones"),  
    path('fetchStateCity/',v2.fetchStateCity,
        name="fetchStateCity"),
    path('ajax/fetchEmployee/',v2.fetchEmployee,
        name="fetchEmployee"),

    path('ajax/fetchData/',v2.fetchData,
        name="fetchData"),
    path('ajax/buildInstituteRly/',v2.buildInstituteRly,
        name="buildInstituteRly"),
    path('editDivison/',v2.editDivison,
        name="editDivison"),
    path('deleteDivison/',v2.deleteDivison,
        name="deleteDivison"),
    path('DivisonMaster/',v2.DivisonMaster,
        name="DivisonMaster"),
    path('divisonuserHome/', views.divisonuserHome,
         name="divisonuserHome"),
    #tarun
    path('autoFetchLocation/',views.autoFetchLocation,name="autoFetchLocation"),

    
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

