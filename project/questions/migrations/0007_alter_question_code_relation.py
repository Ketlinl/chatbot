# Generated by Django 3.2.11 on 2022-02-14 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0006_alter_question_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='code_relation',
            field=models.CharField(help_text='ID da questão anterior a essa no fluxo de respostas do chatbot.', max_length=15, verbose_name='Pergunta anterior'),
        ),
    ]