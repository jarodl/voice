from django.db import models

class Request(models.Model):
    REQUEST_STATES = (
            ('W', 'In-progress'),
            ('F', 'Finished'),
            ('V', 'Needs votes'),
            )
    state = models.CharField(max_length=1, choices=REQUEST_STATES, default='V')
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=140)
    votes_needed = models.IntegerField()
    created = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return self.title

class Vote(models.Model):
    request = models.ForeignKey('Request', related_name='votes')
    voter = models.EmailField()
    used_twitter = models.BooleanField(default=False)
    used_facebook = models.BooleanField(default=False)

    def __unicode__(self):
        return self.voter

    def save(self, *args, **kwargs):
        super(Vote, self).save(*args, **kwargs)
        if self.request.votes_needed <= self.request.votes.count():
            self.request.state = 'W'
            self.request.save()
