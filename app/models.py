# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from django.db import models

"""
class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Events(models.Model):
    sender_id = models.CharField(max_length=255)
    type_name = models.CharField(max_length=255)
    timestamp = models.FloatField(blank=True, null=True)
    intent_name = models.CharField(max_length=255, blank=True, null=True)
    action_name = models.CharField(max_length=255, blank=True, null=True)
    data = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'events'


class Text(models.Model):
    nom = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'text'


class Trackers(models.Model):
    sender_id = models.CharField(primary_key=True, max_length=255)  # The composite primary key (sender_id, event_time) found, that is not supported. The first column is selected.
    event_time = models.DateTimeField()
    intent = models.CharField(max_length=255, blank=True, null=True)
    entities = models.TextField(blank=True, null=True)
    slots = models.TextField(blank=True, null=True)
    latest_action = models.CharField(max_length=255, blank=True, null=True)
    latest_message_id = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'trackers'
        unique_together = (('sender_id', 'event_time'),)
"""
class Incidents(models.Model):
    STATUS_CHOICES = [
        ('en attente', 'En attente'),
        ('en cours', 'En cours'),
        ('terminé', 'Terminé'),
    ]

    id = models.AutoField(primary_key=True)
    client = models.ForeignKey('Clients', on_delete=models.CASCADE, blank=True, null=True)
    incident_number = models.CharField(unique=True, blank=True, null=True, max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(blank=True, null=True, max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='en_attente',)
    assigned_agent = models.CharField(blank=True, null=True, max_length=100)
    created_at = models.DateTimeField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

   
    class Meta:
    #    managed = False
        db_table = 'incidents'
    
    def __str__(self):
        return self.incident_number
        


class Clients(models.Model):
    client_id = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, blank=True, null=True, max_length=255)
    phone_number = models.CharField(unique=True, blank=True, null=True, max_length=9)
    # Ajoutez d'autres champs ici si n�cessaire

    class Meta:
        db_table = 'clients'
        # Si vous d�cidez de laisser Django g�rer la table, enlevez la ligne suivante
        # managed = False

    def __str__(self):
        return self.username

