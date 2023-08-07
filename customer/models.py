from django.db import models
# from django.contrib.auth.models import User
from django.conf import settings
User = settings.AUTH_USER_MODEL

class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class TicketStatus(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Agent(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None, null=True, blank=True)

    def __str__(self):
        return self.user.username
class Ticket(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    status = models.ForeignKey(TicketStatus, on_delete=models.PROTECT)
    assigned_agent = models.ForeignKey(
        'Agent', on_delete=models.SET_NULL, null=True)
    response_time = models.DurationField(null=True, blank=True)
    resolution_time = models.DurationField(null=True, blank=True)
    customer_satisfaction_score = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # agent_assigned = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, blank=True)

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category)
    tags = models.ManyToManyField(Tag)
    
    # Add more fields as needed (e.g., categories, tags)

    def __str__(self):
        return self.title

class Rating(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='ratings')
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='ratings')
    score = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



