# Generated by Django 3.2.11 on 2022-02-13 21:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0003_question_code_relation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='question',
            new_name='title',
        ),
        migrations.RemoveField(
            model_name='question',
            name='code',
        ),
    ]
