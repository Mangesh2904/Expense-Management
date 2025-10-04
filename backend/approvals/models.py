from django.db import models
from users.models import Company, User
from expenses.models import Expense

class ApprovalRule(models.Model):
    """Defines rules for expense approvals within a company."""
    TYPE_CHOICES = (
        ('Percentage', 'Percentage'),
        ('Specific', 'Specific'),
        ('Hybrid', 'Hybrid'),
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    percentage_required = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    specific_approver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} ({self.company.name})'

class ExpenseApproval(models.Model):
    """Tracks the approval status for a specific expense by an approver."""
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name='approvals')
    approver = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    comments = models.TextField(null=True, blank=True)
    sequence_order = models.IntegerField(null=True, blank=True)
    acted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Approval for {self.expense_id} by {self.approver.username}'
