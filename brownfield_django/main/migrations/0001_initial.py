# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('startingBudget', models.PositiveIntegerField(default=60000)),
                ('enableNarrative', models.BooleanField(default=True)),
                ('message', models.TextField(default=b'', max_length=255)),
                ('active', models.BooleanField(default=False)),
                ('archive', models.BooleanField(default=False)),
                ('professor', models.ForeignKey(related_name='taught_by', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=255)),
                ('link', models.CharField(default=b'', max_length=255)),
                ('visible', models.BooleanField(default=False)),
                ('course', models.ForeignKey(default=None, blank=True, to='main.Course', null=True, on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.CharField(max_length=16)),
                ('description', models.CharField(max_length=255)),
                ('cost', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Information',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('infoType', models.CharField(default=b'', max_length=255, blank=True)),
                ('internalName', models.CharField(default=b'', max_length=255, blank=True)),
                ('history', models.ForeignKey(default=None, blank=True, to='main.History', null=True, on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PerformedTest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('x', models.IntegerField(default=0)),
                ('y', models.IntegerField(default=0)),
                ('z', models.IntegerField(default=0)),
                ('testDetails', models.CharField(default=b'', max_length=255)),
                ('testNumber', models.IntegerField(default=0)),
                ('paramString', models.CharField(default=b'', max_length=255)),
                ('history', models.ForeignKey(default=None, blank=True, to='main.History', null=True, on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('signed_contract', models.BooleanField(default=False)),
                ('budget', models.PositiveIntegerField(default=65000)),
                ('team_passwd', models.CharField(default=b'', max_length=255, blank=True)),
                ('course', models.ForeignKey(default=None, blank=True, to='main.Course', null=True, on_delete=models.CASCADE)),
                ('user', models.OneToOneField(related_name='team', null=True, default=None, blank=True, to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ['user'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('profile_type', models.CharField(max_length=2, choices=[(b'AD', b'Administrator'), (b'TE', b'Teacher'), (b'ST', b'Student')])),
                ('tmp_passwd', models.CharField(default=b'', max_length=255, blank=True)),
                ('course', models.ForeignKey(default=None, blank=True, to='main.Course', null=True, on_delete=models.CASCADE)),
                ('team', models.ForeignKey(default=None, blank=True, to='main.Team', null=True, on_delete=models.CASCADE)),
                ('user', models.OneToOneField(related_name='profile', to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ['user'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='history',
            name='team',
            field=models.ForeignKey(to='main.Team', on_delete=models.CASCADE),
            preserve_default=True,
        ),
    ]
