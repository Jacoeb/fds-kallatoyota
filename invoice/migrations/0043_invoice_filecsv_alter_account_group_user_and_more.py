# Generated by Django 4.1.1 on 2022-10-02 06:31

from django.db import migrations, models
import invoice.models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0042_invoice_pot_bank'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='filecsv',
            field=models.FileField(blank=True, upload_to=invoice.models.file_path_filecsv),
        ),
        migrations.AlterField(
            model_name='account',
            name='group_user',
            field=models.CharField(choices=[('User Department', 'User Department'), ('User Invoice', 'User Invoice'), ('User Cashier', 'User Cashier'), ('User Payment', 'User Payment'), ('User Payroll', 'User Payroll'), ('User Kompensasi', 'User Kompensasi')], max_length=255),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='status',
            field=models.CharField(choices=[('List Of Claim', 'List Of Claim'), ('Invoice', 'Invoice'), ('MCM', 'MCM'), ('Payment', 'Payment'), ('Kompensasi', 'Kompensasi'), ('Payment Cabang', 'Payment Cabang'), ('Payroll', 'Payroll')], max_length=255, null=True),
        ),
    ]
