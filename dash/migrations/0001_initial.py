# Generated by Django 4.0 on 2022-01-24 18:49

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Absence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('child', models.IntegerField()),
                ('from_date', models.DateTimeField()),
                ('to_date', models.DateTimeField()),
                ('comment', models.TextField()),
                ('approved', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='CheckIn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.IntegerField()),
                ('time', models.DateTimeField(default=datetime.datetime.now)),
                ('comment', models.TextField()),
                ('type', models.CharField(default='Tardy Unexcused', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='CheckOut',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.IntegerField()),
                ('time_out', models.DateTimeField(default=datetime.datetime.now)),
                ('time_back', models.DateTimeField(blank=True)),
                ('comment', models.TextField()),
                ('type', models.CharField(default='Tardy Unexcused', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
        migrations.CreateModel(
            name='SkyUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.BigIntegerField(db_index=True, primary_key=True, serialize=False)),
                ('email', models.EmailField(db_index=True, max_length=255, unique=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('preferred_name', models.CharField(max_length=100)),
                ('student_id', models.IntegerField(blank=True, db_index=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='NurseApproval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=50)),
                ('approval', models.BooleanField(default=False)),
                ('absenence_code', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='nurse_approval', to='dash.absence')),
            ],
        ),
        migrations.CreateModel(
            name='HeadApproval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school_division', models.CharField(choices=[('US', 'Upper School'), ('MS', 'Middle School')], max_length=2)),
                ('approval', models.BooleanField(default=False)),
                ('absenence_code', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='head_approval', to='dash.absence')),
            ],
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_text', models.CharField(max_length=200)),
                ('votes', models.IntegerField(default=0)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dash.question')),
            ],
        ),
        migrations.AddField(
            model_name='absence',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='planned_absences', to='dash.skyuser'),
        ),
    ]
