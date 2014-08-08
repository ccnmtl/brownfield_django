# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Interactive'
        db.create_table(u'interactive_interactive', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('interactive_type', self.gf('django.db.models.fields.CharField')(max_length=2)),
        ))
        db.send_create_signal(u'interactive', ['Interactive'])


    def backwards(self, orm):
        # Deleting model 'Interactive'
        db.delete_table(u'interactive_interactive')


    models = {
        u'interactive.interactive': {
            'Meta': {'object_name': 'Interactive'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interactive_type': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        }
    }

    complete_apps = ['interactive']