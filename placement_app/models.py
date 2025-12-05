from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

# Create your models here.
class UserType(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    type = models.CharField(max_length=50,null=True)

class Students(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    address = models.CharField(max_length=50,null=True)
    phone = models.CharField(max_length=50,null=True)
    dob = models.DateField(null=True)
    gender = models.CharField(max_length=50,null=True)
    roll_no = models.CharField(max_length=50,null=True)
    program = models.CharField(max_length=50,null=True)
    entroll_year = models.CharField(max_length=50,null=True)
    department = models.CharField(max_length=50,null=True)
    backlogs = models.CharField(max_length=50,null=True)
    cgpa = models.CharField(max_length=50,null=True)
    p_email = models.CharField(max_length=50,null=True)
    passout_year = models.CharField(max_length=50,null=True)
    image = models.ImageField(max_length=50,null=True)


class Placements(models.Model):
    p_id = models.CharField(max_length=50, null=True)
    company_name = models.CharField(max_length=50, null=True)
    c_date = models.DateField(null=True, auto_now_add=True)
    last_date = models.DateField(null=True)
    cgpa = models.FloatField(null=True)  # Changed to Float for comparison
    arrears = models.IntegerField(null=True)  # Changed to Integer for comparison
    passout_year = models.IntegerField(null=True)  # Changed to Integer for comparison
    description = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=50, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save placement details first
        self.notify_eligible_students()  # Send email notifications

    def notify_eligible_students(self):
        from placement_app.models import Students  # Import Students model

        # Fetch students eligible for this placement
        eligible_students = Students.objects.filter(
            cgpa__gte=self.cgpa, passout_year__lte=self.passout_year, backlogs__lte=self.arrears
        )

        # Send email to each eligible student
        for student in eligible_students:
            subject = f"New Placement Opportunity at {self.company_name}"
            message = f"""
            Dear {student.user.first_name},

            A new placement opportunity is available that matches your profile:

            📌 **Company:** {self.company_name}
            📆 **Last Date to Apply:** {self.last_date}
            🎓 **Required CGPA:** {self.cgpa}
            📌 **Allowed Arrears:** {self.arrears}
            📅 **Passout Year Required:** {self.passout_year}
            📝 **Description:** {self.description}

            Please log in to the portal and apply before the deadline.

            Best regards,
            Placement Team
            """
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,  # Sender email (Configured in Django settings)
                [student.user.email],  # Recipient (Student Email)
                fail_silently=False,
            )

class ApplyPlacement(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE,null=True)
    placement = models.ForeignKey(Placements, on_delete=models.CASCADE,null=True)
    resume = models.FileField(null=True)
    certificate = models.FileField(null=True)
    internship = models.CharField(max_length=200,null=True)
    projects = models.CharField(max_length=200,null=True)
    achivements = models.CharField(max_length=200,null=True)
    technical_skills = models.CharField(max_length=200,null=True)
    soft_skills = models.CharField(max_length=200,null=True)
    status = models.CharField(max_length=50,null=True)
    offer_letter = models.FileField(null=True)