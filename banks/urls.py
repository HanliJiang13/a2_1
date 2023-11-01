# banks/urls.py
from django.urls import path
from .views import BankCreateView, BranchCreateView, branch_detail, all_branches_of_bank
from . import views

urlpatterns = [
    path('add/', BankCreateView.as_view(), name='add_bank'),
    path('<int:bank_id>/branches/add/', BranchCreateView.as_view(), name='add_branch'),
    path('branch/<int:branch_id>/details/', branch_detail, name='branch_details'),
    path('<int:bank_id>/branches/all/', all_branches_of_bank, name='all_branches'),
    path('all/', views.BankListView.as_view(), name='banks_all'),
    path('<int:pk>/details/', views.BankDetailView.as_view(), name='bank_details'),
    path('branch/<int:pk>/edit/', views.BranchUpdateView.as_view(), name='branch_edit'),
]