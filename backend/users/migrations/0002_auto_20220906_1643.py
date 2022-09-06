# Generated by Django 2.2.16 on 2022-09-06 13:43

from django.db import migrations, models
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='customuser',
            constraint=models.UniqueConstraint(fields=('subscribed_from_customuser_id', 'subscribed_to_customuser_id'), name='unique_user_subscribers'),
        ),
        migrations.AddConstraint(
            model_name='customuser',
            constraint=models.CheckConstraint(check=models.Q(_negated=True, subscribed_from_customuser_id=django.db.models.expressions.F('subscribed_to_customuser_id')), name='check_not_loop_user_subscribed'),
        ),
    ]