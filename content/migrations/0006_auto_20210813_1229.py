# Generated by Django 3.2.5 on 2021-08-13 03:29

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0005_auto_20210807_2039'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studytime',
            name='text',
        ),
        migrations.CreateModel(
            name='Timer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxLengthValidator(1440)], verbose_name='勉強時間')),
                ('category', models.CharField(max_length=20, verbose_name='分類')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('auth', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
