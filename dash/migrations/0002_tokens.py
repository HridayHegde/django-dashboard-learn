# Generated by Django 3.2.4 on 2021-07-07 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dash', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='tokens',
            fields=[
                ('tokenid', models.AutoField(primary_key=True, serialize=False)),
                ('token_owner', models.CharField(max_length=400)),
            ],
        ),
    ]