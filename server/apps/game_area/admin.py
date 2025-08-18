from django.contrib import admin

from server.apps.game_area.models import MathExpression, MathQuizScoreboard, MathQuiz


@admin.register(MathExpression)
class MathExpressionAdmin(admin.ModelAdmin):
    list_display = ('id', 'latex_expression')


@admin.register(MathQuiz)
class MathQuizAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'difficulty', 'finish_score_reward')


@admin.register(MathQuizScoreboard)
class MathQuizScoreboardAdmin(admin.ModelAdmin):
    list_display = ('id', 'solved_by', 'board_score')
