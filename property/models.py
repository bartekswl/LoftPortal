from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# from django.core.exceptions import ValidationError
# from django.utils.translation import gettext_lazy as _


# def validate_even(value):
#     if value != 'Cassia':
#         raise ValidationError(
#             _('%(value)s is not an even number'),
#             params={'value': value},
#         )

flat_codes = (('C1', 'C1'), ('C2','C2'), ('C3', 'C3'),('R1', 'R1'), ('R2','R2'), ('R3', 'R3'))
building_codes = (('Cassia', 'Cassia'),('Rosewood', 'Rosewood'))

class Flat(models.Model):
    
    flat_number    = models.CharField(max_length=4, choices=flat_codes, null=True, blank=False, unique=True)
    building       = models.CharField(max_length=8, choices=building_codes, null=True, blank=False)
    core           = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=False)
    floor          = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(8)], null=True, blank=False)
    flat_size      = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(3)], null=True, blank=False)
    flat_type      = models.CharField(max_length=10, null=True, blank=False)
    auth_access    = models.CharField(max_length=100, blank=True)
    additional_notes= models.TextField(max_length=300, blank=True)
    
    
    
    def __str__(self):
        return self.flat_number





class Tenant(models.Model):

    name          = models.CharField(max_length=15, null=True, blank=False)
    surname       = models.CharField(max_length=30, null=True, blank=False)
    email         = models.EmailField(max_length=100, unique=True)
    phone_number  = models.CharField(max_length=20, null=True, blank=True, unique=True)
    flat          = models.ForeignKey(Flat, on_delete=models.PROTECT)
    status        = models.CharField(max_length=10, null=True, blank=False)
    stay_length   = models.CharField(max_length=20, null=True, blank=False)
    pet_licence   = models.CharField(max_length=20, null=True, blank=False)
    additional_notes= models.TextField(max_length=300, blank=True)

    class Meta:
        unique_together = ('name', 'surname',)


    def __str__(self):
        return f'{self.name} {self.surname}' 