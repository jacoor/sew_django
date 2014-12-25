# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Profile.photo'
        db.add_column(u'profiles_profile', 'photo',
                      self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True),
                      keep_default=False)

        # Adding field 'Profile.street'
        db.add_column(u'profiles_profile', 'street',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'Profile.house'
        db.add_column(u'profiles_profile', 'house',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'Profile.flat'
        db.add_column(u'profiles_profile', 'flat',
                      self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Profile.zip'
        db.add_column(u'profiles_profile', 'zip',
                      self.gf('sew_django.profiles.fields.PLPostalCodeModelField')(default=1, max_length=6),
                      keep_default=False)

        # Adding field 'Profile.city'
        db.add_column(u'profiles_profile', 'city',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'Profile.phone'
        db.add_column(u'profiles_profile', 'phone',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=100),
                      keep_default=False)

        # Adding field 'Profile.workplace_name'
        db.add_column(u'profiles_profile', 'workplace_name',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Profile.workplace_address'
        db.add_column(u'profiles_profile', 'workplace_address',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Profile.workplace_zip'
        db.add_column(u'profiles_profile', 'workplace_zip',
                      self.gf('sew_django.profiles.fields.PLPostalCodeModelField')(max_length=6, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Profile.workplace_city'
        db.add_column(u'profiles_profile', 'workplace_city',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Profile.photo'
        db.delete_column(u'profiles_profile', 'photo')

        # Deleting field 'Profile.street'
        db.delete_column(u'profiles_profile', 'street')

        # Deleting field 'Profile.house'
        db.delete_column(u'profiles_profile', 'house')

        # Deleting field 'Profile.flat'
        db.delete_column(u'profiles_profile', 'flat')

        # Deleting field 'Profile.zip'
        db.delete_column(u'profiles_profile', 'zip')

        # Deleting field 'Profile.city'
        db.delete_column(u'profiles_profile', 'city')

        # Deleting field 'Profile.phone'
        db.delete_column(u'profiles_profile', 'phone')

        # Deleting field 'Profile.workplace_name'
        db.delete_column(u'profiles_profile', 'workplace_name')

        # Deleting field 'Profile.workplace_address'
        db.delete_column(u'profiles_profile', 'workplace_address')

        # Deleting field 'Profile.workplace_zip'
        db.delete_column(u'profiles_profile', 'workplace_zip')

        # Deleting field 'Profile.workplace_city'
        db.delete_column(u'profiles_profile', 'workplace_city')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'profiles.profile': {
            'Meta': {'object_name': 'Profile'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '110', 'db_index': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'flat': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            'house': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'pesel': ('sew_django.profiles.fields.PLPESELModelField', [], {'unique': 'True', 'max_length': '11', 'db_index': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'workplace_address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'workplace_city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'workplace_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'workplace_zip': ('sew_django.profiles.fields.PLPostalCodeModelField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'zip': ('sew_django.profiles.fields.PLPostalCodeModelField', [], {'max_length': '6'})
        }
    }

    complete_apps = ['profiles']