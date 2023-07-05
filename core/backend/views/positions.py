from django.db import IntegrityError
import csv
import io
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.utils.html import strip_tags
from django.views.generic import View

from backend.models import Candidate, Position
from backend.forms import PositionForm
from core.utils.decorators import AdminOnly


class PositionsView(View):
    template = 'backend/lists/positions.html'

    @method_decorator(AdminOnly)
    def get(self, request, *args, **kwargs):
        positions = Position.objects.all()
        context = {'positions': positions}
        return render(request, self.template, context)


class CreateUpdatePositionView(View):
    template = 'backend/create_update_position.html'

    @method_decorator(AdminOnly)
    def get(self, request, *args, **kwargs):
        position_id = request.GET.get('position_id')
        position = Position.objects.filter(id=position_id).first()
        context = {'position': position}
        return render(request, self.template, context)

    @method_decorator(AdminOnly)
    def post(self, request, *args, **kwargs):
        position_id = request.POST.get('position_id')
        position = Position.objects.filter(id=position_id).first() if position_id else None  # noqa
        form = PositionForm(request.POST, instance=position)
        if form.is_valid():
            form.save()
            if position is not None:
                messages.success(request, 'Position Updated Successfully')
            else:
                messages.success(request, 'New Position Created Successfully')
            return redirect('backend:positions')
        else:
            for field, error in form.errors.items():
                message = f"{field.title()}: {strip_tags(error)}"
                break
            messages.warning(request, message)
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


class UploadPositionsFromCSV(View):
    @method_decorator(AdminOnly)
    def get(self, request, *args, **kwargs):
        return redirect('backend:positions')

    @method_decorator(AdminOnly)
    def post(self, request, *args, **kwargs):
        new_positions = 0
        csv_file = request.FILES.get('csv_file')
        dataset = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(dataset)
        next(io_string)
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            # create position
            try:
                _ = Position.objects.create(
                    name=column[0],
                    precedence=column[1],
                )
            except IntegrityError:
                '''Skip duplicate IDs'''
                print('Voter with index number {} already exists'.format(column[0]))  # noqa
            else:
                # update user with other relevant data after creating
                if _:
                    print('Position with name {} created'.format(column[0]))  # noqa
                new_positions += 1
        if new_positions > 0:
            messages.success(request, '{} Positions Uploaded Successfully'.format(new_positions))  # noqa
        else:
            messages.error(request, 'No Positions Uploaded! Positions already exist')  # noqa
        return redirect('backend:positions')


class DeletePositionView(View):
    @method_decorator(AdminOnly)
    def get(self, request, *args, **kwargs):
        return redirect('backend:positions')

    @method_decorator(AdminOnly)
    def post(self, request, *args, **kwargs):
        position_id = request.POST.get('position_id')
        position = Position.objects.filter(id=position_id).first()
        position.delete()
        messages.success(request, 'Position Deleted Successfully')
        return redirect('backend:positions')
