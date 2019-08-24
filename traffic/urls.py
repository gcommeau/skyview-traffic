from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # API calls
    path('api/classrooms', views.ClassroomListCreate.as_view() ),
    path('api/get_students/<int:classroom_id>/', views.get_students, name='api_get_students'),
    path('api/cancel_checkout', views.cancel_checkout, name='api_cancel_checkout'),
    path('api/checkout', views.checkout, name='api_checkout'),
    # HTML views
    path('classroom', views.classroom_view, name='view_classroom' ),
    path('checkout', views.checkout_view, name='view_checkout'),
    path('login', auth_views.LoginView.as_view(), name='login'),
    path('', views.no_view),
]
