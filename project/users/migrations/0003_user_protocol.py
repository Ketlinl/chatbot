# Generated by Django 3.2.11 on 2022-02-13 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='protocol',
            field=models.CharField(default='', error_messages={'unique': 'Protocolo já existe.'}, help_text='Protocolo do chatbot do usuário', max_length=25, unique=True, verbose_name='protocolo'),
            preserve_default=False,
        ),
    ]
