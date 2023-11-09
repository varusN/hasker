import re

from django.conf import settings

from django import forms

from .models import Answer, Question, VOTES

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ("text",)

class QuestionForm(forms.ModelForm):
    tags = forms.CharField(max_length=512, required=False)

    class Meta:
        model = Question
        fields = ("description", "subject")

    def clean_tags(self):
        raw_tags = self.cleaned_data["tags"]
        raw_tags, _ = re.subn(r"\s+", " ", raw_tags)

        tags = (tag.strip().lower() for tag in raw_tags.split(","))
        tags = set(filter(bool, tags))

        if len(tags) > settings.QUESTIONS_MAX_TAGS:
            raise forms.ValidationError(f"The maximum number of tags is {settings.QUESTIONS_MAX_TAGS}.")

        if any(len(tag) > settings.QUESTIONS_TAGS_LENGTH for tag in tags):
            raise forms.ValidationError(f"Max tag lenght {settings.QUESTIONS_TAGS_LENGTH} characters.")

        return sorted(tags)

class VoteForm(forms.Form):
    target_id = forms.IntegerField()
    value = forms.TypedChoiceField(choices=VOTES, coerce=int)

    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop("model")
        super().__init__(*args, **kwargs)

    def clean_target_id(self):
        target_id = self.cleaned_data["target_id"]

        try:
            target = self.model.objects.get(pk=target_id)
        except ObjectDoesNotExist:
            raise forms.ValidationError("Target object doesn't exist.")

        self.cleaned_data["target"] = target
        return target_id