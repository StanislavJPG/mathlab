from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Avg, Sum, Count
from django.utils.translation import gettext_lazy as _
from django_lifecycle import LifecycleModel, hook, AFTER_CREATE, AFTER_SAVE
from dynamic_filenames import FilePattern
from slugify import slugify

from server.apps.game_area.choices import (
    MathQuizCategoryChoices,
    MathQuizDifficultyChoices,
    MathQuizScoreboardScoreChoices,
)
from server.apps.game_area.querysets import MathQuizQuerySet
from server.common.mixins.models import UUIDModelMixin, TimeStampedModelMixin


class MathQuizChoiceAnswer(TimeStampedModelMixin):
    answer = models.CharField(max_length=255)
    is_correct_answer = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Math Quiz Choice Question')
        verbose_name_plural = _('Math Quiz Choice Questions')

    def __str__(self):
        return f'{self.answer} | {self.__class__.__name__} | id - {self.pk}'


class MathMultipleChoiceTask(UUIDModelMixin, TimeStampedModelMixin, LifecycleModel):
    math_expression = models.ForeignKey(
        'game_area.MathExpression',
        on_delete=models.CASCADE,
        related_name='multiple_choices_quizzes',
    )
    question = models.TextField()
    answers = models.ManyToManyField(
        'game_area.MathQuizChoiceAnswer',
    )

    class Meta:
        verbose_name = _('Math Multiple Choice Task')
        verbose_name_plural = _('Math Multiple Choice Task')

    def __str__(self):
        return f'{self.question} | {self.__class__.__name__} | id - {self.pk}'

    @hook(AFTER_SAVE)
    def after_save(self):
        if self.math_expression.multiple_choices_quizzes.exists():
            self.math_expression.has_multiple_choices = True
            self.math_expression.save(update_fields=['has_multiple_choices'], skip_hooks=True)


class MathExpression(UUIDModelMixin, TimeStampedModelMixin, LifecycleModel):
    latex_expression = models.TextField()
    has_multiple_choices = models.BooleanField(default=False)

    max_time_to_solve = models.DurationField(verbose_name=_('max time to solve'))
    math_quiz = models.ForeignKey(
        'game_area.MathQuiz',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('Math Quiz'),
        related_name='math_expressions',
    )
    score_reward = models.PositiveSmallIntegerField(verbose_name=_('score reward for the single expression'), default=3)

    class Meta:
        ordering = ('created_at',)
        verbose_name = _('Math Expression')
        verbose_name_plural = _('Math Expressions')

    def __str__(self):
        return f'Expression | {self.__class__.__name__} | id - {self.id}'

    @hook(AFTER_SAVE)
    def after_save(self):
        if self.math_quiz_id:
            max_time = self.math_quiz.math_expressions.aggregate(max_time=Sum('max_time_to_solve'))['max_time']
            self.math_quiz.max_time_to_solve = max_time
            self.math_quiz.save(update_fields=['max_time_to_solve'])

            self.math_quiz.math_expressions_count = MathExpression.objects.filter(math_quiz=self.math_quiz).count()
            self.math_quiz.save(update_fields=['math_expressions_count'])


math_description_image_upload_to = FilePattern(
    filename_pattern='{app_label:.25}/quizzes/math_quiz/{instance.uuid}/image/{uuid:s}{ext}'
)


class MathQuiz(UUIDModelMixin, TimeStampedModelMixin, LifecycleModel):
    math_description_image = models.ImageField(upload_to=math_description_image_upload_to, blank=True, null=True)
    category = models.CharField(verbose_name='math quiz category', choices=MathQuizCategoryChoices, max_length=2)
    difficulty = models.CharField(
        verbose_name=_('difficulty'),
        choices=MathQuizDifficultyChoices,
        max_length=2,
        default=MathQuizDifficultyChoices.NORMAL,
    )
    finish_score_reward = models.PositiveSmallIntegerField(
        verbose_name=_('score reward for quiz finishing'), default=15
    )

    author = models.ForeignKey('theorist.Theorist', on_delete=models.SET_NULL, null=True, blank=True)
    author_name_slug = models.SlugField(max_length=255, blank=True)  # to save history while theorist being deleted

    average_solve_time_statistic = models.DurationField(verbose_name=_('average solve time'), null=True, blank=True)

    max_time_to_solve = models.DurationField(verbose_name=_('max time to solve'))
    math_expressions_count = models.PositiveSmallIntegerField(default=0, blank=True)  # denormilized field

    objects = MathQuizQuerySet.as_manager()

    class Meta:
        ordering = ('created_at',)
        verbose_name = _('Math Quiz')
        verbose_name_plural = _('Math Quizzes')

    def __str__(self):
        return f'Quiz | {self.get_category_display()} | {self.__class__.__name__} | id - {self.id}'

    @hook(AFTER_CREATE)
    def after_create(self):
        self.author_name_slug = slugify(self.author.full_name)
        self.save(update_fields=['author_name_slug'])


class MathSolvedQuizzes(TimeStampedModelMixin, UUIDModelMixin, LifecycleModel):
    math_quiz = models.ForeignKey('game_area.MathQuiz', on_delete=models.CASCADE)
    math_quiz_scoreboard = models.ForeignKey('game_area.MathQuizScoreboard', on_delete=models.CASCADE)
    best_time_taken = models.DurationField(verbose_name=_('best time taken to finish this quiz'), blank=True)

    class Meta:
        verbose_name = _('Math solved quizzes')
        unique_together = (('math_quiz', 'math_quiz_scoreboard'),)

    def clean(self):
        if self.best_time_taken > self.math_quiz.max_time_to_solve:
            raise ValidationError(
                _('You have only %s to successfully finish this quiz.') % self.math_quiz.max_time_to_solve
            )

    @hook(AFTER_SAVE)
    def after_save(self):
        self.collect_solved_quiz_statistics()

    def collect_solved_quiz_statistics(self):
        def average_pass_time(expr):
            return self.__class__.objects.filter(**expr).aggregate(avg_pass_time=Avg('best_time_taken'))[
                'avg_pass_time'
            ]

        is_save_best_time = (
            average_pass_time({'math_quiz_scoreboard': self.math_quiz_scoreboard})
            < self.math_quiz_scoreboard.time_taken_to_solve_quizzes
            if self.math_quiz_scoreboard.time_taken_to_solve_quizzes
            else True
        )  # save only best time of save anyway if there is time_taken_to_solve_quizzes is None
        if is_save_best_time:
            self.math_quiz.average_solve_time_statistic = average_pass_time({'math_quiz': self.math_quiz})
            self.math_quiz_scoreboard.time_taken_to_solve_quizzes = average_pass_time(
                {'math_quiz_scoreboard': self.math_quiz_scoreboard}
            )

            self.math_quiz.save(update_fields=['average_solve_time_statistic'], skip_hooks=True)
            self.math_quiz_scoreboard.save(update_fields=['time_taken_to_solve_quizzes'], skip_hooks=True)

        most_popular_category = (
            self.math_quiz_scoreboard.solved_quizzes.values_list('category', flat=True)
            .annotate(most_popular_categories=Count('category'))
            .order_by('-most_popular_categories')[0]
        )
        self.math_quiz_scoreboard.most_popular_quiz_type = most_popular_category
        self.math_quiz_scoreboard.save(update_fields=['most_popular_quiz_type'], skip_hooks=True)


# class MathSolvedExpressions(TimeStampedModelMixin, UUIDModelMixin, LifecycleModel):
#     pass


class MathQuizScoreboard(UUIDModelMixin, TimeStampedModelMixin, LifecycleModel):
    solved_expressions = models.ManyToManyField(
        'game_area.MathExpression', blank=True
    )  # TODO: Add through model like in `solved_quizzes`. Because we need to watch board_score in that model.

    solved_quizzes = models.ManyToManyField('game_area.MathQuiz', through='game_area.MathSolvedQuizzes', blank=True)

    solved_by = models.ForeignKey('theorist.Theorist', on_delete=models.SET_NULL, null=True, blank=True)
    solved_by_name_slug = models.SlugField(max_length=255, blank=True)  # to save history while theorist being deleted

    most_popular_quiz_type = models.CharField(max_length=2, choices=MathQuizCategoryChoices)
    time_taken_to_solve_quizzes = models.DurationField(
        verbose_name=_('time that was taken to solve all quizzes'), blank=True, null=True
    )
    board_score = models.CharField(
        choices=MathQuizScoreboardScoreChoices, default=MathQuizScoreboardScoreChoices.EMPTY, max_length=2
    )

    class Meta:
        ordering = ('created_at',)
        verbose_name = _('Math Scoreboard')
        verbose_name_plural = _('Math Scoreboards')

    def __str__(self):
        return f'Quiz Scoreboard | {self.solved_by_name_slug} | {self.__class__.__name__} | id - {self.id}'

    @hook(AFTER_CREATE)
    def after_create(self):
        self.solved_by_name_slug = slugify(self.solved_by.full_name)
        self.save(update_fields=['solved_by_name_slug'])
