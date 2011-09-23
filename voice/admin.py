from django.contrib import admin

from voice.models import Feature, Vote

class FeatureAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)

class VoteAdmin(admin.ModelAdmin):
    readonly_fields = ('feature', 'used_facebook', 'used_twitter', 'voter',)

admin.site.register(Vote, VoteAdmin)
admin.site.register(Feature, FeatureAdmin)
