from django.contrib.auth.decorators import user_passes_test

admin_required =  user_passes_test( lambda u:u.is_staff, login_url='event-list')