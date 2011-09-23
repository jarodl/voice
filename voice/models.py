from django.db import models

class Feature(models.Model):
    FEATURE_STATES = (
            ('W', 'In-progress'),
            ('F', 'Finished'),
            ('V', 'Needs votes'),
            )
    state = models.CharField(max_length=1, choices=FEATURE_STATES, default='V')
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=140)
    votes_needed = models.IntegerField()
    created = models.DateField(auto_now_add=True)

    def votes_left(self):
        votes_left = self.votes_needed - len(self.votes.all())
        if votes_left >= 0:
            return votes_left
        else:
            return 0

    def total_votes(self):
        return len(self.votes.all())

    def __unicode__(self):
        return self.title

class Vote(models.Model):
    feature = models.ForeignKey('Feature', related_name='votes')
    voter = models.EmailField()
    used_twitter = models.BooleanField(default=False)
    used_facebook = models.BooleanField(default=False)

    class Meta:
        unique_together = (('feature', 'voter'),)

    def __unicode__(self):
        return self.voter

    def save(self, *args, **kwargs):
        super(Vote, self).save(*args, **kwargs)
        self.feature.save()
        if self.feature.votes_left() == 0:
            self.feature.state = 'W'
            self.feature.save()
