# banks/views.py
from django.http import HttpResponseForbidden, Http404, JsonResponse
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import BankForm, BranchForm
from .models import Bank, Branch

class BankCreateView(LoginRequiredMixin, FormView):
    template_name = 'banks/create.html'
    form_class = BankForm
    success_url = '/banks/{id}/details/'  # will be overridden dynamically

    def form_valid(self, form):
        bank = form.save(commit=False)
        bank.owner = self.request.user
        bank.save()
        self.success_url = reverse_lazy('bank_details', kwargs={'pk': bank.id})
        return super().form_valid(form)
    

class BranchCreateView(LoginRequiredMixin, FormView):
    template_name = 'banks/branch.html'
    form_class = BranchForm

    def dispatch(self, request, *args, **kwargs):
        self.bank = Bank.objects.filter(id=self.kwargs['bank_id']).first()
        if not self.bank:
            raise Http404
        if self.bank.owner != self.request.user:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        branch = form.save(commit=False)
        branch.bank = self.bank
        branch.save()
        self.success_url = reverse_lazy('branch_details', kwargs={'branch_id': branch.id})
        return super().form_valid(form)

def branch_detail(request, branch_id):
    try:
        branch = Branch.objects.get(pk=branch_id)
        data = {
            "id": branch.id,
            "name": branch.name,
            "transit_num": branch.transit_num,
            "address": branch.address,
            "email": branch.email,
            "capacity": branch.capacity,
            "last_modified": branch.last_modified.isoformat()
        }
        return JsonResponse(data)
    except Branch.DoesNotExist:
        raise Http404

def all_branches_of_bank(request, bank_id):
    branches = Branch.objects.filter(bank__id=bank_id)
    
    if not branches.exists():
        raise Http404

    data = [{
        "id": branch.id,
        "name": branch.name,
        "transit_num": branch.transit_num,
        "address": branch.address,
        "email": branch.email,
        "capacity": branch.capacity,
        "last_modified": branch.last_modified.isoformat()
    } for branch in branches]
    
    return JsonResponse(data, safe=False)

class BankListView(ListView):
    model = Bank
    template_name = 'banks/list.html'
    context_object_name = 'banks'

class BankDetailView(DetailView):
    model = Bank
    template_name = 'banks/detail.html'

class BranchUpdateView(LoginRequiredMixin, UpdateView):
    model = Branch
    fields = ['name', 'transit_num', 'address', 'email', 'capacity']
    template_name = 'banks/branch_update.html'

    def get_success_url(self):
        return reverse_lazy('branch_details', kwargs={'branch_id': self.object.pk})

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        branch = self.get_object()  # get the branch object
        if branch.bank.owner != self.request.user:
            return HttpResponseForbidden("You don't have permission to edit this branch.")
        return response