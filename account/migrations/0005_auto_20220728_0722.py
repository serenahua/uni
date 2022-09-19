# Generated by Django 3.1.4 on 2022-07-28 07:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20220728_0721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chickenexpense',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='homeexpense',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='hotpotexpense',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='hotpotincome',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
