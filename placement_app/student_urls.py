from django.urls import path
from placement_app.student_views import *

urlpatterns = [
    path('',StudentIndexView.as_view()),
    path('view_profile',StudentProfileView.as_view()),
    path('edit_profile',UpdateProfileView.as_view()),
    path('placement_view',PlacementsView.as_view()),
    path('for_me',ForMEView.as_view()),
    path('apply_placement',ApplyPlacementView.as_view()),
    path('applied_placements',AppliedPlacementsView.as_view()),
    path('update_status',UpdatePlacementStatus.as_view()),
]
def urls():
    return urlpatterns, 'student', 'student'