import csv
import io
import time
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.utils.html import strip_tags
from django.views.generic import View
from accounts.models import User

from core.utils.decorators import AdminOnly


class VotersView(View):
    template = 'backend/lists/voters.html'

    @method_decorator(AdminOnly)
    def get(self, request, *args, **kwargs):
        voters = User.objects.filter(is_student=True).order_by('-index_number')
        context = {'voters': voters}
        return render(request, self.template, context)


class CreateUpdateVoterView(View):
    template = 'backend/create_update_voter.html'

    @method_decorator(AdminOnly)
    def get(self, request, *args, **kwargs):
        voter_index = request.GET.get('index_number')
        voter = User.objects.filter(index_number=voter_index, is_student=True).first()  # noqa
        context = {'voter': voter}
        return render(request, self.template, context)

    @method_decorator(AdminOnly)
    def post(self, request, *args, **kwargs):
        voter_index = request.POST.get('index_number')
        voter = User.objects.filter(index_number=voter_index, is_student=True).first() if voter_index else None  # noqa

        if voter is not None:
            '''Voter already exist so update'''
            voter.index_number = request.POST.get('index_number')
            voter.fullname = request.POST.get('fullname')
            voter.user_class = request.POST.get('user_class')
            voter.save()
            messages.success(request, 'Voter Details Updated Successfully')
            return redirect('backend:voters')
        else:
            '''Voter doesn't exist so create new voter'''
            external_key = str(int(100000 * time.time()))[::-1][0:5]  # noqa # generate password for voter
            voter = User.objects.create_user(
                index_number=request.POST.get('index_number'),
                password=external_key
            )
            voter.fullname = request.POST.get('fullname')
            voter.user_class = request.POST.get('user_class')
            voter.save()
            messages.success(request, 'Voter Created Successfully')
            return redirect('backend:voters')


class UploadVotersFromCSV(View):
    @method_decorator(AdminOnly)
    def get(self, request, *args, **kwargs):
        return redirect('backend:voters')

    @method_decorator(AdminOnly)
    def post(self, request, *args, **kwargs):
        csv_file = request.FILES.get('csv_file')
        dataset = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(dataset)
        next(io_string)
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            _, created = User.objects.update_or_create(
                teacher_id=column[0],
                teacher_name=column[1],
                teacher_gender=column[2],
                teacher_d_o_b=column[3],
                teacher_mobile=column[4],
            )
        messages.success(request, "Teachers uploaded successfully")
        return redirect('admin_teachers')



class DeleteVoterView(View):
    @method_decorator(AdminOnly)
    def get(self, request, *args, **kwargs):
        return redirect('backend:voters')

    @method_decorator(AdminOnly)
    def post(self, request, *args, **kwargs):
        voter_index = request.POST.get('index_number')
        voter = User.objects.filter(index_number=voter_index, is_student=True).first()  # noqa
        voter.delete()
        messages.success(request, 'Voter Deleted Successfully')
        return redirect('backend:voters')
