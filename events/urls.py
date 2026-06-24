from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name = 'event-list'),
    path('upcoming/', views.upcoming_events, name = 'event-upcoming'),
    path('search/', views.search_events, name = 'event-search'), 
    path('create/', views.create_event, name = 'event-create'),
    path('my-events/', views.my_events, name = 'event-my-events'),
    path('dashboard/', views.dashboard, name = 'event-dashboard'),
    path('<int:pk>', views.event_detail, name = 'event-detail'),
    path('category/<int:pk>/', views.events_category, name = 'event-category'),
    path('<int:pk>/edit/', views.edit_event, name = 'event-edit' ),
    path('<int:pk>/delete/', views.delete_event, name = 'event-delete'),
    path('<int:pk>/cancel/', views.cancel_event, name = 'event-cancel'),
    path('<int:pk>/join/', views.join_event, name = 'event-join'),
    path('<int:pk>/leave/', views.leave_event, name = 'event-leave'),
    path('<int:pk>/participants/', views.event_participants, name = 'event-participants'), 
]