from django.contrib import admin
from .models import Incidents
from .models import Clients
# Register your models here.


class AdminIncidents(admin.ModelAdmin):

    readonly_fields = ('assigned_agent', 'client_username', 'created_at','description','incident_number',)

    list_display = ('id', 'client_username', 'description', 'category', 'created_at', 'status', 'assigned_agent', 'comment')
    list_filter = ('category', 'status', 'created_at', 'assigned_agent', 'client_id')
    search_fields = ('id', 'client_username', 'description', 'category', 'created_at', 'status', 'assigned_agent', 'comment')
    list_per_page = 10

    def save_model(self, request, obj, form, change):
        if obj.status in ['en cours', 'terminé']:
            obj.assigned_agent = f"{request.user.first_name} {request.user.last_name}"
        elif obj.status == 'en attente':
            obj.assigned_agent = "non attribué"
        super().save_model(request, obj, form, change)

    def client_username(self, obj):
        return obj.client.username

class AdminClients(admin.ModelAdmin):

    readonly_fields = ('username', 'phone_number')
    list_display = ('client_id', 'username', 'phone_number')
    search_fields = ('client_id', 'username', 'phone_number')

admin.site.register(Incidents, AdminIncidents) 

admin.site.register(Clients, AdminClients)

