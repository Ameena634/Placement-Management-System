from django.urls import path
from placement_app.admin_views import *

urlpatterns = [
    path('',AdminIndexView.as_view()),
    path('student_verify',StudentVerify.as_view()),
    path('approve',Approve.as_view()),
    path('reject',Reject.as_view()),
    path('student_view',StudentView.as_view()),
    path('add_placement',AddPlacementView.as_view()),
    path('placement_view',PlacementsView.as_view()),
    path('student_responses',StudentsResponsesView.as_view()),
    path('approve_placement',ApprovePlacement.as_view()),
    path('reject_placement',RejectPlacement.as_view()),
    path('not_selected',NotSelected.as_view()),
    path('upload_offer',UploadOfferLetter.as_view()),
]
def urls():
    return urlpatterns, 'admin', 'admin'