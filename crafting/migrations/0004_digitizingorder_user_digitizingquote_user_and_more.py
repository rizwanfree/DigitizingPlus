# Generated by Django 5.1.6 on 2025-04-12 03:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crafting', '0003_digitizingquote_patchquote_vectorquote_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='digitizingorder',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='digitizing_orders', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='digitizingquote',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='digitizing_quotes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='patchorder',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='patch_orders', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='patchquote',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='patch_quotes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='vectororder',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vector_orders', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='vectorquote',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vector_quotes', to=settings.AUTH_USER_MODEL),
        ),
    ]
