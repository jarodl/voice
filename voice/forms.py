from django.forms import ModelForm, ValidationError
from voice.models import Vote

class VoteForm(ModelForm):

    class Meta:
        model = Vote
        exclude = ('used_twitter', 'used_facebook',)

    def clean(self):
        cleaned_data = self.cleaned_data
        request_id = cleaned_data.get('request')
        voter = cleaned_data.get('voter')

        vote = Vote.objects.filter(request=request_id, voter=voter)
        if vote.exists():
            error = '%s has already voted on this request' % voter
            self._errors['request'] = self._errors.get('request', [])
            self._errors['request'].append(error)
            raise ValidationError(error)

        return cleaned_data
