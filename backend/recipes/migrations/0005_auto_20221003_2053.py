# Generated by Django 2.2.16 on 2022-10-03 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_auto_20220927_1931'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.CharField(help_text='Required. Enter name recipe, please.', max_length=200, verbose_name='name'),
        ),
    ]
