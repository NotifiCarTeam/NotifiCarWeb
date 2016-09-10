from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from django.core import validators
from django.contrib.auth.models import User

class Car(models.Model):
    owner = models.ForeignKey(User, verbose_name=_('Owner'))
    car_model = models.CharField(
        _("Car model"),
        max_length=20,
        validators=[
            validators.RegexValidator(
                r'^[a-zA-Z0-9\s+]+$',
                _('Car model must have only alphanumeric characters')
            )
        ],
        blank=False
    )
    color = models.CharField(
        _("Car color"),
        max_length=20,
        validators=[
            validators.RegexValidator(
                r'^[a-zA-Z\s+]+$',
                _('Car color must have only alphabetical characters')
            )
        ],
        blank=False
    )
    license_plate = models.CharField(
        _("License Plate"),
        max_length=7,
        validators=[
            validators.RegexValidator(
                r'^([A-Z]{3})([0-9]{4})$',
                _('License plate must contain 3 letters and 4 numbers')
            )
        ],
        help_text=_('Do not use hyphen (-). Use only letters and numbers. Ex.: JHG1234'),
        blank=False
    )

    def __str__(self):
        return (self.car_model + " - " + self.license_plate)
