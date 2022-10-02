from django.db import models
import os
from django.contrib.auth.models import User

# Create your models here.


def file_path(instance, filename):
    path = "documents/"
    format = "attachment-" + filename
    return os.path.join(path, format)


def file_path_buktitransfer(instance, filename):
    path = "buktitransfer/"
    format = "buktitransfer-" + filename
    return os.path.join(path, format)


def file_path_filecsv(instance, filename):
    path = "filecsv/"
    format = "filecsv-" + filename
    return os.path.join(path, format)


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group_user = models.CharField(
        max_length=255,
        choices=[
            ('User Department', 'User Department'),
            ('User Invoice', 'User Invoice'),
            ('User Cashier', 'User Cashier'),
            ('User Payment', 'User Payment'),
            ('User Payroll', 'User Payroll'),
            ('User Kompensasi', 'User Kompensasi'),
        ]
    )

    def __str__(self):
        return self.user.username


class Invoice(models.Model):
    STATUS = (
        ('List Of Claim', 'List Of Claim'),
        ('Invoice', 'Invoice'),
        ('MCM', 'MCM'),
        ('Payment', 'Payment'),
        ('Kompensasi', 'Kompensasi'),
        ('Payment Cabang', 'Payment Cabang'),
        ('Payroll', 'Payroll'),
    )

    TIPE = (
        ('Operation', 'Operation'),
        ('Investasi', 'Investasi'),
        ('Pendanaan', 'Pendanaan'),
    )
    JENIS = (
        ('Kompensasi', 'Kompensasi'),
        ('Payment Cabang', 'Payment Cabang'),
        ('Payroll', 'Payroll'),
    )
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    no_invoice = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=255, null=True, choices=STATUS)
    tipe = models.CharField(max_length=255, null=True, choices=TIPE)
    no_pr = models.CharField(max_length=255, null=True, blank=True)
    nama_vendor = models.CharField(max_length=255, null=True)
    deskripsi = models.TextField(null=True, blank=True)
    nominal = models.FloatField(max_length=255, null=True, default=0)
    pot_pajak = models.FloatField(max_length=255, null=True, default=0)
    pot_bank = models.FloatField(max_length=255, null=True, default=0)
    kompensasi = models.BooleanField('Kompensasi', default=False)
    bayar = models.FloatField(max_length=255, null=True, default=0)
    attachment = models.FileField(upload_to=file_path, blank=True)
    jenis = models.CharField(max_length=255, null=True,
                             blank=True, choices=JENIS)
    email = models.EmailField(max_length=255, null=True)
    invoice_date = models.DateField(null=True, blank=True)
    invoice_create_date = models.DateField(null=True, blank=True)
    mcm_date = models.DateField(null=True, blank=True)
    no_payment = models.CharField(max_length=255, null=True, blank=True)
    payment_date = models.DateField(null=True, blank=True)
    payment_create_date = models.DateField(null=True, blank=True)
    buktitransfer = models.FileField(
        upload_to=file_path_buktitransfer, blank=True)
    estimasi_bayar = models.DateField(null=True, blank=True)
    filecsv = models.FileField(
        upload_to=file_path_filecsv, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.no_invoice

    @property
    def get_attachment_url(self):
        if self.attachment and hasattr(self.attachment, 'url'):
            return self.attachment.url

    @property
    def get_buktitransfer_url(self):
        if self.buktitransfer and hasattr(self.buktitransfer, 'url'):
            return self.buktitransfer.url

    @property
    def get_filecsv_url(self):
        if self.filecsv and hasattr(self.filecsv, 'url'):
            return self.filecsv.url


class Department(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True)
    kode = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=255, null=True)
    email = models.EmailField(max_length=255, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Bank(models.Model):
    invoice = models.ForeignKey(Invoice, null=True, on_delete=models.CASCADE)
    no_rekening = models.CharField(max_length=255, null=True)
    nama_rekening = models.CharField(max_length=255, null=True)
    nama_bank = models.CharField(max_length=255, null=True)
    nominal = models.FloatField(max_length=255, null=True)
    biaya_admin = models.FloatField(max_length=255, null=True, default=0)
    total_bayar = models.FloatField(max_length=255, null=True, default=0)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.no_rekening
