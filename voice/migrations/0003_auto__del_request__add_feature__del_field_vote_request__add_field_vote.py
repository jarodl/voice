# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Removing unique constraint on 'Vote', fields ['voter', 'request']
        db.delete_unique('voice_vote', ['voter', 'request_id'])

        # Deleting model 'Request'
        db.delete_table('voice_request')

        # Adding model 'Feature'
        db.create_table('voice_feature', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('state', self.gf('django.db.models.fields.CharField')(default='V', max_length=1)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=140)),
            ('votes_needed', self.gf('django.db.models.fields.IntegerField')()),
            ('created', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('voice', ['Feature'])

        # Deleting field 'Vote.request'
        db.delete_column('voice_vote', 'request_id')

        # Adding field 'Vote.feature'
        db.add_column('voice_vote', 'feature', self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='votes', to=orm['voice.Feature']), keep_default=False)

        # Adding unique constraint on 'Vote', fields ['voter', 'feature']
        db.create_unique('voice_vote', ['voter', 'feature_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Vote', fields ['voter', 'feature']
        db.delete_unique('voice_vote', ['voter', 'feature_id'])

        # Adding model 'Request'
        db.create_table('voice_request', (
            ('description', self.gf('django.db.models.fields.TextField')(max_length=140)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('created', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(default='V', max_length=1)),
            ('votes_needed', self.gf('django.db.models.fields.IntegerField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('voice', ['Request'])

        # Deleting model 'Feature'
        db.delete_table('voice_feature')

        # Adding field 'Vote.request'
        db.add_column('voice_vote', 'request', self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='votes', to=orm['voice.Request']), keep_default=False)

        # Deleting field 'Vote.feature'
        db.delete_column('voice_vote', 'feature_id')

        # Adding unique constraint on 'Vote', fields ['voter', 'request']
        db.create_unique('voice_vote', ['voter', 'request_id'])


    models = {
        'voice.feature': {
            'Meta': {'object_name': 'Feature'},
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '140'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'V'", 'max_length': '1'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'votes_needed': ('django.db.models.fields.IntegerField', [], {})
        },
        'voice.vote': {
            'Meta': {'unique_together': "(('feature', 'voter'),)", 'object_name': 'Vote'},
            'feature': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'votes'", 'to': "orm['voice.Feature']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'used_facebook': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'used_twitter': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'voter': ('django.db.models.fields.EmailField', [], {'max_length': '75'})
        }
    }

    complete_apps = ['voice']
