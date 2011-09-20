from django.contrib import admin

from voice.models import Request, Vote

class RequestAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)

class VoteAdmin(admin.ModelAdmin):
    readonly_fields = ('request', 'used_facebook', 'used_twitter', 'voter',)

admin.site.register(Vote, VoteAdmin)
admin.site.register(Request, RequestAdmin)
