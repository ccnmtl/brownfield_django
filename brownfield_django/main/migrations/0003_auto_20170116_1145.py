# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-16 16:45
from __future__ import unicode_literals

from django.db import migrations

from brownfield_django.main.document_links import all_documents


def update_document_links(apps, schema_editor):
    Document = apps.get_model('main', 'Document')

    for doc in all_documents:
        qs = Document.objects.filter(name=doc['name'])
        qs.update(link=doc['link'])


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_userprofile_archive'),
    ]

    operations = [
        migrations.RunPython(update_document_links),
    ]
