# -*- coding: utf-8 -*-
from django.db import models
from localflavor.pl.forms import PLPESELField
# Create your models here.

class PLPESELModelField(models.CharField):

    description = "CharField with PLPESELField widget"

    def formfield(self, **kwargs):
        # This is a fairly standard way to set up some defaults
        # while letting the caller override them.
        defaults = {'form_class': PLPESELField}
        defaults.update(kwargs)
        return super(PLPESELModelField, self).formfield(**defaults)

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^sew_django\.profiles\.fields\.PLPESELModelField"])