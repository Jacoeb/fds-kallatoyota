# Generated by Django 4.1.1 on 2022-09-27 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0037_invoice_estimasi_bayar'),
    ]

    operations = [
        migrations.AddField(
            model_name='bank',
            name='potongan',
            field=models.FloatField(default=0, max_length=255, null=True),
        ),
    ]
