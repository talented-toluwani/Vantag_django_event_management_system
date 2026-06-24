from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def admin_required()