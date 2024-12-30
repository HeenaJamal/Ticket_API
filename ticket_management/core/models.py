from django.db import models

# Admin, Support, Developer Models
class Admin(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15, unique=True)
    otp = models.CharField(max_length=6)

class Support(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15, unique=True)

class Developer(models.Model):
    FRONTEND = 'frontend'
    BACKEND = 'backend'
    ROLE_CHOICES = [
        (FRONTEND, 'Frontend'),
        (BACKEND, 'Backend'),
    ]
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

# Ticket Model
class Ticket(models.Model):
    title = models.CharField(max_length=255)
    ticket_code = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    status = models.CharField(max_length=50, default='open')  # 'open', 'closed', etc.
    #images = models.ImageField(upload_to='tickets/', blank=True, null=True)
    date_time = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Support, on_delete=models.CASCADE, related_name='tickets')


class TicketImage(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='ticket_images/')  # Store images in 'ticket_images' folder

    def __str__(self):
        return f"Image for ticket {self.ticket.ticket_code}"