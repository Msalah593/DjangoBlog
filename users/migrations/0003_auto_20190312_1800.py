# Generated by Django 2.0.7 on 2019-03-12 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20190216_1910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='is_active',
            field=models.BooleanField(default=False, help_text='Designates whether this \n                                        user should be treated as\n                                        active. Unselect this instead\n                                        of deleting accounts.', verbose_name='active'),
        ),
    ]
