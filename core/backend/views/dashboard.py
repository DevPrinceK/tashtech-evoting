from django.shortcuts import render
from django.views import View

from backend.models import Candidate, Election, Position
from django.utils.decorators import method_decorator
from core.utils.constants import House, PositionName
from core.utils.decorators import AdminOnly


class IndexView(View):
    template = 'backend/index.html'

    @method_decorator(AdminOnly)
    def get(self, request, *args, **kwargs):
        current_election = Election.objects.filter(is_active=True).order_by('created_at').first()  # noqa
        positions_set_1 = Position.objects.all().order_by('-id')[:10]
        positions_set_2 = Position.objects.all().order_by('-id')[10:]

        sps = Candidate.objects.filter(position__name=PositionName.SP.value).order_by('ballot_number')  # noqa
        gps = Candidate.objects.filter(position__name=PositionName.GP.value).order_by('ballot_number')  # noqa

        cob = Candidate.objects.filter(position__name=PositionName.COB.value).order_by('ballot_number')  # noqa
        cog = Candidate.objects.filter(position__name=PositionName.COG.value).order_by('ballot_number')  # noqa

        sgpb = Candidate.objects.filter(position__name=PositionName.SGPB.value).order_by('ballot_number')  # noqa
        sgpg = Candidate.objects.filter(position__name=PositionName.SGPG.value).order_by('ballot_number')  # noqa

        dhpb = Candidate.objects.filter(position__name=PositionName.DHPB.value).order_by('ballot_number')  # noqa
        dhpg = Candidate.objects.filter(position__name=PositionName.DHPG.value).order_by('ballot_number')  # noqa

        ecpb = Candidate.objects.filter(position__name=PositionName.ECPB.value).order_by('ballot_number')  # noqa
        ecpg = Candidate.objects.filter(position__name=PositionName.ECPG.value).order_by('ballot_number')  # noqa

        plpb = Candidate.objects.filter(position__name=PositionName.PLPB.value).order_by('ballot_number').first()  # noqa
        plpg = Candidate.objects.filter(position__name=PositionName.PLPG.value).order_by('ballot_number').first()  # noqa

        csb = Candidate.objects.filter(position__name=PositionName.CSB.value).order_by('ballot_number').first()  # noqa
        csg = Candidate.objects.filter(position__name=PositionName.CSG.value).order_by('ballot_number').first()  # noqa

        # ppb = Candidate.objects.filter(position__name=PositionName.PPB.value).order_by('ballot_number')  # noqa
        # ppg = Candidate.objects.filter(position__name=PositionName.PPG.value).order_by('ballot_number')  # noqa

        hspb = Candidate.objects.filter(position__name=PositionName.HSPB.value).order_by('ballot_number')  # noqa
        hspg = Candidate.objects.filter(position__name=PositionName.HSPG.value).order_by('ballot_number').first()  # noqa

        hpba = Candidate.objects.filter(position__name=PositionName.HPB.value, house=House.ASANTE.value).order_by('ballot_number').first()  # noqa
        hpga = Candidate.objects.filter(position__name=PositionName.HPG.value, house=House.ASANTE.value).order_by('ballot_number').first()  # noqa

        hpbb = Candidate.objects.filter(position__name=PositionName.HPB.value, house=House.BOTWE.value).order_by('ballot_number').first()  # noqa
        hpgb = Candidate.objects.filter(position__name=PositionName.HPG.value, house=House.BOTWE.value).order_by('ballot_number').first()  # noqa

        hpbka = Candidate.objects.filter(position__name=PositionName.HPB.value, house=House.KALEDZI.value).order_by('ballot_number').first()  # noqa
        hpgka = Candidate.objects.filter(position__name=PositionName.HPG.value, house=House.KALEDZI.value).order_by('ballot_number').first()  # noqa

        hpbku = Candidate.objects.filter(position__name=PositionName.HPB.value, house=House.KUMI.value).order_by('ballot_number')  # noqa
        hpgku = Candidate.objects.filter(position__name=PositionName.HPG.value, house=House.KUMI.value).order_by('ballot_number')  # noqa

        context = {
            'current_election': current_election,
            'positions': positions_set_1,
            'positions_set_2': positions_set_2,
            'sps': sps,
            'gps': gps,
            'cob': cob,
            'cog': cog,
            'sgpb': sgpb,
            'sgpg': sgpg,
            'dhpb': dhpb,
            'dhpg': dhpg,
            'ecpb': ecpb,
            'ecpg': ecpg,
            'lpb': plpb,
            'lpg': plpg,
            'csb': csb,
            'csg': csg,
            # 'ppb': ppb,
            # 'ppg': ppg,
            'hspb': hspb,
            'hspg': hspg,
            'hpba': hpba,
            'hpga': hpga,
            'hpbb': hpbb,
            'hpgb': hpgb,
            'hpbka': hpbka,
            'hpgka': hpgka,
            'hpbku': hpbku,
            'hpgku': hpgku,
        }
        return render(request, self.template, context)
