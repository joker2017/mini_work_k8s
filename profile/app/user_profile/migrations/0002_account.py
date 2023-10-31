# Generated by Django 4.2.5 on 2023-10-31 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.CharField(blank=True, editable=False, max_length=20, primary_key=True, serialize=False, unique=True)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
            ],
            options={
                'db_table': 'account_account',
                'managed': False,
            },
        ),
    ]
