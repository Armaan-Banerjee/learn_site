from django import forms
from .models import Tags

class create_new_page(forms.Form):

    def __init__(self, *args, **kwargs):
        super(create_new_page, self).__init__(*args, **kwargs)
        self.fields['tags'].choices = Tags.set_all()

    title = forms.CharField(max_length=255, help_text="please enter the title of this page")
    data = forms.CharField(widget=forms.Textarea)
    OPTIONS = Tags.set_all()
    tags = forms.MultipleChoiceField(help_text="Please enter the name for this tag", widget=forms.CheckboxSelectMultiple,
    choices=OPTIONS, required=False)

class add_tags_to_page(forms.Form):
    page = forms.UUIDField()
    OPTIONS = Tags.set_all()
    tags = forms.MultipleChoiceField(help_text="Please enter the name for this tag", widget=forms.CheckboxSelectMultiple,
    choices=OPTIONS)

class create_new_tag(forms.Form):
    name = forms.CharField(max_length=255, help_text="please enter name of tag")
    details = forms.CharField(widget=forms.Textarea, required=False)
    
class edit_tag(forms.Form):
    name = forms.CharField(max_length=255, help_text="please enter name of tag")
    details = forms.CharField(widget=forms.Textarea, required=False)

class create_comment(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    page_id = forms.UUIDField()
    user_id = forms.UUIDField()