from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Event, Registration
from .forms import EventForm

@login_required
def event_list(request):
    events = Event.objects.filter(is_cancelled = False).order_by('date')
    context = {'events': events}
    return render(request, 'events/event_list.html', context)

@login_required
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)

    is_registered = Registration.objects.filter(
        event = event,
        participant = request.user,
        status = 'active'
    ).exists()

    context = {
        'events': event,
        'is_registered': is_registered,
        }
    return render(request, 'events/event_detail.html', context)

@login_required
def event_create(request):

    is_staff = 

    if request.method == "GET":
        form = EventForm(request.GET)