# Generated by Django 4.2.7 on 2023-12-07 00:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SQLMODEL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_column', models.DateField(blank=True, null=True)),
                ('trade_code_column', models.CharField(blank=True, max_length=100, null=True)),
                ('high_column', models.DecimalField(decimal_places=1, max_digits=200)),
                ('low_column', models.DecimalField(decimal_places=1, max_digits=200)),
                ('open_column', models.DecimalField(decimal_places=1, max_digits=200)),
                ('close_column', models.DecimalField(decimal_places=1, max_digits=200)),
                ('volume_column', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
    ]
