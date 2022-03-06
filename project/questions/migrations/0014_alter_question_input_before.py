# Generated by Django 3.2.11 on 2022-02-19 21:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0013_alter_question_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='input_before',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='related_inputs', to='questions.question', verbose_name='Entrada anterior'),
        ),
    ]