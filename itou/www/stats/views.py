from django.shortcuts import render

from django.db.models.functions import ExtractWeek, ExtractYear
from django.db.models import Sum, Count, Avg

from itou.prescribers.models import PrescriberOrganization
from itou.siaes.models import Siae
from itou.users.models import User
from itou.job_applications.models import JobApplication


def stats(request, template_name="stats/stats.html"):
    stats = (
        JobApplication.objects.annotate(year=ExtractYear("created_at"))
        .annotate(week=ExtractWeek("created_at"))
        .values("year", "week")
        .annotate(total=Count("pk"))
        .order_by("year", "week")
    )
    # stats = (
    #     JobApplication.objects
    #     .annotate(week=ExtractWeek("created_at"))
    #     .values("week")
    #     .annotate(total=Count("week"))
    #     .order_by("week")
    # )
    context = {"stats": stats}
    return render(request, template_name, context)
