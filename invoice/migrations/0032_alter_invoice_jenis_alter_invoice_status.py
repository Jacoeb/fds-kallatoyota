# Generated by Django 4.1.1 on 2022-09-26 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0031_invoice_bukti_transfer_alter_invoice_attachment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='jenis',
            field=models.CharField(blank=True, choices=[('Kompensasi', 'Kompensasi'), ('Payment Cabang', 'Payment Cabang'), ('Payroll', 'Payroll')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='status',
            field=models.CharField(choices=[('List Of Claim', 'List Of Claim'), ('Invoice', 'Invoice'), ('MCM', 'MCM'), ('Payment', 'Payment'), ('Payment Cabang', 'Payment Cabang'), ('Payroll', 'Payroll')], max_length=255, null=True),
        ),
    ]
