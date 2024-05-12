# Generated by Django 5.0.3 on 2024-05-11 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ta_app', '0002_skill_course_required_skills_user_skills'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='skills',
        ),
        migrations.RemoveField(
            model_name='course',
            name='required_skills',
        ),
        migrations.AddField(
            model_name='user',
            name='backend_skill',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='discrete_math_skill',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='frontend_skill',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='java_skill',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='python_skill',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='scala_skill',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='Skill',
        ),
    ]