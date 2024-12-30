from django.urls import path, include
from .views import LoginView, SupportCRUD
from .views import TicketListView, TicketCreateView, TicketUpdateView, TicketDeleteView, TicketDetailView
from .views import DeveloperCRUD  

urlpatterns = [
    # Login URL
    path('login/', LoginView.as_view(), name='login'),
    
    # Support CRUD URLs
    path('supports/', SupportCRUD.as_view(), name='support_crud'),  # Create and List Support users
    path('supports/update/<int:id>/', SupportCRUD.as_view(), name='support_update'),  # Update Support user by ID
    path('supports/delete/<int:id>/', SupportCRUD.as_view(), name='support_delete'),  # Delete Support user by ID
    
    path('tickets/', TicketListView.as_view(), name='ticket_list'),  # List all tickets
    path('tickets/create/', TicketCreateView.as_view(), name='ticket_create'),  # Create new ticket
    path('tickets/update/<int:id>/', TicketUpdateView.as_view(), name='ticket_update'),  # Update ticket by ID
    path('tickets/delete/<int:id>/', TicketDeleteView.as_view(), name='ticket_delete'),  # Delete ticket by ID
    path('tickets/<int:id>/', TicketDetailView.as_view(), name='ticket_detail'),  # View ticket details
    path('developers/', DeveloperCRUD.as_view()),  # For GET (list) and POST
    path('developers/<int:id>/', DeveloperCRUD.as_view()),  # For PUT and DELETE

   
]
