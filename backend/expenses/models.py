from django.db import models
from users.models import User, Company

class Expense(models.Model):
    """Represents an employee's expense claim."""
    STATUS_CHOICES = (
        ('Draft', 'Draft'),
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    expense_date = models.DateField()
    currency = models.CharField(max_length=10)
    amount_original = models.DecimalField(max_digits=12, decimal_places=2)
    amount_converted = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Draft')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Expense {self.id} by {self.employee.username}'

class ExpenseAttachment(models.Model):
    """Stores attachments for an expense, like receipts."""
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name='attachments')
    file_url = models.FileField(upload_to='expense_attachments/')
    ocr_text = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Attachment for Expense {self.expense.id}'

class CurrencyRate(models.Model):
    """Caches currency exchange rates."""
    base_currency = models.CharField(max_length=10)
    target_currency = models.CharField(max_length=10)
    exchange_rate = models.DecimalField(max_digits=12, decimal_places=6)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.base_currency} to {self.target_currency}: {self.exchange_rate}'
