from rest_framework import serializers
from .models import Admin, Support, Developer, Ticket

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['name', 'email', 'mobile', 'otp']

class SupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Support
        fields = ['id', 'name', 'email', 'mobile']

class DeveloperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Developer
        fields = ['id', 'name', 'email', 'mobile', 'role']

from rest_framework import serializers
from .models import Ticket, TicketImage

class TicketImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketImage
        fields = ['image']

class TicketSerializer(serializers.ModelSerializer):
    images = TicketImageSerializer(many=True, read_only=True)  # Nested serializer for images

    class Meta:
        model = Ticket
        fields = ['id', 'title', 'ticket_code', 'description', 'status', 'images', 'created_at']
