from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Admin, Support, Developer, Ticket
from .serializers import AdminSerializer, SupportSerializer, DeveloperSerializer, TicketSerializer

# Login (Mobile & OTP)
class LoginView(APIView):
    def post(self, request):
        mobile = request.data.get('mobile')
        otp = request.data.get('otp')
        try:
            user = Admin.objects.get(mobile=mobile, otp=otp)
            return Response({"message": "Login successful", "role": "admin"})
        except Admin.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

# CRUD for Support
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Support, Ticket
from .serializers import SupportSerializer, TicketSerializer

class SupportCRUD(APIView):
    # Handle GET, POST, PUT, DELETE for Support
    
    def get(self, request, *args, **kwargs):
        supports = Support.objects.all()
        serializer = SupportSerializer(supports, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = SupportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        support_id = kwargs.get('id')
        try:
            support = Support.objects.get(id=support_id)
        except Support.DoesNotExist:
            return Response({"error": "Support user not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = SupportSerializer(support, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        support_id = kwargs.get('id')
        try:
            support = Support.objects.get(id=support_id)
            support.delete()
            return Response({"message": "Support user deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Support.DoesNotExist:
            return Response({"error": "Support user not found"}, status=status.HTTP_404_NOT_FOUND)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Developer
from .serializers import DeveloperSerializer

class DeveloperCRUD(APIView):
    # Handle GET, POST, PUT, DELETE for Developer

    def get(self, request, *args, **kwargs):
        # Retrieve all developers or a specific developer by ID
        developer_id = kwargs.get('id')
        if developer_id:
            try:
                developer = Developer.objects.get(id=developer_id)
                serializer = DeveloperSerializer(developer)
                return Response(serializer.data)
            except Developer.DoesNotExist:
                return Response({"error": "Developer not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            developers = Developer.objects.all()
            serializer = DeveloperSerializer(developers, many=True)
            return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        # Create a new developer record
        serializer = DeveloperSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        # Update an existing developer record
        developer_id = kwargs.get('id')
        try:
            developer = Developer.objects.get(id=developer_id)
        except Developer.DoesNotExist:
            return Response({"error": "Developer not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = DeveloperSerializer(developer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        # Delete a developer record
        developer_id = kwargs.get('id')
        try:
            developer = Developer.objects.get(id=developer_id)
            developer.delete()
            return Response({"message": "Developer deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Developer.DoesNotExist:
            return Response({"error": "Developer not found"}, status=status.HTTP_404_NOT_FOUND)




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Ticket, TicketImage
from .serializers import TicketSerializer
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404


class TicketListView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can view tickets
    
    def get(self, request, *args, **kwargs):
        role = request.user.role  # Assuming you have a role field in your User model
        
        if role != 'support' and role != 'admin':
            return Response({"error": "You are not authorized to view tickets."}, status=status.HTTP_403_FORBIDDEN)
        
        tickets = Ticket.objects.all()
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)


class TicketCreateView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can create tickets
    
    def post(self, request, *args, **kwargs):
        role = request.user.role  # Get role from authenticated user
        
        if role != 'support':
            return Response({"error": "You are not authorized to create tickets."}, status=status.HTTP_403_FORBIDDEN)

        ticket_code = request.data.get('ticket_code')
        title = request.data.get('title')
        description = request.data.get('description')
        status = request.data.get('status', 'open')
        images = request.FILES.getlist('images')  # Get list of images uploaded by user
        
        ticket = Ticket.objects.create(
            title=title,
            description=description,
            ticket_code=ticket_code,
            status=status
        )

        # Add images to the TicketImage model if any
        for image in images:
            TicketImage.objects.create(ticket=ticket, image=image)
        
        serializer = TicketSerializer(ticket)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TicketUpdateView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can update tickets
    
    def put(self, request, *args, **kwargs):
        role = request.user.role  # Get role from authenticated user
        
        if role != 'support':
            return Response({"error": "You are not authorized to update tickets."}, status=status.HTTP_403_FORBIDDEN)

        ticket_id = kwargs.get('id')  # Get the ticket ID from the URL
        ticket = get_object_or_404(Ticket, id=ticket_id)
        
        ticket.title = request.data.get('title', ticket.title)
        ticket.description = request.data.get('description', ticket.description)
        ticket.status = request.data.get('status', ticket.status)

        # Update images if new images are uploaded
        if 'images' in request.FILES:
            images = request.FILES.getlist('images')
            for image in images:
                TicketImage.objects.create(ticket=ticket, image=image)

        ticket.save()
        serializer = TicketSerializer(ticket)
        return Response(serializer.data)


class TicketDeleteView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can delete tickets
    
    def delete(self, request, *args, **kwargs):
        role = request.user.role  # Get role from authenticated user
        
        if role != 'support':
            return Response({"error": "You are not authorized to delete tickets."}, status=status.HTTP_403_FORBIDDEN)

        ticket_id = kwargs.get('id')  # Get the ticket ID from the URL
        ticket = get_object_or_404(Ticket, id=ticket_id)
        ticket.delete()
        return Response({"message": "Ticket deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class TicketDetailView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can view ticket details
    
    def get(self, request, *args, **kwargs):
        ticket_id = kwargs.get('id')  # Get the ticket ID from the URL
        ticket = get_object_or_404(Ticket, id=ticket_id)
        serializer = TicketSerializer(ticket)
        return Response(serializer.data)

