from django import forms 
from info.models import Tags

class CreateFlashCardTags(forms.Form):
    OPTIONS = Tags.set_all()
    tags = forms.MultipleChoiceField(help_text="Please enter the name for this tag", widget=forms.CheckboxSelectMultiple,
    choices=OPTIONS)
    