from django.contrib import admin

from server.apps.game_area.models import MathExpression, MathQuizScoreboard, MathQuiz
from server.apps.game_area.models.quizzes import MathSolvedQuizzes


@admin.register(MathExpression)
class MathExpressionAdmin(admin.ModelAdmin):
    list_display = ('id', 'latex_expression')


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
