import csv
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.utils.html import strip_tags
from django.views.generic import View
from django.http.response import HttpResponse
from backend.forms import CandidateForm

from backend.models import Candidate, Position
from core.utils.decorators import AdminOnly


class CandidatesListView(View):
    template = 'backend/lists/candidates.html'

    @method_decorator(AdminOnly)
    def get(self, request, *args, **kwargs):
        context = {'candidates': Candidate.objects.all().order_by('position__name', 'ballot_number')}  # noqa
        return render(request, self.template, context)


class CreateUpdateCandidateView(View):
    '''Class for creating and updating candidates'''
    template = 'backend/create_update_candidate.html'

    @method_decorator(AdminOnly)
    def get(self, request, *args, **kwargs):
        candidate_id = request.GET.get('candidate_id')
        candidate = Candidate.objects.filter(id=candidate_id).first()
        positions = Position.objects.all()
        context = {'positions': positions, 'candidate': candidate}
        return render(request, self.template, context)

    @method_decorator(AdminOnly)
    def post(self, request, *args, **kwargs):
        position_id = request.POST.get('position')
        candidate_id = request.POST.get('candidate_id')
        position = Position.objects.filter(id=position_id).first()

        if candidate_id:
            # candidate exists
            candidate = Candidate.objects.filter(id=candidate_id).first()
            form = CandidateForm(request.POST, request.FILES, instance=candidate)  # noqa
            if form.is_valid():
                candidate = form.save(commit=False)
                candidate.position = position
                candidate.save()
                messages.success(request, 'Candidate Details Updated Successfully.')  # noqa
                return redirect('backend:candidates')
            else:
                for field, error in form.errors.items():
                    message = f"{field.title()}: {strip_tags(error)}"
                    break
                messages.warning(request, message)
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        else:
            # it's a new candidate
            form = CandidateForm(request.POST, request.FILES)
            if form.is_valid():
                candidate = form.save(commit=False)
                candidate.position = position
                candidate.save()
                messages.success(request, 'New Candidate Created Successfully.')  # noqa
                return redirect('backend:candidates')
            else:
                for field, error in form.errors.items():
                    message = f"{field.title()}: {strip_tags(error)}"
                    break
                messages.warning(request, message)
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


class DeleteCandidateView(View):
    @method_decorator(AdminOnly)
    def get(self, request, *args, **kwargs):
        return redirect('backend:candidates')

    @method_decorator(AdminOnly)
    def post(self, request, *args, **kwargs):
        candidate_id = request.POST.get('candidate_id')
        candidate = Candidate.objects.filter(id=candidate_id)
        candidate.delete()
        messages.success(request, 'Candidate Deleted Successfully!')
        return redirect('backend:candidates')


class DownloadCandidateResultsAsCSVView(View):
    @method_decorator(AdminOnly)
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="election_results.csv"'  # noqa

        writer = csv.writer(response)
        writer.writerow(
            ['BALLOT NO.', 'POSITION', 'CANDIDATE', 'VOTES COUNT', 'NO VOTES', 'VOTE COUNT %', 'NO VOTES %'])  # noqa

        candidates = Candidate.objects.all().order_by('position__name', 'ballot_number')  # noqa
        for candidate in candidates:
            writer.writerow(
                [
                    candidate.ballot_number,
                    candidate.position.name,
                    candidate.name,
                    candidate.vote_count,
                    candidate.no_votes_count,
                    candidate.get_vote_percentage(),
                    candidate.get_no_vote_percentage(),
                ]
            )
        return response
