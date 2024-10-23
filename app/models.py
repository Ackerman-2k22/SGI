# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from django.db import models

class Incidents(models.Model):
    STATUS_CHOICES = [
        ('en attente', 'En attente'),
        ('en cours', 'En cours'),
        ('terminé', 'Terminé'),
    ]

    id = models.AutoField(primary_key=True)
    client = models.ForeignKey('Clients', on_delete=models.CASCADE, blank=True, null=True, related_name='incidents')
    incident_number = models.CharField(unique=True, blank=True, null=True, max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(blank=True, null=True, max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='en_attente',)
    assigned_agent = models.CharField(blank=True, null=True, max_length=100)
    created_at = models.DateTimeField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    resolved_at = models.DateTimeField(blank=True, null=True)

   
    class Meta:
        db_table = 'incidents'
    
    def __str__(self):
        return self.incident_number
        


class Clients(models.Model):
    client_id = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, blank=True, null=True, max_length=255)
    phone_number = models.CharField(unique=True, blank=True, null=True, max_length=9)

    class Meta:
        db_table = 'clients'

    def __str__(self):
        return self.username
