# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding unique constraint on 'Vote', fields ['voter', 'request']
        db.create_unique('voice_vote', ['voter', 'request_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Vote', fields ['voter', 'request']
        db.delete_unique('voice_vote', ['voter', 'request_id'])


    models = {
        'voice.request': {
            'Meta': {'object_name': 'Request'},
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '140'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'V'", 'max_length': '1'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'votes_needed': ('django.db.models.fields.IntegerField', [], {})
        },
        'voice.vote': {
            'Meta': {'unique_together': "(('request', 'voter'),)", 'object_name': 'Vote'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'request': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'votes'", 'to': "orm['voice.Request']"}),
            'used_facebook': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'used_twitter': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'voter': ('django.db.models.fields.EmailField', [], {'max_length': '75'})
        }
    }

    complete_apps = ['voice']
