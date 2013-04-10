# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Schema'
        db.create_table('searchengine_schema', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('namespace', self.gf('django.db.models.fields.URLField')(max_length=400)),
            ('name', self.gf('django.db.models.fields.SlugField')(default='', max_length=50)),
            ('description', self.gf('django.db.models.fields.CharField')(default='', max_length=80)),
        ))
        db.send_create_signal('searchengine', ['Schema'])

        # Adding unique constraint on 'Schema', fields ['namespace', 'name']
        db.create_unique('searchengine_schema', ['namespace', 'name'])

        # Adding model 'ParameterName'
        db.create_table('searchengine_parametername', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('schema', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['searchengine.Schema'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('type', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('ranking', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('initial', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('choices', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('help_text', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('max_length', self.gf('django.db.models.fields.IntegerField')(default=255)),
        ))
        db.send_create_signal('searchengine', ['ParameterName'])

        # Adding unique constraint on 'ParameterName', fields ['schema', 'name']
        db.create_unique('searchengine_parametername', ['schema_id', 'name'])

        # Adding model 'MyTardisProfile'
        db.create_table('searchengine_mytardisprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=400)),
            ('institution', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('searchengine', ['MyTardisProfile'])

        # Adding model 'MyTardisProfileParameterSet'
        db.create_table('searchengine_mytardisprofileparameterset', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mytardis_profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['searchengine.MyTardisProfile'], unique=True)),
            ('schema', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['searchengine.Schema'])),
            ('ranking', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('searchengine', ['MyTardisProfileParameterSet'])

        # Adding model 'MyTardisParameter'
        db.create_table('searchengine_mytardisparameter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['searchengine.ParameterName'])),
            ('parameter_set', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['searchengine.MyTardisProfileParameterSet'])),
            ('value', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('searchengine', ['MyTardisParameter'])

        # Adding model 'ExperimentProfile'
        db.create_table('searchengine_experimentprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('experiment_id', self.gf('django.db.models.fields.IntegerField')()),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('searchengine', ['ExperimentProfile'])

        # Adding model 'ExperimentProfileParameterSet'
        db.create_table('searchengine_experimentprofileparameterset', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('experiment_profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['searchengine.ExperimentProfile'], unique=True)),
            ('schema', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['searchengine.Schema'])),
            ('ranking', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('searchengine', ['ExperimentProfileParameterSet'])

        # Adding model 'ExperimentParameter'
        db.create_table('searchengine_experimentparameter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['searchengine.ParameterName'])),
            ('paramset', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['searchengine.ExperimentProfileParameterSet'])),
            ('value', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('searchengine', ['ExperimentParameter'])


    def backwards(self, orm):
        # Removing unique constraint on 'ParameterName', fields ['schema', 'name']
        db.delete_unique('searchengine_parametername', ['schema_id', 'name'])

        # Removing unique constraint on 'Schema', fields ['namespace', 'name']
        db.delete_unique('searchengine_schema', ['namespace', 'name'])

        # Deleting model 'Schema'
        db.delete_table('searchengine_schema')

        # Deleting model 'ParameterName'
        db.delete_table('searchengine_parametername')

        # Deleting model 'MyTardisProfile'
        db.delete_table('searchengine_mytardisprofile')

        # Deleting model 'MyTardisProfileParameterSet'
        db.delete_table('searchengine_mytardisprofileparameterset')

        # Deleting model 'MyTardisParameter'
        db.delete_table('searchengine_mytardisparameter')

        # Deleting model 'ExperimentProfile'
        db.delete_table('searchengine_experimentprofile')

        # Deleting model 'ExperimentProfileParameterSet'
        db.delete_table('searchengine_experimentprofileparameterset')

        # Deleting model 'ExperimentParameter'
        db.delete_table('searchengine_experimentparameter')


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
        'searchengine.mytardisparameter': {
            'Meta': {'ordering': "['name']", 'object_name': 'MyTardisParameter'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['searchengine.ParameterName']"}),
            'parameter_set': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['searchengine.MyTardisProfileParameterSet']"}),
            'value': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'searchengine.mytardisprofile': {
            'Meta': {'object_name': 'MyTardisProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '400'})
        },
        'searchengine.mytardisprofileparameterset': {
            'Meta': {'ordering': "['-ranking']", 'object_name': 'MyTardisProfileParameterSet'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mytardis_profile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['searchengine.MyTardisProfile']", 'unique': 'True'}),
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