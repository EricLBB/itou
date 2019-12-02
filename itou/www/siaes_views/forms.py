from django import forms
from django.conf import settings
from django.core.exceptions import NON_FIELD_ERRORS
from django.utils.translation import gettext_lazy as _

from itou.siaes.models import Siae, SiaeMembership
from itou.utils.address.departments import DEPARTMENTS
from itou.utils.validators import validate_post_code


class CreateSiaeForm(forms.ModelForm):
    """
    Create a new SIAE (Agence / Etablissement in French).
    """

    def __init__(self, current_siae, *args, **kwargs):
        self.current_siae = current_siae
        super(CreateSiaeForm, self).__init__(*args, **kwargs)

        test_departments = {d: DEPARTMENTS[d] for d in settings.ITOU_TEST_DEPARTMENTS}
        self.fields.get("department").choices = test_departments.items()

        required_fields = ["address_line_1", "city", "department", "phone"]
        for required_field in required_fields:
            # Make field required without overwriting its other properties.
            self.fields[required_field].required = True

    class Meta:
        model = Siae
        fields = [
            "siret",
            "kind",
            "name",
            "brand",
            "address_line_1",
            "address_line_2",
            "post_code",
            "city",
            "department",
            "phone",
            "email",
            "website",
            "description",
        ]
        help_texts = {
            "brand": _(
                "Si ce champ est renseigné, il sera utilisé en tant que nom sur la fiche."
            ),
            "department": _(
                (
                    "Seulement les départements du Bas-Rhin (67), du Pas-de-Calais (62) "
                    + "et de la Seine Saint Denis (93) sont disponibles pendant la phase actuelle "
                    + "d'expérimentation de la plateforme de l'inclusion."
                )
            ),
            "phone": _("Par exemple 0610203040"),
            "website": _("Votre site web doit commencer par http:// ou https://"),
            "description": _("Texte de présentation de votre SIAE."),
        }
        error_messages = {
            NON_FIELD_ERRORS: {
                "unique_together": "Il ne peut pas exister plus qu'une %(model_name)s "
                + "avec ce %(field_labels)s, or il en existe déjà une."
            }
        }

    siret = forms.CharField(
        label=_("Numéro SIRET"),
        min_length=14,
        max_length=14,
        required=True,
        strip=True,
        help_text=_(
            "Saisissez 14 chiffres. "
            + "Doit être le SIRET de votre structure actuelle ou un SIRET avec le même SIREN."
        ),
    )

    source = forms.CharField(
        widget=forms.HiddenInput(), required=True, initial=Siae.SOURCE_USER_CREATED
    )

    post_code = forms.CharField(
        label=_("Code Postal"),
        min_length=5,
        max_length=5,
        validators=[validate_post_code],
        required=True,
        strip=True,
        help_text=_("Saisissez les 5 chiffres de votre code postal."),
    )

    def clean_siret(self):
        siret = self.cleaned_data["siret"]
        if not siret.startswith(self.current_siae.siren):
            raise forms.ValidationError(
                _(
                    "Le numéro SIRET doit avoir le SIREN {}".format(
                        self.current_siae.siren
                    )
                )
            )
        return siret

    def save(self, request, commit=True):

        siae = super().save(commit=commit)

        if commit:
            siae.geocode(siae.address_on_one_line, post_code=siae.post_code, save=False)
            siae.created_by = request.user
            siae.source = Siae.SOURCE_USER_CREATED
            siae.save()

            membership = SiaeMembership()
            membership.user = request.user
            membership.siae = siae
            membership.is_siae_admin = True
            membership.save()

        return siae


class EditSiaeForm(forms.ModelForm):
    """
    Edit an SIAE's card (or "Fiche" in French).
    """

    class Meta:
        model = Siae
        fields = ["brand", "phone", "email", "website", "description"]
        help_texts = {
            "brand": _(
                "Si ce champ est renseigné, il sera utilisé en tant que nom sur la fiche."
            ),
            "phone": _("Par exemple 0610203040"),
            "description": _("Texte de présentation de votre SIAE."),
            "website": _("Votre site web doit commencer par http:// ou https://"),
        }
