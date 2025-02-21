# Generated by Django 5.1.6 on 2025-02-18 22:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('forum', '0014_remove_comment_user_and_more'),
        ('theorist', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='dislikes',
            field=models.ManyToManyField(
                related_name='disliked_comments',
                through='forum.CommentDislike',
                to='theorist.theorist',
            ),
        ),
        migrations.AlterField(
            model_name='comment',
            name='likes',
            field=models.ManyToManyField(
                related_name='liked_comments',
                through='forum.CommentLike',
                to='theorist.theorist',
            ),
        ),
        migrations.AlterField(
            model_name='commentdislike',
            name='theorist',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='comment_dislikes_relations',
                to='theorist.theorist',
            ),
        ),
        migrations.AlterField(
            model_name='commentlike',
            name='theorist',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='comment_likes_relations',
                to='theorist.theorist',
            ),
        ),
        migrations.AlterField(
            model_name='post',
            name='dislikes',
            field=models.ManyToManyField(
                related_name='disliked_posts',
                through='forum.PostDislike',
                to='theorist.theorist',
            ),
        ),
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(
                related_name='liked_posts',
                through='forum.PostLike',
                to='theorist.theorist',
            ),
        ),
        migrations.AlterField(
            model_name='post',
            name='theorist',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='posts',
                to='theorist.theorist',
            ),
        ),
        migrations.AlterField(
            model_name='postdislike',
            name='theorist',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='post_dislikes_relations',
                to='theorist.theorist',
            ),
        ),
        migrations.AlterField(
            model_name='postlike',
            name='theorist',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='post_likes_relations',
                to='theorist.theorist',
            ),
        ),
    ]
