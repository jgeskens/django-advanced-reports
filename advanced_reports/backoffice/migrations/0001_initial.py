# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

from django.conf import settings

# This is done for compatibility with other databases.
POSTGRES_AVAILABLE = 'postgresql' in settings.DATABASES['default'].get('ENGINE', '')

def get_models():
    models = {
        u'backoffice.searchindex': {
            'Meta': {'object_name': 'SearchIndex'},
            'backoffice_instance': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'model_slug': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'to_index': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    if POSTGRES_AVAILABLE:
        models[u'backoffice.searchindex'].update({'search_index': ('djorm_pgfulltext.fields.VectorField', [], {'default': "''", 'null': 'True', 'db_index': 'True'})})

    return models

def get_table(migr):
    table = [
        (u'id', migr.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ('backoffice_instance', migr.gf('django.db.models.fields.CharField')(max_length=32)),
        ('model_slug', migr.gf('django.db.models.fields.CharField')(max_length=32)),
        ('model_id', migr.gf('django.db.models.fields.PositiveIntegerField')()),
        ('to_index', migr.gf('django.db.models.fields.TextField')(blank=True))
    ]

    if POSTGRES_AVAILABLE:
        table.append(('search_index', migr.gf('djorm_pgfulltext.fields.VectorField')(default='', null=True, db_index=True)))

    return table

class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SearchIndex'
        db.create_table(u'backoffice_searchindex', get_table(self))
        db.send_create_signal(u'backoffice', ['SearchIndex'])

        if not POSTGRES_AVAILABLE:
            print('Please execute following SQL queries to enable MySQL Full Text Search:')
            print('ALTER TABLE backoffice_searchindex ENGINE=MyISAM;')
            print('CREATE FULLTEXT INDEX backoffice_searchindex_fulltext ON backoffice_searchindex (to_index);')


    def backwards(self, orm):
        # Deleting model 'SearchIndex'
        db.delete_table(u'backoffice_searchindex')


    models = get_models()

    complete_apps = ['backoffice']
