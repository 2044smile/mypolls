from django import forms

# from polls.custom_layout_object import Formset

from polls.models import Choice, Question, Comment


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_title','question_text',]


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['question','choice_title','choice_text']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_user','comment_password','comment_body']