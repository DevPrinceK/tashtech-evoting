from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.utils.html import strip_tags
from django.views.generic import View

from backend.models import Election
from backend.forms import ElectionForm
from core.utils.decorators import AdminOnly


class ElectionsView(View):
    template = 'backend/lists/elections.html'

    @method_decorator(AdminOnly)
    def get(self, request, *args, **kwargs):
        elections = Election.objects.all()
        context = {'elections': elections}
        return render(request, self.template, context)


class CreateUpdateElectionView(View):
    template = 'backend/create_update_election.html'

    @method_decorator(AdminOnly)
    def get(self, request, *args, **kwargs):
        election_id = request.GET.get('election_id')
        election = Election.objects.filter(id=election_id).first()
        context = {'election': election}
        return render(request, self.template, context)

    @method_decorator(AdminOnly)
    def post(self, request, *args, **kwargs):
        election_id = request.POST.get('election_id')
        election = Election.objects.filter(id=election_id).first() if election_id else None  # noqa
        form = ElectionForm(request.POST, instance=election)
        if form.is_valid():
            form.save()
            if election is not None:
                messages.success(request, 'Election Updated Successfully')
            else:
                messages.success(request, 'New Election Created Successfully')
            return redirect('backend:elections')
        else:
            for field, error in form.errors.items():
                message = f"{field.title()}: {strip_tags(error)}"
                break
            messages.warning(request, message)
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


class DeleteElectionView(View):
    @method_decorator(AdminOnly)
    def get(self, request, *args, **kwargs):
        return redirect('backend:elections')

    @method_decorator(AdminOnly)
    def post(self, request, *args, **kwargs):
        election_id = request.POST.get('election_id')
        election = Election.objects.filter(id=election_id).first()
        election.delete()
        messages.success(request, 'Election Deleted Successfully')
        return redirect('backend:elections')
