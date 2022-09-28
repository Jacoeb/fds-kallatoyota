from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .models import *

def department_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='user_dept')
        instance.groups.add(group)
        Department.objects.create(
            user=instance,
            name=instance.username,
        )
        
post_save.connect(department_profile, sender=User)