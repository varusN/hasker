import re

from django.conf import settings
from django import forms

from .models import Answer, Question


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ("text",)

class QuestionForm(forms.ModelForm):
    tags = forms.CharField(max_length=512, required=False)

    class Meta:
        model = Question
        fields = ("description", "subject", "tags")

    def clean_tags(self):
        raw_tags = self.cleaned_data["tags"]
        raw_tags, _ = re.subn(r"\s+", " ", raw_tags)

        tags = (tag.strip().lower() for tag in raw_tags.split(","))
        tags = set(filter(bool, tags))

        if len(tags) > settings.QUESTIONS_MAX_TAGS:
            print('WTF')
            raise forms.ValidationError(f"The maximum number of tags is {settings.QUESTIONS_MAX_TAGS}.")

        if any(len(tag) > settings.QUESTIONS_TAGS_LENGTH for tag in tags):
            raise forms.ValidationError(f"Max tag lenght {settings.QUESTIONS_TAGS_LENGTH} characters.")
        return sorted(tags)


