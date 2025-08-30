from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.forms import BaseInlineFormSet
from django_admin_inline_paginator_plus.admin import TabularInlinePaginated
from django.contrib.admin import site as admin_site

from server.apps.game_area.models import (
    MathExpression,
    MathQuizScoreboard,
    MathSolvedQuizzes,
    MathQuiz,
    MathMultipleChoiceTask,
    MathMultipleChoiceTaskAnswer,
    MathQuizChoiceAnswer,
)
from server.apps.game_area.models.quizzes import MathSolvedExpressions


@admin.register(MathQuizChoiceAnswer)
class MathQuizChoiceAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'answer', 'is_correct_answer')


@admin.register(MathMultipleChoiceTaskAnswer)
class MathMultipleChoiceTaskAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'answer')


class SingleCorrectAnswerFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        correct_count = 0
        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False):
                answer = form.cleaned_data.get('answer')
                if answer and answer.is_correct_answer:
                    correct_count += 1
        if correct_count > 1:
            raise ValidationError('You already have answer marked as correct.')


class MathMultipleChoiceTaskAnswerForm(forms.ModelForm):
    answer = forms.ModelChoiceField(queryset=MathQuizChoiceAnswer.objects.none())

    class Meta:
        model = MathMultipleChoiceTaskAnswer
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        used_answers = MathMultipleChoiceTaskAnswer.objects.values_list('answer_id', flat=True)
        available_answers = MathQuizChoiceAnswer.objects.exclude(id__in=used_answers)

        if self.instance.pk and self.instance.answer:
            available_answers = MathQuizChoiceAnswer.objects.filter(
                Q(id__in=available_answers.values_list('pk', flat=True)) | Q(id=self.instance.answer.pk)
            )

        self.fields['answer'].queryset = available_answers
        rel = self.instance._meta.get_field('answer').remote_field
        self.fields['answer'].widget = RelatedFieldWidgetWrapper(self.fields['answer'].widget, rel, admin_site)


class MathMultipleChoiceTaskAnswerInline(TabularInlinePaginated):
    model = MathMultipleChoiceTaskAnswer
    formset = SingleCorrectAnswerFormSet
    form = MathMultipleChoiceTaskAnswerForm
    per_page = 8


@admin.register(MathMultipleChoiceTask)
class MathMultipleChoiceTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'question')
    inlines = (MathMultipleChoiceTaskAnswerInline,)


@admin.register(MathExpression)
class MathExpressionAdmin(admin.ModelAdmin):
    list_display = ('id', 'latex_expression')
    readonly_fields = ('has_multiple_choices',)


class MathExpressionInline(TabularInlinePaginated):
    model = MathExpression
    per_page = 8


@admin.register(MathQuiz)
class MathQuizAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'difficulty', 'finish_score_reward')
    readonly_fields = ('average_solve_time_statistic',)
    inlines = (MathExpressionInline,)


class MathSolvedQuizzesInline(admin.TabularInline):
    model = MathSolvedQuizzes


class MathSolvedExpressionsInline(admin.TabularInline):
    model = MathSolvedExpressions


@admin.register(MathQuizScoreboard)
class MathQuizScoreboardAdmin(admin.ModelAdmin):
    list_display = ('id', 'solved_by', 'board_score')
    inlines = (MathSolvedQuizzesInline, MathSolvedExpressionsInline)
