from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [

    path('edit-incidents/<int:id>', views.edit_incidents, name='edit-incidents'),
    path('add-incidents', views.add_incidents, name='add-incidents'),
    path('clients/', views.clients, name='clients'),
    path('clients/', views.list_clients, name='list-clients'),
    path('incident_category_summary', views.incident_category_summary,
         name="incident_category_summary"),
    path('stats', views.stats_view, name="stats"),
    path('search-incidents', csrf_exempt(views.search_incidents), name="search_incidents"),
    path('filter-incidents', csrf_exempt(views.filter_incidents), name="filter_incidents"),
    path('search-clients', csrf_exempt(views.search_clients), name="search_clients"),
    path('details/<int:client_id>/', views.details, name='details'),
    path('dashboard', views.dashboard_view, name="dashboard"),
    path('dashboard_data_summary/', views.dashboard_data_summary, name='dashboard_data_summary'),
]

