# Generated by Django 5.0.10 on 2025-02-16 16:04

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    replaces = [
        ("forum", "0001_initial"),
        ("forum", "0002_initial"),
        ("forum", "0003_remove_post_categories_delete_category_and_more"),
        ("forum", "0004_alter_post_categories"),
        ("forum", "0005_postcategory_remove_post_categories_post_categories"),
        ("forum", "0006_post_slug_alter_post_content_alter_post_title"),
    ]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "category_name",
                    models.CharField(max_length=100, verbose_name="category_name"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=85, verbose_name="title")),
                ("content", models.TextField(max_length=2000, verbose_name="content")),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "modified_at",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("post_views", models.IntegerField(blank=True, default=0, null=True)),
                (
                    "categories",
                    models.ManyToManyField(
                        db_index=True,
                        related_name="post_categories",
                        to="forum.category",
                    ),
                ),
                (
                    "post_dislikes",
                    models.ManyToManyField(
                        db_index=True,
                        related_name="disliked_posts",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "post_likes",
                    models.ManyToManyField(
                        db_index=True,
                        related_name="liked_posts",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "post",
                "verbose_name_plural": "posts",
                "ordering": ("title",),
                "get_latest_by": "created_at",
            },
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("comment", models.TextField(max_length=2000, verbose_name="comment")),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("modified_at", models.DateTimeField(default=None, null=True)),
                (
                    "dislikes",
                    models.ManyToManyField(
                        default=0,
                        related_name="disliked_comments",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "likes",
                    models.ManyToManyField(
                        default=0,
                        related_name="liked_comments",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="forum.post"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddIndex(
            model_name="post",
            index=models.Index(
                fields=["created_at"], name="forum_post_created_d558d2_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="post",
            index=models.Index(
                fields=["modified_at"], name="forum_post_modifie_02ef33_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="post",
            index=models.Index(
                fields=["post_views"], name="forum_post_post_vi_6d1b3b_idx"
            ),
        ),
        migrations.RemoveField(
            model_name="post",
            name="categories",
        ),
        migrations.DeleteModel(
            name="Category",
        ),
        migrations.CreateModel(
            name="PostCategory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        choices=[
                            ("GF", "Graph Functions"),
                            ("MT", "Matrices"),
                            ("RV", "Equations"),
                            ("NR", "Inequalities"),
                            ("SM", "Systems of Equations"),
                            ("VM", "Higher Mathematics"),
                            ("TY", "Probability Theory"),
                            ("KM", "Combinatorics"),
                            ("DM", "Discrete Mathematics"),
                            ("PM", "Elementary Mathematics"),
                            ("VD", "Percentages"),
                            ("TG", "Trigonometry"),
                            ("GM", "Geometry"),
                            ("YS", "Probability and Statistics"),
                            ("AL", "Algorithms"),
                            ("AG", "Algebra"),
                            ("IN", "Other"),
                        ],
                        max_length=100,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="post",
            name="categories",
            field=models.ManyToManyField(related_name="posts", to="forum.postcategory"),
        ),
        migrations.AddField(
            model_name="post",
            name="slug",
            field=models.SlugField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="post",
            name="content",
            field=models.TextField(max_length=2000),
        ),
        migrations.AlterField(
            model_name="post",
            name="title",
            field=models.CharField(max_length=85),
        ),
    ]
