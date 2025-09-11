from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path('qr/<str:reg_id>/', views.participant_qr, name='participant_qr'),
    path('scan/', views.scan_page, name='scan'),
    path('export_excel/', views.export_xlsx, name='export_excel'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('mark_attendance/<str:reg_id>/', views.mark_attendance, name='mark_attendance'),
    path('clear/', views.clear_participants, name='clear_participants'),
    path('signup/', views.SignUp_view, name='SignUp'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
