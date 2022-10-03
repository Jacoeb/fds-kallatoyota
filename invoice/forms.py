from dataclasses import fields
from faulthandler import disable
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *


class BankFormDetail(ModelForm):
    class Meta:
        model = Bank
        fields = (
            'invoice',
            'no_rekening',
            'nama_rekening',
            'nama_bank',
            'nominal',
        )
        widgets = {
            'invoice': forms.TextInput(
                attrs={
                    'type': 'hidden',
                }
            ),
            'no_rekening': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'nama_rekening': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'nama_bank': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'nominal': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
        }
    # fields = ['no_rekening','nama_rekening','nama_bank']
    # def __init__(self, *args, **kwargs):
    #     super(BankFormDetail, self).__init__(*args, **kwargs)
    #     for key,val in self.fields.items():
    #         val.widget.attrs.update({'class':'form-control'})


class AdminBankDetail(ModelForm):
    class Meta:
        model = Bank
        fields = (
            'biaya_admin',
            'total_bayar',
        )
        widgets = {
            'biaya_admin': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            # 'total_bayar': forms.TextInput(
            #     attrs={
            #         'type': 'hidden',
            #     }
            # ),
        }


class InvoiceForm(ModelForm):
    class Meta:
        model = Invoice
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(InvoiceForm, self).__init__(*args, **kwargs)
        for key, val in self.fields.items():
            val.widget.attrs.update({'class': 'form-control'})

        # self.fields['no_invoice'].widget.attrs.update({'class': 'form-control'})


class InvoiceFormUser(ModelForm):
    class Meta:
        model = Invoice
        fields = ('no_invoice',
                  'nama_vendor',
                  'no_pr',
                  'deskripsi',
                  'attachment',
                  'email',
                  'user',
                  'status',
                  )
        widgets = {
            'user': forms.TextInput(
                attrs={
                    'type': 'hidden',
                    # 'class':'form-control',
                }
            ),
            'no_invoice': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'nama_vendor': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'no_pr': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'deskripsi': forms.Textarea(
                attrs={
                    'class': 'form-control',
                }
            ),
            'attachment': forms.FileInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'status': forms.TextInput(
                attrs={
                    'type': 'hidden',
                    'value': 'List Of Claim',
                }
            ),

        }

    # def __init__(self, *args, **kwargs):
    #     super(InvoiceFormUser, self).__init__(*args, **kwargs)

    #     self.fields['no_invoice'].widget.attrs.update({'class': 'form-control'})
    #     self.fields['nama_vendor'].widget.attrs.update({'class': 'form-control'})
    #     self.fields['deskripsi'].widget.attrs.update({'class': 'form-control'})
    #     self.fields['attachment'].widget.attrs.update({'class': 'form-control'})
    #     self.fields['user'].widget.attrs.update({'class': 'form-control','disabled':'disabled'})


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name', 'password1', 'password2']
        # fields = ['username', 'email', 'password1', 'password2']


class NominalPostForm(ModelForm):
    class Meta:
        model = Invoice
        fields = (
            'nominal',
            'estimasi_bayar',
        )
        widgets = {
            'nominal': forms.TextInput(
                attrs={
                    'type': 'hidden',
                }
            ),
            'estimasi_bayar': forms.TextInput(
                attrs={
                    'type': 'hidden',
                }
            ),
        }


class TipePostForm(ModelForm):
    class Meta:
        model = Invoice
        fields = (
            'tipe',
            'pot_pajak',
            # 'kompensasi',
            'invoice_date',
            'jenis',
            'no_payment',
            'payment_date',
            'buktitransfer',
        )
        widgets = {
            'tipe': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'jenis': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'pot_pajak': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'no_payment': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'buktitransfer': forms.FileInput(
                attrs={
                    'class': 'form-control',
                    'required': 'required',
                }
            ),
            # 'kompensasi': forms.CheckboxInput(
            #     attrs={
            #         'class': 'form-control',
            #     }
            # ),
            'invoice_date': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Pilih Tanggal Invoice',
                    'type': 'date',
                    'required': 'required',
                }
            ),
            'payment_date': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Pilih Tanggal Invoice',
                    'type': 'date',
                    'required': 'required',
                }
            ),
        }


class InvoiceFormAdmin(ModelForm):
    class Meta:
        model = Invoice
        fields = ('no_invoice',
                  'nama_vendor',
                  'site_vendor',
                  'no_pr',
                  'deskripsi',
                  'attachment',
                  'user',
                  'status',
                  )
        widgets = {
            'user': forms.Select(
                attrs={
                    # 'type': 'hidden',
                    'class': 'form-control',
                }
            ),
            'no_invoice': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'nama_vendor': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'site_vendor': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'no_pr': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'deskripsi': forms.Textarea(
                attrs={
                    'class': 'form-control',
                }
            ),
            'attachment': forms.FileInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'status': forms.TextInput(
                attrs={
                    'type': 'hidden',
                    'class': 'form-control',
                }
            ),

        }

    # def __init__(self, *args, **kwargs):
    #     super(InvoiceFormUser, self).__init__(*args, **kwargs)

    #     self.fields['no_invoice'].widget.attrs.update({'class': 'form-control'})
    #     self.fields['nama_vendor'].widget.attrs.update({'class': 'form-control'})
    #     self.fields['deskripsi'].widget.attrs.update({'class': 'form-control'})
    #     self.fields['attachment'].widget.attrs.update({'class': 'form-control'})
    #     self.fields['user'].widget.attrs.update({'class': 'form-control','disabled':'disabled'})


class postPaymentForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = (
            'no_payment',
            'payment_date',
            'payment_create_date',
            'buktitransfer',
            'status',
        )
        widgets = {
            'payment_date': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Pilih Tanggal Invoice',
                    'type': 'date',
                    'required': 'required',
                }
            ),
            'buktitransfer': forms.FileInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'no_payment': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'payment_create_date': forms.TextInput(
                attrs={
                    'type': 'hidden',
                }
            ),
        }
