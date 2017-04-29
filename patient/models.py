#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Patient(models.Model):
    paternal_last = models.CharField(max_length=30)
    maternal_last = models.CharField(max_length=30)
    first = models.CharField(max_length=30)
    middle = models.CharField(max_length=30)
    suffix = models.CharField(max_length=5)
    prefix = models.CharField(max_length=5)
    dob = models.DateField()

    MALE = 'm'
    FEMALE = 'f'
    GENDER_CHOICES = ((MALE, "Male"), (FEMALE, "Female"))

    gender = models.CharField(
        max_length = 1,
        choices = GENDER_CHOICES,
        default = FEMALE,
    )

    street1 = models.CharField(max_length=64)
    street2 = models.CharField(max_length=64)
    city = models.CharField(max_length=30)
    colonia = models.CharField(max_length=30)

    STATE_CHOICES = (("AG", u"Aguascalientes"), 
                     ("BC", u"Baja California"), 
                     ("BS", u"Baja California Sur"), 
                     ("CH", u"Chihuahua"), 
                     ("CL", u"Colima"), 
                     ("CM", u"Campeche"), 
                     ("CO", u"Coahuila"), 
                     ("CS", u"Chiapas"), 
                     ("DF", u"Federal District"), 
                     ("DG", u"Durango"), 
                     ("GR", u"Guerrero"), 
                     ("GT", u"Guanajuato"), 
                     ("HG", u"Hidalgo"), 
                     ("JA", u"Jalisco"), 
                     ("ME", u"México State"), 
                     ("MI", u"Michoacán"), 
                     ("MO", u"Morelos"), 
                     ("NA", u"Nayarit"), 
                     ("NL", u"Nuevo León"), 
                     ("OA", u"Oaxaca"), 
                     ("PB", u"Puebla"), 
                     ("QE", u"Querétaro"), 
                     ("QR", u"Quintana Roo"), 
                     ("SI", u"Sinaloa"), 
                     ("SL", u"San Luis Potosí"), 
                     ("SO", u"Sonora"), 
                     ("TB", u"Tabasco"), 
                     ("TL", u"Tlaxcala"), 
                     ("TM", u"Tamaulipas"), 
                     ("VE", u"Veracruz"), 
                     ("YU", u"Yucatán"), 
                     ("ZA", u"Zacatecas"), 
                    )

    state = models.CharField(
        max_length = 2,
        choices = STATE_CHOICES,
        default = "BC",
    )

    phone1 = models.CharField(max_length=20)
    phone2 = models.CharField(max_length=20)
    email = models.EmailField()
    emergencyfullname = models.CharField(max_length=64)
    emergencyphone = models.CharField(max_length=20)
    emergencyemail = models.EmailField()
