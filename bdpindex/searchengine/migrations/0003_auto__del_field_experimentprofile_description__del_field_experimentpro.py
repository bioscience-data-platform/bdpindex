# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'ExperimentProfile.description'
        db.delete_column('searchengine_experimentprofile', 'description')

        # Deleting field 'ExperimentProfile.location'
        db.delete_column('searchengine_experimentprofile', 'location')


    def backwards(self, orm):
        # Adding field 'ExperimentProfile.description'
        db.add_column('searchengine_experimentprofile', 'description',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'ExperimentProfile.location'
        db.add_column('searchengine_experimentprofile', 'location',
                      self.gf('django.db.models.fields.CharField')(default='123', max_length=255),
                      keep_default=False)


    models = {
        'searchengine.experimentparameter': {
            'Meta': {'ordering': "['name']", 'object_name': 'ExperimentParameter'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['searchengine.ParameterName']"}),
            'paramset': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['searchengine.ExperimentProfileParameterSet']"}),
            'value': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'searchengine.experimentprofile': {
            'Meta': {'object_name': 'ExperimentProfile'},
            'experiment_id': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'searchengine.experimentprofileparameterset': {
            'Meta': {'ordering': "['-ranking']", 'object_name': 'ExperimentProfileParameterSet'},
            'experiment_profile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['searchengine.ExperimentProfile']", 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ranking': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'schema': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['searchengine.Schema']"})
        },
        'searchengine.parametername': {
            'Meta': {'ordering': "['-ranking']", 'unique_together': "(('schema', 'name'),)", 'object_name': 'ParameterName'},
            'choices': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'help_text': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initial': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'max_length': ('django.db.models.fields.IntegerField', [], {'default': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'ranking': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'schema': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['searchengine.Schema']"}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'searchengine.schema': {
            'Meta': {'unique_together': "(('namespace', 'name'),)", 'object_name': 'Schema'},
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.SlugField', [], {'default': "''", 'max_length': '50'}),
            'namespace': ('django.db.models.fields.URLField', [], {'max_length': '400'})
        }
    }

    complete_apps = ['searchengine']