from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Event, Registration
from .forms import EventForm
from .decorators import admin_required
from django.contrib import messages
from django.views.decorators.http import require_POST

@login_required
def event_list(request):
    #filters the events objects to get a list of all the events
    events = Event.objects.filter(is_cancelled = False).order_by('date')
    context = {'events': events}
    return render(request, 'events/event_list.html', context)

@login_required
def event_detail(request, pk):
    #fetches event with its unique identief to edit its details
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
def event_create(request):
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
def event_cancel(request, pk):
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

@require_POST         
@login_required
def join_event(request, pk):
    event = get_object_or_404(Event, pk=pk)

    is_regitered = Registration.objects.filter(
        event = event,
        participant = request.user,
        status = 'active',
    ).exists()

    context = {
        'event': event,
        'is_registered': is_regitered ,
    }

    return render(request, 'events/event_list', context)

    

 
        
