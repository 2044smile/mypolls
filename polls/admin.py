from django.contrib import admin
from .models import Question, Choice, Comment


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3
    list_display = ['choice_text']


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_title', 'question_text']
    fieldsets = [
        (None,     {'fields': ['question_title','question_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    inlines = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Comment)
