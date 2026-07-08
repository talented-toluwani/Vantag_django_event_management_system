from django.utils import timezone

from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import Q

from .models import Event, Registration, Category
from .forms import EventForm
from .decorators import admin_required
from accounts.models import CustomUser


@login_required
def event_list(request):
    #filters the events objects to get a list of all the events
    events = Event.objects.filter(is_cancelled = False).order_by('date')
    context = {'events': events}
    return render(request, 'events/event_list.html', context)

@login_required
def event_detail(request, pk):
    #fetches a single event with its unique identief to edit its details
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
@admin_required
def create_event(request):
    if request.method == "GET":
        form = EventForm()
        context = {
            'form':form,
        }
        return render(request, 'events/event_detail.html', context)
    
    if request.method == "POST":
        form = EventForm(request.POST)
        context = {
            'form':form,
        }
        
        if form.is_valid():
            instance = form.save(commit=False)
            instance.created_by = request.user
            instance.save()

            messages.success(request, "Event Successfully created")
            return redirect('event-detail', pk= instance.pk)
        
        return render(request, 'events/event_create.html', context)
    
@login_required
@admin_required
def edit_event(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if request.method == "GET":
        form = EventForm(instance=event)
        context = {
        'form': form,
    }
        return render (request, 'events/edit_event.html', context)
        
    if request.method == "POST":
        form = EventForm(request.POST,instance=event)
        context = {
            'form': form,
        }

        if form.is_valid():
            instance = form.save()

            messages.success(request, "Event detail has been editied")
            return redirect( 'event-detail', pk =  instance.pk)
        
        return render(request, 'events/edit_event.html', context)
    
@login_required
@admin_required
def delete_event(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if request.method == "GET":#fecthes the event and renders confirmation page
        context = {
            'event': event,
        }
        return render(request, 'events/delete_event.html', context)

    if request.method == "POST":#dletes event
        event.delete() 
        messages.success(request, "Event Successfully deleted")
        return redirect('event-list')
            
@login_required
@admin_required
def cancel_event(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if request.method == "GET":
        context = {
            'event': event
        }
        return render(request, 'events/cancel_event.html', context)
    
    if request.method == "POST":
        event.is_cancelled= True
        event.save()
        messages.success(request, "Event has been successfully cancelled")
        return redirect('event-detail')

        
@login_required
@require_POST 
def join_event(request, pk):
    event = get_object_or_404(Event, pk=pk)

    is_registered = Registration.objects.filter(
        event = event,
        participant = request.user,
        status = 'active',
    ).exists() #checks for duplicate registration

    if is_registered:
        messages.success(request, "You are already registered for this event.")
        return redirect('event-detail', pk=event.pk)
    
    active_registrations = Registration.objects.filter(
        event = event,
        status = 'active',
    ).count() #checks capcity of the event

    if active_registrations >= event.capacity:
        messages.error(request, "The event has reached maximum capacity")
        return redirect('event-detail', pk=event.pk)
    
    Registration.objects.create(
        event = event,
        participant = request.user,
        status = 'active',
    )

    messages.success(request, "You have successfully joined the event")
    return redirect('event-detail', pk=event.pk)

@login_required
@require_POST
def leave_event(request, pk):
    event = get_object_or_404(Event, pk=pk)

    is_registered = Registration.objects.filter(
        event = event,
        participant = request.user,
        status = 'active'
    ).exists()

    if not is_registered:
        messages.error(request, "You are not registered for this event.")
        return redirect('event-detail', pk=event.pk)


    is_cancelled = Registration.objects.filter(
            event = event,
            participant = request.user,
            status = 'active'
        )
    
    is_cancelled.delete()
    messages.success(request, "You have left the event")
    return redirect('event-detail', pk=event.pk)
    
@login_required
def my_events(request):
    events = Event.objects.filter(
        registration__participant = request.user, 
        registration__status = 'active',
        is_cancelled = False
        )
    
    context = {
        'events': events,
    }
    return render(request, 'events/my_events.html',context)

@login_required
def upcoming_events(request):
    events = Event.objects.filter(
        is_cancelled = False,
        date__gt= timezone.now()
        )
    context = {
        'events': events,
    }

    return render(request, 'events/upcoming_events.html', context)

@login_required
def search_events(request):
    query = request.GET.get('q', '')

    if query:
        events = Event.objects.filter(
             Q(title__icontains=query) | Q(location__icontains=query),
            is_cancelled=False
        )
    
    else:
        events + Event.objects.none()

    context = {
        'events':events,
        'query':query,
    }

    return render(request, 'events/search_events.html', context)

@login_required
@admin_required
def event_participants(request, pk):
    event = get_object_or_404(Event, pk=pk )
    registrations = Registration.objects.filter(
        event = event
    )

    context = {
        'event':event,
        'registrations':registrations,
    }

    return render(request, 'events/event_participants.html', context)

@login_required
@admin_required
def dashboard(request):
     
    total_events =   Event.objects.all().count(),
    active_events = Event.objects.filter(is_cancelled = False).count(),
    cancelled_events =  Event.objects.filter(is_cancelled = True).count(),
    total_registrations =  Registration.objects.all().count(),
    active_registrations = Registration.objects.filter(status = 'active').count(),
    total_user =  CustomUser.objects.count(),
    recent_event=  Event.objects.order_by('-created_at')[:5],
    
    context = {
        'total_events': total_events,
        'active_events': active_events,
        'cancelled_events': cancelled_events,
        'total_registrations': total_registrations,
        'active_registrations':active_registrations,
        'total_user': total_user,
        'recent_event': recent_event,
    }

    return render(request, 'events/dashboard.html', context)
  
@login_required
def events_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    event = Event.objects.filter(
        is_cancelled = False,
        category = category,
        ).order_by('date')

    context = {
        'category': category,
        'event': event,
    }

    return render(request, 'events/events_category.html', context)
