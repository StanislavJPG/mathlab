from django.urls import path

from server.apps.complaints.logic.complaint_management import ComplaintCreateView

app_name = 'complaints'

urlpatterns = [
    path('<slug:object_label>/<uuid:object_uuid>/create/', ComplaintCreateView.as_view(), name='complaint-create'),
]
