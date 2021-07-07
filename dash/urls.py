from django.urls import path

from . import views
app_name = 'dash'
urlpatterns = [
    path('',views.dashboard,name="dashboard"),
    path('raiseticket',views.raise_ticket,name="raiseticket"),
    path('showticketform',views.showticketform,name="showticketform"),
    path('showreguser',views.showuserreg,name="showreguser"),
    path('registeruser',views.registeruser,name="registeruser"),
    path('showlogin',views.showlogin,name="showlogin"),
    path('login',views.loginuser,name="login"),
    path('showticket/<int:ticket_id>/',views.showticket,name="showticket"),
    path('logout',views.logoutuser,name='logout'),
    path('completeticket/<int:ticket_id>',views.completeticket,name="completeticket"),
    path('showuserlist',views.showuserlist,name="showuserlist"),
    path('api', views.getChartData.as_view(),name="chartapi"),
    path('api_data', views.getData.as_view(),name="getdata"),
    path('auth', views.authAPI,name="authapi"),
    path('getdataonauth', views.senddataontokenauth,name="getdataonauth"),


    
]