from django.contrib import admin

from server.apps.game_area.models import (
    MathExpression,
    MathQuizScoreboard,
    MathSolvedQuizzes,
    MathQuiz,
    MathQuizChoiceAnswer,
    MathMultipleChoiceTask,
)


@admin.register(MathQuizChoiceAnswer)
class MathQuizChoiceAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'answer', 'is_correct_answer')


@admin.register(MathMultipleChoiceTask)
class MathMultipleChoiceTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'question')


@admin.register(MathExpression)
class MathExpressionAdmin(admin.ModelAdmin):
    list_display = ('id', 'latex_expression')
    readonly_fields = ('has_multiple_choices',)


@admin.register(MathQuiz)
class MathQuizAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'difficulty', 'finish_score_reward')
    readonly_fields = ('average_solve_time_statistic', 'math_expressions_count')


class MathQuizScoreboardInline(admin.TabularInline):
    model = MathSolvedQuizzes


@admin.register(MathQuizScoreboard)
class MathQuizScoreboardAdmin(admin.ModelAdmin):
    list_display = ('id', 'solved_by', 'board_score')
    inlines = (MathQuizScoreboardInline,)
