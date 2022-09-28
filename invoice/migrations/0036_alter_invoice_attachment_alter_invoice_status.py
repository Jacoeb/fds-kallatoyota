# Generated by Django 4.1.1 on 2022-09-27 05:43

from django.db import migrations, models
import invoice.models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0035_invoice_invoice_create_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='attachment',
            field=models.FileField(blank=True, upload_to=invoice.models.file_path),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='status',
            field=models.CharField(choices=[('List Of Claim', 'List Of Claim'), ('Invoice', 'Invoice'), ('MCM', 'MCM'), ('Payment', 'Payment'), ('Kompensasi', 'Kompensasi'), ('Payment Cabang', 'Payment Cabang')], max_length=255, null=True),
        ),
    ]
