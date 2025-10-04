from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Company(models.Model):
    """Represents a company."""
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    default_currency = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    """Custom user model extending Django's default user."""
    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('Manager', 'Manager'),
        ('Employee', 'Employee'),
    )
    # The default 'username' field is used for email to ensure uniqueness.
    # 'first_name' can be used for the user's name.
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='team_members')

    # We don't need password_hash; Django handles passwords securely.
    # We use 'date_joined' for created_at.

    def __str__(self):
        return self.username

class AuditLog(models.Model):
    """Logs actions performed by users on different entities."""
    ENTITY_CHOICES = (
        ('Expense', 'Expense'),
        ('User', 'User'),
        ('Rule', 'Rule'),
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    
    # Generic relationship to point to Expense, User, or Rule models
    entity_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    entity_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('entity_type', 'entity_id')

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} performed {self.action} on {self.content_object}'
