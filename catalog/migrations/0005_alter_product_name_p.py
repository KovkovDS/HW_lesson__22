# Generated by Django 5.1.4 on 2024-12-26 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_alter_product_name_p'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='name_p',
            field=models.CharField(max_length=150, unique=True, verbose_name='Наименование'),
        ),
    ]