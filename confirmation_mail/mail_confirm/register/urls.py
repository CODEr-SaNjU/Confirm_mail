from django.urls import path,include
from . import views

urlpatterns = [
    path('register',views.SignUpView.as_view(),name='register'),
    path('activate/<uidb64>/<token>/', views.ActivateAccount.as_view(), name='activate'),
]