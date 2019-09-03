from django.test import TestCase
from django.urls import reverse

from itou.jobs.factories import create_test_romes_and_appellations
from itou.jobs.models import Appellation
from itou.siaes.factories import SiaeWithMembershipFactory
from itou.users.factories import DEFAULT_PASSWORD


class ConfigureJobsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase.

        siae = SiaeWithMembershipFactory()
        user = siae.members.first()

        create_test_romes_and_appellations(["N1101", "N1105", "N1103", "N4105"])
        appellations = Appellation.objects.filter(
            name__in=[
                "Agent / Agente cariste de livraison ferroviaire",
                "Agent / Agente de quai manutentionnaire",
                "Agent magasinier / Agente magasinière gestionnaire de stocks",
                "Chauffeur-livreur / Chauffeuse-livreuse",
            ]
        )
        siae.jobs.add(*appellations)

        cls.siae = siae
        cls.user = user

        cls.url = reverse("dashboard:configure_jobs")

    def test_access(self):

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user.email, password=DEFAULT_PASSWORD)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_content(self):

        self.client.login(username=self.user.email, password=DEFAULT_PASSWORD)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(self.siae.jobs.count(), 4)
        response_content = str(response.content)
        for appellation in self.siae.jobs.all():
            self.assertIn(f'value="{appellation.code}"', response_content)
            self.assertIn(f'name="is_active-{appellation.code}"', response_content)

    def test_update(self):

        self.client.login(username=self.user.email, password=DEFAULT_PASSWORD)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        post_data = {
            # List of appellations codes that we will operate on.
            "code": ["10357", "10579", "10750", "10877", "16361"],
            # Do nothing for "Agent / Agente cariste de livraison ferroviaire"
            "is_active-10357": "on",  # "on" is set when the checkbox is checked.
            # Update "Agent / Agente de quai manutentionnaire"
            "is_active-10579": "",
            # Update "Agent magasinier / Agente magasinière gestionnaire de stocks"
            "is_active-10750": "",
            # Delete for "Chauffeur-livreur / Chauffeuse-livreuse"
            # Exclude code `11999` from POST payload.
            # Add "Aide-livreur / Aide-livreuse"
            "is_active-10877": "on",
            # Add "Manutentionnaire"
            "is_active-16361": "",
        }

        response = self.client.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 302)

        self.assertEqual(self.siae.jobs.count(), 5)
        self.assertEqual(self.siae.jobs_through.count(), 5)

        self.assertTrue(
            self.siae.jobs_through.get(appellation_id=10357, is_active=True)
        )
        self.assertTrue(
            self.siae.jobs_through.get(appellation_id=10579, is_active=False)
        )
        self.assertTrue(
            self.siae.jobs_through.get(appellation_id=10750, is_active=False)
        )
        self.assertTrue(
            self.siae.jobs_through.get(appellation_id=10877, is_active=True)
        )
        self.assertTrue(
            self.siae.jobs_through.get(appellation_id=16361, is_active=False)
        )