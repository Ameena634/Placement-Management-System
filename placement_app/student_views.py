from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage

from placement_app.models import *

# Create your views here.

class StudentIndexView(TemplateView):
    template_name='student/index.html'

class StudentProfileView(TemplateView):
    template_name='student/view_profile.html'
    def get_context_data(self, **kwargs):
        context = super(StudentProfileView,self).get_context_data(**kwargs)
        std = Students.objects.filter(user_id=self.request.user.id)
        context['std'] = std
        return context
    
class UpdateProfileView(TemplateView):
    template_name='student/edit_profile.html'
    def get_context_data(self, **kwargs):
        context = super(UpdateProfileView,self).get_context_data(**kwargs)
        std = Students.objects.filter(user_id=self.request.user.id)
        context['std'] = std
        return context
    
    def post(self,request,*args,**kwargs):
        id = self.request.GET['id']
        usr = Students.objects.get(id=id)
        usr.roll_no = request.POST['roll_no']
        usr.department = request.POST['department']
        usr.entroll_year = request.POST['entroll_year']
        usr.address = request.POST['address']
        usr.backlogs = request.POST['backlogs']
        usr.cgpa = request.POST['cgpa']
        usr.phone = request.POST['phone']
        usr.dob = request.POST['dob']
        usr.gender = request.POST['gender']
        usr.p_email = request.POST['p_email']
        usr.program = request.POST['program']
        usr.passout_year = request.POST['passout_year']
        usr.image = request.FILES['image']
        usr.save()
        return render(request,'student/index.html',{'message':"Profile Updated"})
    

class PlacementsView(TemplateView):
    template_name = 'student/placements_view.html'
    def get_context_data(self, **kwargs):
        context = super(PlacementsView,self).get_context_data(**kwargs)
        plc = Placements.objects.all()
        context['plc'] = plc
        return context
    
class ForMEView(TemplateView):
    template_name = 'student/for_me.html'
    def get_context_data(self, **kwargs):
        context = super(ForMEView,self).get_context_data(**kwargs)
        std = Students.objects.get(user_id=self.request.user.id)
        plc = Placements.objects.filter(cgpa__lte=std.cgpa,passout_year__gte=std.passout_year,arrears__gte=std.backlogs)
        context['plc'] = plc
        return context
    
class ApplyPlacementView(TemplateView):
    template_name = 'student/apply_placement.html'
    def post(self,request,*args,**kwargs):
        std = Students.objects.get(user_id=self.request.user.id)
        id = self.request.GET['id']
        usr = ApplyPlacement()
        usr.resume = request.FILES['resume']
        usr.certificate = request.FILES['certificate']
        usr.achivements = request.POST['achivements']
        usr.projects = request.POST['projects']
        usr.internship = request.POST['internship']
        usr.technical_skills = request.POST['technical_skills']
        usr.soft_skills = request.POST['soft_skills']
        usr.placement_id = id
        usr.student_id = std.id
        usr.status = 'added'
        usr.save()
        return render(request,'student/index.html',{'message':"Applied Successfully"})
    
class AppliedPlacementsView(TemplateView):
    template_name = 'student/applied_placements.html'
    def get_context_data(self, **kwargs):
        context = super(AppliedPlacementsView,self).get_context_data(**kwargs)
        std = Students.objects.get(user_id=self.request.user.id)
        plc = ApplyPlacement.objects.filter(student_id=std.id)
        context['plc'] = plc
        return context
    
class UpdatePlacementStatus(TemplateView):
    template_name = 'student/update_status.html'
    def post(self,request,*args,**kwargs):
        id = self.request.GET['id']
        usr = ApplyPlacement.objects.get(pk=id)
        usr.status = request.POST['status']
        usr.save()
        return render(request,'student/index.html',{'message':"Updated"})

    