# Generated by Django 3.2 on 2023-02-28 17:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_auto_20230228_1616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='title',
            field=models.ForeignKey(help_text='Произведение, к которому относится рейтинг', on_delete=django.db.models.deletion.CASCADE, related_name='rating', to='reviews.title', unique=True, verbose_name='Произведение'),
        ),
    ]
