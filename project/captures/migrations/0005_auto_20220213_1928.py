# Generated by Django 3.2.11 on 2022-02-13 22:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('captures', '0004_auto_20220213_1918'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='capture',
            options={'ordering': ('created_at',), 'verbose_name': 'Captura', 'verbose_name_plural': 'Capturas'},
        ),
        migrations.RenameField(
            model_name='capture',
            old_name='cep',
            new_name='zip_code',
        ),
    ]
