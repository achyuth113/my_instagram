# Generated by Django 2.0.5 on 2018-07-18 06:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20180718_1137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='followers',
            name='follower_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.profile'),
        ),
    ]