# Generated by Django 5.1 on 2024-11-03 11:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userlanguage',
            name='language',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='favorite_language',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='completed_lessons',
        ),
        migrations.RemoveField(
            model_name='userlanguage',
            name='user',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='Email',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='fullName',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='language_level',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='password',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='achievements',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='birthday',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='certificates',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='finishes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='followers',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='following',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='UserAchievement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('date_earned', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='CommunityPost',
        ),
        migrations.DeleteModel(
            name='Language',
        ),
        migrations.DeleteModel(
            name='LessonTag',
        ),
        migrations.DeleteModel(
            name='Lesson',
        ),
        migrations.DeleteModel(
            name='UserLanguage',
        ),
    ]
