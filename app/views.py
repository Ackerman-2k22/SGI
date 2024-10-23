from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from .models import Incidents, Clients
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.db.models.functions import TruncWeek, TruncMonth
from django.db.models.functions import TruncMonth
from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Count
from django.shortcuts import render
from .models import Incidents
from django.db.models import Q
import json
import datetime
from django.utils import timezone
from django.core import serializers
# Create your views here.


def filter_incidents(request):
    category = request.GET.get('category', '')
    status = request.GET.get('status', '')

    query = Q()
    if category:
        query &= Q(category=category)
    if status:
        query &= Q(status=status)

    incidents = Incidents.objects.filter(query)

    data = list(incidents.values('id', 'client__username', 'description', 'category', 'created_at', 'status', 'assigned_agent', 'comment', 'resolved_at'))

    for item in data:
        item['created_at'] = item['created_at'].strftime('%Y-%m-%d %H:%M:%S')
#        item['resolved_at'] = item['resolved_at'].strftime('%Y-%m-%d %H:%M:%S')  # Ajustez le format si nécessaire

    return JsonResponse(data, safe=False)


def search_incidents(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText', '')
        incidents = Incidents.objects.filter(
            Q(id__istartswith=search_str) |
            Q(client__username__icontains=search_str) |
            Q(description__icontains=search_str) |
            Q(created_at__istartswith=search_str) |
            Q(assigned_agent__istartswith=search_str) |
            Q(category__icontains=search_str) |
            Q(comment__icontains=search_str) |
            Q(resolved_at__istartswith=search_str)
            
        ).distinct()

        data = list(incidents.values('id', 'client__username', 'description', 'category', 'created_at', 'status', 'assigned_agent', 'comment', 'resolved_at'))

        for item in data:
            item['created_at'] = item['created_at'].strftime('%Y-%m-%d %H:%M:%S')

        return JsonResponse(data, safe=False)

def search_clients(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText', '')
        clients = Clients.objects.filter(
            Q(client_id__istartswith=search_str) |
            Q(username__icontains=search_str) |
            Q(phone_number__icontains=search_str)
        ).distinct()

        data = list(clients.values('client_id', 'username', 'phone_number'))

        return JsonResponse(data, safe=False)

@login_required(login_url = '/authentication/login')
def index(request):
    app = Incidents.objects.all().order_by('-id') 
    categories = Incidents.objects.values_list('category', flat=True).distinct()
    statuses = Incidents.objects.values_list('status', flat=True).distinct()
    paginator = Paginator(app,3)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)

    context = {
        'app':app,
        'page_obj':page_obj,
        'categories': categories,
        'statuses': statuses,
    }
    return render(request, 'app/index.html', context)

def add_incidents(request):
    return render(request, 'app/add_incidents.html')

@login_required
def edit_incidents(request, id):
    incident = get_object_or_404(Incidents, pk=id)
    if request.method == "POST":
        incident.comment = request.POST['comment']
        incident.status = request.POST['status']

        user = request.user

        if incident.status == "en attente":
            incident.assigned_agent = "non attribué"
            incident.resolved_at = None 
        elif incident.status == "en cours":
            incident.assigned_agent = f"{user.first_name} {user.last_name}"
            incident.resolved_at = None 
        elif incident.status == "terminé":
            incident.assigned_agent = f"{user.first_name} {user.last_name}"
            if not incident.resolved_at:
                incident.resolved_at = timezone.now()

        incident.save()
        messages.success(request, "L'incident a été mis à jour avec succès.")
        return redirect('app')
    else:
        return render(request, 'app/edit_incidents.html', {'incident': incident})
    

def details(request, client_id):
    client = get_object_or_404(Clients, pk=client_id)
    messages.success(request, "Client affiché avec succès.")
    return render(request, 'app/details.html', {'client': client})
    
def clients(request):
    clients_list = Clients.objects.all()
    return render(request, 'app/clients.html', {'clients': clients_list})



def list_clients(request):
    clients = Clients.objects.annotate(number_of_incidents=Count('incidents'))
    for client in clients:
        print(client.username, client.number_of_incidents)
    return render(request, 'app/clients.html', {'clients': clients})



def incident_category_summary(request):
    todays_date = timezone.now().date()
    six_months_ago = todays_date - datetime.timedelta(days=30*6)
    incidents = Incidents.objects.filter(
        created_at__date__gte=six_months_ago, 
        created_at__date__lte=todays_date
    )

    # Statistiques par catégorie
    category_summary = incidents.values('category').annotate(total=Count('id')).order_by('-total')
    category_data = {entry['category']: entry['total'] for entry in category_summary if entry['category']}

    # Statistiques par statut
    status_summary = incidents.values('status').annotate(total=Count('id')).order_by('-total')
    status_data = {entry['status']: entry['total'] for entry in status_summary if entry['status']}

    # Statistiques par agent assigné
    agent_summary = incidents.values('assigned_agent').annotate(total=Count('id')).order_by('-total')
    agent_data = {entry['assigned_agent']: entry['total'] for entry in agent_summary if entry['assigned_agent']}

    # Taux d'incidents créés par mois
    incidents_per_month = incidents.annotate(month=TruncMonth('created_at')).values('month').annotate(total=Count('id')).order_by('month')
    month_data = {entry['month'].strftime("%Y-%m"): entry['total'] for entry in incidents_per_month if entry['month']}

    final_data = {
        'incident_category_data': category_data,
        'incident_status_data': status_data,
        'incident_agent_data': agent_data,
        'incident_month_data': month_data,
    }

    return JsonResponse(final_data, safe=False)

def stats_view(request):
    return render(request, 'app/stats.html')

def dashboard_view(request):
    return render(request, 'app/dashboard.html')

def dashboard_data_summary(request):
    todays_date = timezone.now().date()
    six_months_ago = todays_date - datetime.timedelta(days=30*6)
    incidents = Incidents.objects.filter(
        created_at__date__gte=six_months_ago, 
        created_at__date__lte=todays_date
    )

    # Incidents par semaine (les 6 derniers mois)
    incidents_per_week = incidents.annotate(week=TruncWeek('created_at')).values('week').annotate(total=Count('id')).order_by('week')
    week_labels = [entry['week'].strftime("%Y-%m-%d") for entry in incidents_per_week]
    week_data = [entry['total'] for entry in incidents_per_week]

    # Incidents par mois (les 6 derniers mois)
    incidents_per_month = incidents.annotate(month=TruncMonth('created_at')).values('month').annotate(total=Count('id')).order_by('month')
    month_labels = [entry['month'].strftime("%Y-%m") for entry in incidents_per_month]
    month_data = [entry['total'] for entry in incidents_per_month]

    dashboard_data = {
        'incident_week_data': {'labels': week_labels, 'data': week_data},
        'incident_month_data': {'labels': month_labels, 'data': month_data},
    }

    return JsonResponse(dashboard_data, safe=False)