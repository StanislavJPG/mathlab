from server.apps.complaints.models import Complaint


def count_active_complaints():
    complaints = Complaint.objects.filter_by_not_processed()
    return complaints.count()
