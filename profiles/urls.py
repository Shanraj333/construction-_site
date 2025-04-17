from django.urls import path
from . import views

urlpatterns = [
    # ✅ Home route
    path('', views.home, name='home'),
     path('submit-feedback/', views.submit_feedback, name='submit_feedback'),
     path('delete-feedback/<int:feedback_id>/', views.delete_feedback, name='delete_feedback'),

    # Lists
    path('engineers/', views.engineers_list, name='engineers_list'),
    path('contractors/', views.contractors_list, name='contractors_list'),
    path('workers/', views.workers_list, name='workers_list'),


    # Registration routes
    path('register/engineer/', views.register_engineer, name='register_engineer'),
    path('register/contractor/', views.register_contractor, name='register_contractor'),
    path('register/worker/', views.register_worker, name='register_worker'),

    # Admin actions
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/approve/<int:profile_id>/', views.approve_profile, name='approve_profile'),
    path('dashboard/reject/<int:profile_id>/', views.reject_profile, name='reject_profile'),


    path('dashboard/delete/<int:profile_id>/', views.delete_profile, name='delete_profile'),
    path('dashboard/delete_all/<str:category>/', views.delete_all_profiles, name='delete_all_profiles'),

]