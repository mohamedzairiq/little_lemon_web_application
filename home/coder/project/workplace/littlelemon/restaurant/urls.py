from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from . import views

# DRF Router for API viewsets
router = DefaultRouter()
router.register(r'api/menu', views.MenuViewSet)
router.register(r'api/category', views.CategoryViewSet)
router.register(r'api/order', views.OrderViewSet)

urlpatterns = [
    # HTML Views
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('book/', views.book, name="book"),
    path('menu/', views.menu, name="menu"),
    path('menu/<int:pk>/', views.menu_item, name="menu_item"),

    # API URLs
    path('api/cart/', views.CartView.as_view(), name='cart'),
    path('api/assign-manager/<int:user_id>/',
         views.ManagerGroupView.as_view(), name='assign_manager'),
    path('api/booking/', views.BookingListCreateView.as_view(),
         name='booking-list-create'),

    # Token Authentication Route (required for rubric)
    path('api-token-auth/', obtain_auth_token),

    # Djoser endpoints (user management API, required for rubric)
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),

    # Router URLs (Menu, Category, Order)
    path('', include(router.urls)),
]
