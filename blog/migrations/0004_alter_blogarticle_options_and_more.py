# Generated by Django 5.1.4 on 2025-02-24 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_blogarticle_number_views'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogarticle',
            options={'ordering': ['create_at'], 'permissions': [('can_publish_article', 'Публикация статьи блога')], 'verbose_name': 'Статья', 'verbose_name_plural': 'Статьи'},
        ),
        migrations.AlterField(
            model_name='blogarticle',
            name='published',
            field=models.BooleanField(default=False, verbose_name='Опубликована'),
        ),
    ]
