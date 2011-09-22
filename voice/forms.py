from django.forms import ModelForm
from voice.models import Vote

class VoteForm(ModelForm):

    class Meta:
        model = Vote
        exclude = ('request', 'used_twitter', 'used_facebook',)
