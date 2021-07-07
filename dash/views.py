from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Ticket
from django.db.models.functions import TruncMonth
from django.db.models import Count

from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import Http404

from datetime import datetime
import qrcode

# Create your views here.
@login_required
def dashboard(request):
    try:
        t = Ticket.objects.filter(completed=False)
    except Ticket.DoesNotExist:
        raise Http404("Tickets do not exist")
    try:
        totalticks = Ticket.objects.all()
    except Ticket.DoesNotExist:
        raise Http404("Tickets donot exist")
    try:
        completedticks = Ticket.objects.filter(completed=True)
    except Ticket.DoesNotExist:
        raise Http404("Tickets donot exist")

   
    context = {
        'ticketlist':t,
        'nooftickets': len(totalticks),
        'pendingtickets': len(t),
        'completedtickets': int((len(completedticks)/len(totalticks))*100),
        'upcomingduedate' : Ticket.objects.latest('-duedate').duedate.date,
    
    }
    return render(request, 'dash/dashboard.html',context)

def showticketform(request):
    return render(request,'dash/raiseticket.html',{})

def raise_ticket(request):
    title = request.POST['title']
    description = request.POST['description']
    customer_name = request.POST['cust_name']
    customer_email = request.POST['cust_email']
    duedate = request.POST['duedate']
    tick = Ticket(title=title,description=description,customer_name=customer_name,customer_email=customer_email,duedate=duedate)
    try:
        tick.save()
    except OSError as e:
        print(e)
    
    return HttpResponseRedirect(reverse('dash:showticketform'))

def showuserreg(request):
    return render(request, 'dash/register.html')

def registeruser(request):
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    user = User.objects.create_user(username,email,password)
    try:
        user.save()
    except OSError as e:
        print(e)
    return HttpResponseRedirect(reverse('dash:showlogin'))

def showlogin(request):
    return render(request, 'dash/login.html',{})

def loginuser(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request,username=username,password=password)
    if user is not None:
        login(request,user)
        return HttpResponseRedirect(reverse('dash:dashboard'))
    else:
        print("Invalid User")
        return render(request, 'dash/login.html',{"error":"User does not Exist"})

@login_required
def logoutuser(request):
    logout(request)
    return HttpResponseRedirect(reverse('dash:dashboard'))

@login_required
def showuserlist(request):
    return render(request, 'dash/userlist.html',{'userlist':User.objects.all()})

import base64
import io
from django.core import serializers
@login_required
def showticket(request,ticket_id):
    ticket = Ticket.objects.get(pk=ticket_id)
 

    
    qrcode = generateQR("ticket_id:"+str(ticket.ticket_id)+", due_date:"+str(ticket.duedate)+",customer_name:"+str(ticket.customer_name)+",title:"+str(ticket.title)+",desc:"+str(ticket.description))
    return render(request, 'dash/showticket.html',{'ticketdata' : ticket, 'qrcode':qrcode})

@login_required
def completeticket(request,ticket_id):
    ticket = Ticket.objects.get(pk=ticket_id)
    ticket.completed = True
    ticket.save()
    return HttpResponseRedirect(reverse('dash:dashboard'))

def generateQR(datadict):
    upistring = datadict
    
    print(upistring)
    
    image = qrcode.make(upistring)
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    buffer.seek(0)

    data_uri = base64.b64encode(buffer.read()).decode('ascii')
    return data_uri
    

from rest_framework.views import APIView
from django.views.generic import View
from rest_framework.response import Response
class getChartData(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, format = None):
        monthdata = Ticket.objects.annotate(month=TruncMonth('datetime_created')).values('month').annotate(c=Count('ticket_id')).values('month', 'c')
        labellist = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        datalist = {}
        for x in monthdata:
            monthname = datetime.fromisoformat(str(x['month'])).strftime('%b')
            monthcount = int(x['c'])
            datalist[monthname] = monthcount
        finaldata = []
        for y in labellist:
            if y in datalist.keys():
                finaldata.append(datalist[y])
            else:
                finaldata.append(0)

        chartLabel = "Monthly Ticket Statistics"
        data = {
            "labels":labellist,
            "chartLabel":chartLabel,
            "chartdata":finaldata,
        }
        return Response(data)

import random
class getData(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, format = None):
        data = {
            'Name' : "Hriday",
            'Job' : "Developer"

        }
        return Response(data)

from .models import tokens
from rest_framework.decorators import api_view
@api_view(['POST'])
def authAPI(request):
    if request.method == 'POST':
        username = request.query_params.get('username')
        print("YO")
        print(username)
        t = tokens(token_owner=username)
        t.save()
        x = tokens.objects.filter(token_owner=str(username))
        data = {
            'tokenid' : x[0].tokenid,
            'tokenowner': x[0].token_owner
        }
        return Response(data)

@api_view(['POST'])
def senddataontokenauth(request):
    if request.method == 'POST':
        tokenid = request.query_params.get('tokenid')
        tokenowner = request.query_params.get('tokenowner')
        if tokens.objects.filter(token_owner=tokenowner,tokenid = tokenid):
            data = {
                'data' : 'ok'
            }
            return Response(data)
        else:
            data = {
                'data' : 'error : Token Invalid'
            }
            return Response(data)