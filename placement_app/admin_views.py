from django.views.generic import TemplateView,View
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage

from placement_app.models import *

# Create your views here.

class AdminIndexView(TemplateView):
    template_name='admin/index.html'  

class StudentVerify(TemplateView):
    template_name = 'admin/student_verify.html'
    def get_context_data(self, **kwargs):
        context = super(StudentVerify,self).get_context_data(**kwargs)
        std = Students.objects.filter(user__last_name='0',user__is_staff='0',user__is_active='1')
        context['std'] = std
        return context
    
class Approve(View):
    def dispatch(self, request, *args, **kwargs):
        id = request.GET['id']
        user = User.objects.get(pk=id)
        user.last_name='1'
        user.save()
        return render(request,'admin/index.html',{'message':" Account Approved"})

class Reject(View):
    def dispatch(self, request, *args, **kwargs):
        id = request.GET['id']
        user = User.objects.get(pk=id)
        user.last_name='1'
        user.is_active='0'
        user.save()
        return render(request,'admin/index.html',{'message':"Account Removed"})

class StudentView(TemplateView):
    template_name = 'admin/student_view.html'
    def get_context_data(self, **kwargs):
        context = super(StudentView,self).get_context_data(**kwargs)
        std = Students.objects.filter(user__last_name='1',user__is_staff='0',user__is_active='1')
        context['std'] = std
        return context
    
class AddPlacementView(TemplateView):
    template_name = 'admin/add_placement.html'
    def post(self, request, *args, **kwargs):
        company_name = request.POST['company_name']
        p_id = request.POST['p_id']
        l_date = request.POST['l_date']
        cgpa = request.POST['cgpa']
        passout_year = request.POST['passout_year']
        arrears = request.POST['arrears']
        description = request.POST['description']

        plc= Placements(p_id=p_id,company_name=company_name,last_date=l_date,cgpa=cgpa,passout_year=passout_year,arrears=arrears,description=description,status='added')
        plc.save()
        return render(request,'admin/index.html',{'message':"Placement Added"})
    
class PlacementsView(TemplateView):
    template_name = 'admin/placements_view.html'
    def get_context_data(self, **kwargs):
        context = super(PlacementsView,self).get_context_data(**kwargs)
        plc = Placements.objects.all()
        context['plc'] = plc
        return context
    
class StudentsResponsesView(TemplateView):
    template_name = 'admin/students_responses.html'
    def get_context_data(self, **kwargs):
        context = super(StudentsResponsesView,self).get_context_data(**kwargs)
        plc = ApplyPlacement.objects.all()
        context['plc'] = plc
        return context
    
class ApprovePlacement(View):
    def dispatch(self, request, *args, **kwargs):
        id = request.GET['id']
        plc = ApplyPlacement.objects.get(id=id)
        plc.status = 'approved'
        plc.save()
        return render(request,'admin/index.html',{'message':"Placement Approved"})
    
class RejectPlacement(View):
    def dispatch(self, request, *args, **kwargs):
        id = request.GET['id']
        plc = ApplyPlacement.objects.get(id=id)
        plc.status = 'rejected'
        plc.save()
        return render(request,'admin/index.html',{'message':"Placement Rejected"})
    
class NotSelected(View):
    def dispatch(self, request, *args, **kwargs):
        id = request.GET['id']
        plc = ApplyPlacement.objects.get(id=id)
        plc.status = 'not selected'
        plc.save()
        return render(request,'admin/index.html',{'message':"Placement Not Selected"})
    
class UploadOfferLetter(TemplateView):
    template_name = 'admin/upload_offer.html'
    def post(self,request,*args,**kwargs):
        id = self.request.GET['id']
        usr = ApplyPlacement.objects.get(pk=id)
        usr.status = 'offer letter uploaded'
        usr.offer_letter = request.FILES['offer_letter']
        usr.save()
        return render(request,'admin/index.html',{'message':"Updated"})