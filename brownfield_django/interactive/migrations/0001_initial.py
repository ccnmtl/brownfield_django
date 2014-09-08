# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'VisualReconnaisence'
        db.create_table(u'interactive_visualreconnaisence', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'interactive', ['VisualReconnaisence'])

        # Adding model 'SiteHistory'
        db.create_table(u'interactive_sitehistory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'interactive', ['SiteHistory'])

        # Adding model 'Testing'
        db.create_table(u'interactive_testing', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('interactive_type', self.gf('django.db.models.fields.CharField')(max_length=2)),
        ))
        db.send_create_signal(u'interactive', ['Testing'])


    def backwards(self, orm):
        # Deleting model 'VisualReconnaisence'
        db.delete_table(u'interactive_visualreconnaisence')

        # Deleting model 'SiteHistory'
        db.delete_table(u'interactive_sitehistory')

        # Deleting model 'Testing'
        db.delete_table(u'interactive_testing')


    models = {
        u'interactive.sitehistory': {
            'Meta': {'object_name': 'SiteHistory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'interactive.testing': {
            'Meta': {'object_name': 'Testing'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interactive_type': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        u'interactive.visualreconnaisence': {
            'Meta': {'object_name': 'VisualReconnaisence'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['interactive']