# Generated by Django 4.1.1 on 2022-09-25 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0027_invoice_invoice_date_alter_invoice_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='jenis',
            field=models.CharField(choices=[('Kompensasi', 'Kompensasi'), ('Payment Cabang', 'Payment Cabang')], max_length=255, null=True),
        ),
    ]
