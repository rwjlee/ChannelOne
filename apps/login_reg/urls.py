from django.urls import path
from . import views

app_name = 'login_reg'

urlpatterns = [
    path('', views.index, name='index'),
    path('bills', views.bills, name='bills'),
    path('get_bills', views.get_bills, name='get_bills'),
    path('save_bill', views.save_bill, name='save_bill'),
    path('delete_bill/<int:bill_id>', views.delete_bill, name='delete_bill'),
    path('update_bill/<int:bill_id>', views.update_bill, name='update_bill'),
    path('projects', views.projects, name='projects'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('authenticate/<str:auth_for>', views.authenticate, name='authenticate'),
    path('logout', views.logout, name='logout'),
    path('authenticate_ajax/<str:auth_for>', views.authenticate_ajax, name='authenticate_ajax'),
    path('demo', views.demo, name='demo'),
]