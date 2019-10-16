# Generated by Django 2.2.4 on 2019-09-30 13:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("prescribers", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="prescriberorganization",
            name="members",
            field=models.ManyToManyField(
                blank=True,
                through="prescribers.PrescriberMembership",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Membres",
            ),
        ),
        migrations.AddField(
            model_name="prescribermembership",
            name="organization",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="prescribers.PrescriberOrganization",
            ),
        ),
        migrations.AddField(
            model_name="prescribermembership",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]