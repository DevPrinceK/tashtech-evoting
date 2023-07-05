import csv
import io
import time
from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.db import IntegrityError


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
            voter.status = request.POST.get('status')
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
            voter.external_key = external_key
            voter.sex = request.POST.get('sex')
            voter.house = request.POST.get('house')
            voter.status = request.POST.get('status')
            voter.save()
            messages.success(request, 'Voter Created Successfully')
            return redirect('backend:voters')


class UploadVotersFromCSV(View):
    @method_decorator(AdminOnly)
    def get(self, request, *args, **kwargs):
        return redirect('backend:voters')

    @method_decorator(AdminOnly)
    def post(self, request, *args, **kwargs):
        new_voters = 0
        csv_file = request.FILES.get('csv_file')
        dataset = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(dataset)
        next(io_string)
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            external_key = str(int(100000 * time.time()))[::-1][0:5]  # noqa # generate password for voter
            # create user with custom user manager
            try:
                _ = User.objects.create_user(
                    index_number=column[4],
                    password=external_key,
                )
            except IntegrityError:
                '''Skip duplicate IDs'''
                print('Voter with index number {} already exists'.format(column[0]))  # noqa
            else:
                # update user with other relevant data after creating
                if _:
                    _.fullname = column[0]
                    _.sex = column[1]
                    _.user_class = column[2]
                    _.house = column[3]
                    _.status = column[5]
                    _.external_key = external_key
                    _.save()
                new_voters += 1
        if new_voters > 0:
            messages.success(request, '{} Voters Uploaded Successfully'.format(new_voters))  # noqa
        else:
            messages.error(request, 'No Voters Uploaded! Voters already exist')  # noqa
        return redirect('backend:voters')


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
