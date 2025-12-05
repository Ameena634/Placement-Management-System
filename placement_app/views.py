from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import login, authenticate
from placement_app.models import *

# Create your views here.

class indexView(TemplateView):
    template_name='index.html'  

class LoginView(TemplateView):
    template_name='login.html'
    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password= request.POST['password']

        user = authenticate(username=username,password=password)
        if user is not None:

            login(request,user)
            if user.last_name == '1':

                if user.is_superuser:
                    return redirect('/admin')
               
                else:
                    return redirect('/student')

            else:


                return render(request,'login.html',{'message':" User Account Not Authenticated"})
        else:

            return render(request,'login.html',{'message':"Invalid Username or Password"})
        
class StudentReg(TemplateView):
    template_name='student_reg.html'

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        password = request.POST['password']
        con_password = request.POST['con_password']
        department = request.POST['department']
        image = request.FILES['image']
        if password != con_password:
            return render(request,'student_reg.html',{'message':'Password and Confirm Password does not match'})
        else:
            user = User.objects.create_user(username=username,password=password,email=email,first_name=first_name,last_name="0")
            user.save()
            std= Students(user=user,department=department,image=image)
            std.save()
            usertype= UserType(user=user,type='student')
            usertype.save()
            return render(request,'student_reg.html',{'message':'User Registered Successfully'})