from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager, PermissionsMixin

from datetime import datetime

from dash.auth_utils.permissions_dict import create_perms_list


class SkyUserManager(BaseUserManager):
    def create_user(self, user):
        new_user = self.model(
            id = user['id' ],
            email=self.normalize_email(user['email']),
            first_name=user['first_name'],
            last_name=user['last_name'],
            preferred_name=user['preferred_name'],
            roles=user['roles']
        )
        new_user.save(using=self._db)
        return new_user

    def create_superuser(self, user):
        new_user = self.model(
            id = user['id' ],
            email=self.normalize_email(user['email']),
            first_name=user['fist_name'],
            last_name=user['last_name'],
            preferred_name=user['preferred_name']
        )
        new_user.save(using=self._db)
        return new_user


class SkyUser(AbstractBaseUser, PermissionsMixin):
    objects=SkyUserManager()

    id = models.BigIntegerField(primary_key=True, auto_created=False, db_index=True)
    email = models.EmailField(unique=True, max_length=255, db_index=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    preferred_name = models.CharField(max_length=100)
    student_id = models.IntegerField(blank=True, null=True, db_index=True)
    roles = models.JSONField(null=True)

    class Meta:
        permissions = create_perms_list()

    def __str__(self):
        return f'{self.preferred_name} {self.last_name}'
    
    USERNAME_FIELD = 'email'

    @property
    def is_staff(self):
        """ Is the user a member of staff?"""
        return self.is_admin   


class PlannedAbsence(models.Model):
    parent = models.ForeignKey("SkyUser", on_delete=models.PROTECT, related_name="planned_absences", db_index=True)
    child = models.IntegerField()
    from_date = models.DateTimeField(blank=False)
    to_date = models.DateTimeField(blank=False)
    comment = models.TextField()
    approved = models.BooleanField(default=False)


class Attendance(models.Model):
    student_id = models.IntegerField()
    begin_date = models.DateTimeField(default=datetime.now)
    end_date = models.DateTimeField(default=datetime.now)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    exuse_type = models.CharField(max_length=50, default='Tardy Unexcused')
    comment = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=50)


class NurseApproval(models.Model):
    absenence_code = models.ForeignKey("PlannedAbsence", on_delete=models.PROTECT, related_name='nurse_approval', db_index=True)
    type = models.CharField(max_length=50, blank=False)
    approval = models.BooleanField(default=False)


class HeadApproval(models.Model):
    SCHOOL_DIVISIONS = [
        ("US", 'Upper School'),
        ('MS', 'Middle School')
    ]
    absenence_code = models.ForeignKey("PlannedAbsence", on_delete=models.PROTECT, related_name='head_approval', db_index=True)
    school_division = models.CharField(max_length=2, choices=SCHOOL_DIVISIONS)
    approval = models.BooleanField(default=False)