from django.shortcuts import render, get_object_or_404
from .forms import BookingForm
from .models import Menu, Category, Cart, Order, OrderItem, Booking
from rest_framework import viewsets, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User, Group
from .serializers import MenuSerializer, CategorySerializer, CartSerializer, OrderSerializer, BookingSerializer
from .permissions import IsManager, IsDeliveryCrew
from django_filters.rest_framework import DjangoFilterBackend

# HTML Template Views

def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def book(request):
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, 'book.html', context)

def menu(request):
    menu_data = Menu.objects.all()
    main_data = {"menu": menu_data}
    return render(request, 'menu.html', main_data)

def menu_item(request, pk):
    item = get_object_or_404(Menu, pk=pk)
    return render(request, 'menu_item.html', {"item": item})

def display_menu_items(request, pk=None):
    menu_item = get_object_or_404(Menu, pk=pk)
    return render(request, 'menu_item.html', {"menu_item": menu_item})

# API Views

class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CartView(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Manager').exists():
            return Order.objects.all()
        elif user.groups.filter(name='Delivery crew').exists():
            return Order.objects.filter(delivery_crew=user)
        else:
            return Order.objects.filter(user=user)

class ManagerGroupView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, user_id):
        user = User.objects.get(id=user_id)
        group = Group.objects.get(name='Manager')
        group.user_set.add(user)
        return Response({'message': 'User added to Manager group'})

# Booking API View

class BookingListCreateView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['first_name', 'last_name']
