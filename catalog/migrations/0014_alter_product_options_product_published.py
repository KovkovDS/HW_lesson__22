# Generated by Django 5.1.4 on 2025-02-22 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0013_alter_product_picture'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['updated_at', 'name_p'], 'permissions': [('can_unpublish_product', 'Снятие продукта с публикации')], 'verbose_name': 'Продукт', 'verbose_name_plural': 'Продукты'},
        ),
        migrations.AddField(
            model_name='product',
            name='published',
            field=models.BooleanField(default=False, verbose_name='Опубликован'),
        ),
    ]
