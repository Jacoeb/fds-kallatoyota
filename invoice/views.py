from ast import If
from datetime import date
from django.shortcuts import render, redirect
from django.db.models import Sum
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
import datetime


# Create your views here.

from . models import *
from . forms import *
from . decoratos import *


# View Login
@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password is incorrect')
    context = {
        'title': 'Kalla FDS'
    }
    return render(request, 'invoice/login.html', context)


@login_required(login_url='login')
@admin_only
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, 'Account was created for ' + username)
            return redirect('login')

    context = {
        'form': form,
        'title': 'Kalla FDS',
    }
    return render(request, 'invoice/register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


# View User Dept
@login_required(login_url='login')
@allowed_users(allowed_roles=['user_dept'])
def dashboardUser(request):
    department = request.user
    # print ('department:', department)
    invoices = Invoice.objects.all()

    total_invoice = invoices.filter(user=department).count()
    listofclaim = invoices.filter(
        status='List Of Claim', user=department).count()
    invoicing = invoices.filter(status='Invoice', user=department).count()
    mcm = invoices.filter(status='MCM', user=department).count()
    payment = invoices.filter(status='Payment', user=department).count()
    payroll = invoices.filter(status='Payroll', user=department).count()
    total_invoice_payroll = invoicing + payroll
    payment_cabang = invoices.filter(
        status='Payment Cabang', user=department).count()
    payment_kompensasi = invoices.filter(
        status='Payment Kompensasi', user=department).count()
    total_payment = payment + payment_cabang + payment_kompensasi
    context = {
        'invoice': invoices,
        'total_invoice': total_invoice,
        'listofclaim': listofclaim,
        'invoicing': invoicing,
        'mcm': mcm,
        'payment': payment,
        'department': department,
        'total_payment': total_payment,
        'total_invoice_payroll': total_invoice_payroll,
    }
    return render(request, 'invoice/dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['user_dept'])
def listOfClaim(request):
    department = request.user
    invoices = Invoice.objects.all().filter(user=department)
    # bayar = invoices.
    # print('bayar : ', bayar)
    # bank = Bank.objects.all()
    # nominal = bank.aggregate(nominal=Sum('nominal'))

    context = {
        'title': 'List Of Claim',
        'invoice': invoices,
        # 'bayar': bayar,
        # 'nominal': nominal,
    }
    return render(request, 'invoice/list_of_claim.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['user_dept'])
def add_listofclaim(request):
    id = request.user.id
    # print ('user id :', id)
    user_active = User.objects.get(id=id)
    data = {
        'user': user_active.id,
    }
    # print ('user :', data)
    form = InvoiceFormUser(request.POST or None,
                           request.FILES or None, initial=data)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('listofclaim')
    context = {
        'title': 'Tambah List Of Claim',
        'form': form,
    }
    return render(request, 'invoice/invoice_form.html', context)


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['user_dept'])
def update_listofclaim(request, pk):
    invoice = Invoice.objects.get(id=pk)
    lampiran = invoice.attachment
    # print ('lampiran :', lampiran)
    # print ('i :', invoice)
    form = InvoiceFormUser(request.POST or None,
                           request.FILES or None, instance=invoice)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('listofclaim')
    context = {
        'title': 'Update List Of Claim',
        'form': form,
        'lampiran': lampiran,
        'invoice': invoice,
    }
    return render(request, 'invoice/invoice_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['user_dept'])
def detail_listofclaim(request, pk):
    invoices = Invoice.objects.get(id=pk)
    # no_invoice = invoices.no_invoice
    bank = invoices.bank_set.all()
    total_bank = bank.count()
    # print(total_bank)
    if (total_bank >= 1):
        estimasi_bayar = date.today() + datetime.timedelta(days=20)
        data = {
            'estimasi_bayar': estimasi_bayar
        }
        total_potongan = bank.aggregate(biaya_admin=Sum('biaya_admin'))
        values = [float(x) for x in list(total_potongan.values())]
        for value in values:
            pot_bank = value
            bayar = invoices.nominal - invoices.pot_pajak - pot_bank
            nominal = bank.aggregate(nominal=Sum('nominal'))
            form = NominalPostForm(request.POST or None,
                                   instance=invoices, initial=data)
            if request.method == 'POST':
                if form.is_valid():
                    form.save()
                    return redirect('listofclaim')
    else:
        bayar = invoices.nominal - invoices.pot_pajak
        nominal = bank.aggregate(nominal=Sum('nominal'))
        form = NominalPostForm(request.POST or None, instance=invoices)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                return redirect('listofclaim')
    context = {
        'invoice': invoices,
        'bank': bank,
        'total_bank': total_bank,
        'nominal': nominal,
        'form': form,
        'bayar': bayar,
    }
    return render(request, 'invoice/detail_listofclaim.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['user_dept'])
def add_bank(request, pk):
    invoices = Invoice.objects.get(id=pk)
    form = BankFormDetail(initial={'invoice': invoices})
    if request.method == 'POST':
        form = BankFormDetail(request.POST)
        if form.is_valid():
            form.save()
            return redirect('detail_listofclaim', pk)
    context = {
        'title': 'Tambah Bank',
        'invoice': invoices,
        'form': form,
    }
    return render(request, 'invoice/bank_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['user_dept'])
def update_bank(request, pk):
    banks = Bank.objects.get(id=pk)
    invoice = banks.invoice
    id_invoice = Invoice.objects.get(no_invoice=invoice)
    id = id_invoice.id
    form = BankFormDetail(request.POST or None, instance=banks)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('detail_listofclaim', id)
    context = {
        'title': 'Tambah Bank',
        'bank': banks,
        'form': form,
    }
    return render(request, 'invoice/bank_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['user_dept'])
def delete_listofclaim(request, pk):
    Invoice.objects.filter(id=pk).delete()
    return redirect('listofclaim')
# End View Department


# View Admin Invoice
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin_invoice'])
def dashboardInvoice(request):
    department = request.user
    # print ('department:', department)
    invoices = Invoice.objects.all()

    total_invoice = invoices.count()
    listofclaim = invoices.filter(status='List Of Claim').count()
    invoicing = invoices.filter(status='Invoice').count()
    mcm = invoices.filter(status='MCM').count()
    payment = invoices.filter(status='Payment').count()
    payment_cabang = invoices.filter(status='Payment Cabang').count()
    total_payment = payment + payment_cabang
    print(total_payment)
    context = {
        'invoice': invoices,
        'total_invoice': total_invoice,
        'listofclaim': listofclaim,
        'invoicing': invoicing,
        'mcm': mcm,
        'payment': payment,
        'department': department,
        'total_payment': total_payment,
    }
    return render(request, 'invoice/dashboard.html', context)


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['admin_invoice'])
def invoicing(request):
    invoices = Invoice.objects.filter(status='List Of Claim')
    # print ('invoice :',invoice)
    form = TipePostForm()

    context = {
        'invoice': invoices,
        'form': form,
    }
    return render(request, 'invoice/invoice.html', context)


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['admin_invoice'])
def add_invoice_admin(request):
    form = InvoiceFormAdmin(request.POST or None,
                            request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('invoicing')
    context = {
        'title': 'Tambah List Of Claim',
        'form': form,
    }
    return render(request, 'invoice/invoice_form.html', context)


# def post_nominal(request, pk):
#     invoices = Invoice.objects.get(id=pk)
#     form = NominalPostForm(request.POST or None, invoices=invoices)
#     if request.method == 'POST':
#         if form.is_valid():
#             form.save()
#             return redirect('listofclaim')
#     context = {
#         'form' : form,
#     }
#     return render(request, 'invoice/detail_listofclaim.html', context)


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['admin_invoice'])
def update_invoice_admin(request, pk):
    invoice = Invoice.objects.get(id=pk)
    lampiran = invoice.attachment
    # print ('lampiran :', lampiran)
    # print ('i :', invoice)
    form = InvoiceFormAdmin(request.POST or None,
                            request.FILES or None, instance=invoice)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('invoicing')
    context = {
        'title': 'Update List Of Claim',
        'form': form,
        'lampiran': lampiran,
        'invoice': invoice,
    }
    return render(request, 'invoice/invoice_form.html', context)


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['admin_invoice'])
def delete_invoice_admin(request, pk):
    Invoice.objects.filter(id=pk).delete()
    return redirect('invoicing')


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['admin_invoice'])
def post_tipe(request, pk):
    invoice = Invoice.objects.get(id=pk)
    form = TipePostForm(request.POST or None, instance=invoice)
    if request.method == 'POST':
        jenis = request.POST.get('jenis')
        potongan = request.POST.get('pot_pajak')
        today = date.today()
        tipe = request.POST.get('tipe')
        invoice_date = request.POST.get('invoice_date')
        nominal = invoice.nominal
        bayar = float(nominal) - float(potongan)
        print(pk, jenis, potongan, tipe, bayar, invoice_date, today)
        if jenis == 'Payment Cabang':
            Invoice.objects.filter(id=pk).update(
                pot_pajak=potongan, status='Payment Cabang', jenis=jenis, tipe=tipe, bayar=bayar, invoice_date=invoice_date, invoice_create_date=today)
        elif jenis == 'Kompensasi':
            Invoice.objects.filter(id=pk).update(
                pot_pajak=potongan, status='Kompensasi', jenis=jenis, tipe=tipe, bayar=bayar, invoice_date=invoice_date, invoice_create_date=today)
        elif jenis == 'Payroll':
            Invoice.objects.filter(id=pk).update(
                pot_pajak=potongan, status='Payroll', jenis=jenis, tipe=tipe, bayar=bayar, invoice_date=invoice_date, invoice_create_date=today)
        else:
            Invoice.objects.filter(id=pk).update(
                pot_pajak=potongan, status='Invoice', jenis=jenis, tipe=tipe, bayar=bayar, invoice_date=invoice_date, invoice_create_date=today)
        return redirect('invoicing')

        # if form.is_valid():
        #     form.save()
    context = {
        'form': form,
        'invoice': invoice,
        'title': 'Apply & Post Tipe Transaksi',
    }
    return render(request, 'invoice/post_tipe.html', context)


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['admin_invoice'])
def reportInvoice(request):
    context = {
        'title': 'Report Invoice',
    }
    return render(request, 'invoice/report.html', context)


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['admin_invoice'])
def resultInvoice(request):
    tanggal_mulai = request.POST.get('tanggal_mulai')
    tanggal_akhir = request.POST.get('tanggal_akhir')
    invoices = Invoice.objects.filter(
        invoice_create_date__range=[tanggal_mulai, tanggal_akhir])
    # invoice_oracle = invoices.invoice_date
    # print(invoice_oracle)
    context = {
        'title': 'Result Invoice',
        'table_title': 'Daftar Invoice',
        'invoices': invoices,
        'tanggal_mulai': tanggal_mulai,
        'tanggal_akhir': tanggal_akhir,
    }
    return render(request, 'invoice/result.html', context)
# End Admin Invoice


# View Admin Cashier
@ login_required(login_url='login')
@ allowed_users(allowed_roles=['cashier'])
def dashboardCashier(request):
    department = request.user.username
    invoices = Invoice.objects.all()

    total_invoice = invoices.count()
    listofclaim = invoices.filter(status='List Of Claim').count()
    invoicing = invoices.filter(status='Invoice').count()
    mcm = invoices.filter(status='MCM').count()
    payment = invoices.filter(status='Payment').count()
    context = {
        'invoice': invoices,
        'total_invoice': total_invoice,
        'listofclaim': listofclaim,
        'invoicing': invoicing,
        'mcm': mcm,
        'payment': payment,
        'department': department
    }
    return render(request, 'invoice/dashboard.html', context)


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['cashier'])
def mcm(request):
    invoices = Invoice.objects.filter(status='Invoice', kompensasi=False)
    # print ('invoice :',invoice)
    form = TipePostForm()

    context = {
        'invoice': invoices,
        'form': form,
    }
    return render(request, 'invoice/invoice.html', context)


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['cashier'])
def detail_mcm(request, pk):
    invoices = Invoice.objects.get(id=pk)
    # no_invoice = invoices.no_invoice
    bank = invoices.bank_set.all()
    total_bank = bank.count()
    total_potongan = bank.aggregate(biaya_admin=Sum('biaya_admin'))
    values = [float(x) for x in list(total_potongan.values())]
    for value in values:
        pot_bank = value
    bayar = invoices.nominal - invoices.pot_pajak - pot_bank
    nominal = bank.aggregate(nominal=Sum('nominal'))
    # bayar_bank
    # print(total_potongan, nominal, no_invoice, total_bank, pot_bank)
    # form = NominalPostForm(request.POST or None, instance=invoices)
    # if request.method == 'POST':
    #     if form.is_valid():
    #         form.save()
    #         return redirect('mcm')

    context = {
        'invoice': invoices,
        'bank': bank,
        'total_bank': total_bank,
        'nominal': nominal,
        # 'form': form,
        'bayar': bayar,
    }
    return render(request, 'invoice/detail_listofclaim.html', context)


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['cashier'])
def add_biaya_admin(request, pk):
    bank = Bank.objects.get(id=pk)
    invoice_id = bank.invoice
    id = Invoice.objects.get(no_invoice=invoice_id)
    biaya_admin = request.POST.get('biaya_admin')
    # print(id.id, biaya_admin, total_bayar)
    form = AdminBankDetail(request.POST or None, instance=bank)
    if request.method == 'POST':
        admin_bank = biaya_admin
        total_bayar = bank.nominal - float(admin_bank)
        Bank.objects.filter(id=pk).update(
            biaya_admin=admin_bank, total_bayar=total_bayar)
        # if form.is_valid():
        #     form.save()
        # print(id_invoice, potongan, nominal)
        return redirect('detail_mcm', id.id)

        # if form.is_valid():
        #     form.save()
    context = {
        'form': form,
        'invoice': invoice,
        'title': 'Apply & Post Potongan Bank',
    }
    return render(request, 'invoice/post_biaya_admin.html', context)


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['cashier'])
def post_mcm(request, pk):
    invoice = Invoice.objects.get(id=pk)
    bank = invoice.bank_set.all()
    total_potongan = bank.aggregate(biaya_admin=Sum('biaya_admin'))
    values = [float(x) for x in list(total_potongan.values())]
    for value in values:
        pot_bank = value
    nominal = invoice.nominal
    pot_pajak = invoice.pot_pajak
    bayar = nominal - pot_bank - pot_pajak
    mcm_date = date.today()
    # print(nominal, pot_bank, pot_pajak, bayar)
    Invoice.objects.filter(id=pk).update(
        bayar=bayar, status="MCM", mcm_date=mcm_date, pot_bank=pot_bank)
    return redirect('mcm')


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['cashier'])
def reportMCM(request):
    context = {
        'title': 'Report MCM',
    }
    return render(request, 'invoice/report.html', context)


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['cashier'])
def resultMCM(request):
    tanggal_mulai = request.POST.get('tanggal_mulai')
    tanggal_akhir = request.POST.get('tanggal_akhir')
    invoices = Invoice.objects.filter(
        mcm_date__range=[tanggal_mulai, tanggal_akhir])
    nominal = invoices.aggregate(nominal=Sum('nominal'))
    pot_pajak = invoices.aggregate(pot_pajak=Sum('pot_pajak'))
    pot_bank = invoices.aggregate(pot_bank=Sum('pot_bank'))
    bayar = invoices.aggregate(bayar=Sum('bayar'))
    # print(tanggal_mulai, tanggal_akhir, invoices)
    context = {
        'title': 'Result MCM',
        'table_title': 'Daftar MCM',
        'invoices': invoices,
        'tanggal_mulai': tanggal_mulai,
        'tanggal_akhir': tanggal_akhir,
        'pot_pajak': pot_pajak,
        'nominal': nominal,
        'pot_bank': pot_bank,
        'bayar': bayar,
    }
    return render(request, 'invoice/result.html', context)
# end cashier


# View Admin Payment
@ login_required(login_url='login')
@ allowed_users(allowed_roles=['payment'])
def dashboardPayment(request):
    department = request.user.username
    invoices = Invoice.objects.all()

    total_invoice = invoices.count()
    listofclaim = invoices.filter(status='List Of Claim').count()
    invoicing = invoices.filter(status='Invoice').count()
    mcm = invoices.filter(status='MCM').count()
    payment = invoices.filter(status='Payment').count()
    context = {
        'invoice': invoices,
        'total_invoice': total_invoice,
        'listofclaim': listofclaim,
        'invoicing': invoicing,
        'mcm': mcm,
        'payment': payment,
        'department': department
    }
    return render(request, 'invoice/dashboard.html', context)


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['payment'])
def payment(request):
    invoices = Invoice.objects.filter(status='MCM')
    # print ('invoice :',invoice)

    context = {
        'invoice': invoices,
    }
    return render(request, 'invoice/invoice.html', context)


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['payment'])
def post_payment(request, pk):
    invoice = Invoice.objects.get(id=pk)
    lampiran = invoice.buktitransfer
    today = date.today()
    data = {
        'payment_create_date': today,
    }
    form = postPaymentForm(request.POST or None,
                           request.FILES or None, instance=invoice, initial=data)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
        # no_payment = request.POST.get('no_payment')
        # payment_date = request.POST.get('payment_date')
        # print(pk, no_payment, payment_date, payment_create_date)
        # Invoice.objects.filter(id=pk).update(
        #     no_payment=no_payment, payment_date=payment_date, payment_create_date=payment_create_date, status='Payment')
        return redirect('payment')

        # if form.is_valid():
        #     form.save()
    context = {
        'form': form,
        'invoice': invoice,
        'lampiran': lampiran,
        'today': today,
        'title': 'Apply & Post Tipe Transaksi',
    }
    return render(request, 'invoice/post_tipe.html', context)


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['payment'])
def reportPayment(request):
    context = {
        'title': 'Report Payment'
    }
    return render(request, 'invoice/report.html', context)


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['payment'])
def resultPayment(request):
    tanggal_mulai = request.POST.get('tanggal_mulai')
    tanggal_akhir = request.POST.get('tanggal_akhir')
    invoices = Invoice.objects.filter(
        payment_date__range=[tanggal_mulai, tanggal_akhir])
    # print(tanggal_mulai, tanggal_akhir, invoices)
    context = {
        'title': 'Result Payment',
        'table_title': 'Daftar Payment',
        'invoices': invoices,
        'tanggal_mulai': tanggal_mulai,
        'tanggal_akhir': tanggal_akhir,
    }
    return render(request, 'invoice/result.html', context)
# end Payment


# Payroll
@ login_required(login_url='login')
@ allowed_users(allowed_roles=['payroll'])
def dashboardPayroll(request):
    department = request.user.username
    invoices = Invoice.objects.all()

    total_invoice = invoices.count()
    listofclaim = invoices.filter(status='List Of Claim').count()
    invoicing = invoices.filter(status='Invoice').count()
    mcm = invoices.filter(status='MCM').count()
    payment = invoices.filter(status='Payment').count()
    context = {
        'invoice': invoices,
        'total_invoice': total_invoice,
        'listofclaim': listofclaim,
        'invoicing': invoicing,
        'mcm': mcm,
        'payment': payment,
        'department': department,
    }
    return render(request, 'invoice/dashboard.html', context)


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['payroll'])
def payroll(request):
    invoices = Invoice.objects.filter(status='Payroll')
    # print ('invoice :',invoice)

    context = {
        'invoice': invoices,
    }
    return render(request, 'invoice/invoice.html', context)


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['payroll'])
def post_payroll(request, pk):
    invoice = Invoice.objects.get(id=pk)
    lampiran = invoice.filecsv
    today = date.today()
    data = {
        'payroll_create_date': today,
    }
    form = postPayrollForm(request.POST or None,
                           request.FILES or None, instance=invoice, initial=data)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
        # no_payment = request.POST.get('no_payment')
        # payment_date = request.POST.get('payment_date')
        # print(pk, no_payment, payment_date, payment_create_date)
        # Invoice.objects.filter(id=pk).update(
        #     no_payment=no_payment, payment_date=payment_date, payment_create_date=payment_create_date, status='Payment')
        return redirect('payroll')

        # if form.is_valid():
        #     form.save()
    context = {
        'form': form,
        'invoice': invoice,
        'lampiran': lampiran,
        'today': today,
        'title': 'Apply & Post Tipe Transaksi',
    }
    return render(request, 'invoice/post_tipe.html', context)


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['payroll'])
def reportPayroll(request):
    context = {
        'title': 'Report Payroll'
    }
    return render(request, 'invoice/report.html', context)


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['payroll'])
def resultPayroll(request):
    tanggal_mulai = request.POST.get('tanggal_mulai')
    tanggal_akhir = request.POST.get('tanggal_akhir')
    invoices = Invoice.objects.filter(
        payroll_date__range=[tanggal_mulai, tanggal_akhir])
    # print(tanggal_mulai, tanggal_akhir, invoices)
    context = {
        'title': 'Result Payroll',
        'table_title': 'Daftar Payroll',
        'invoices': invoices,
        'tanggal_mulai': tanggal_mulai,
        'tanggal_akhir': tanggal_akhir,
    }
    return render(request, 'invoice/result.html', context)
# End Payroll


# Accounting
@ login_required(login_url='login')
@ allowed_users(allowed_roles=['accounting'])
def dashboardAccounting(request):
    department = request.user.username
    invoices = Invoice.objects.all()

    total_invoice = invoices.count()
    listofclaim = invoices.filter(status='List Of Claim').count()
    invoicing = invoices.filter(status='Invoice').count()
    mcm = invoices.filter(status='MCM').count()
    payment = invoices.filter(status='Payment').count()
    payment_cabang = invoices.filter(status='Payment Cabang').count()
    total_payment = payment + payment_cabang
    context = {
        'invoice': invoices,
        'total_invoice': total_invoice,
        'listofclaim': listofclaim,
        'invoicing': invoicing,
        'mcm': mcm,
        'payment': payment,
        'department': department,
        'total_payment': total_payment,
    }
    return render(request, 'invoice/dashboard.html', context)


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['accounting'])
def accounting(request):
    invoices = Invoice.objects.filter(status='Kompensasi')
    # print ('invoice :',invoice)
    form = TipePostForm()

    context = {
        'invoice': invoices,
        'form': form,
    }
    return render(request, 'invoice/invoice.html', context)


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['accounting'])
def post_kompensasi(request, pk):
    today = date.today()
    # invoice = Invoice.objects.filter(id=pk)
    # bayar = invoice.bayar
    # print(bayar, today)
    Invoice.objects.filter(id=pk).update(
        status="Payment Kompensasi", kompensasi_create_date=today)
    return redirect('accounting')


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['accounting'])
def reportAccounting(request):
    context = {
        'title': 'Report Kompensasi',
    }
    return render(request, 'invoice/report.html', context)


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['accounting'])
def resultAccounting(request):
    tanggal_mulai = request.POST.get('tanggal_mulai')
    tanggal_akhir = request.POST.get('tanggal_akhir')
    invoices = Invoice.objects.filter(
        kompensasi_date__range=[tanggal_mulai, tanggal_akhir])
    # print(tanggal_mulai, tanggal_akhir, invoices)
    context = {
        'title': 'Result Kompensasi',
        'table_title': 'Daftar Kompensasi',
        'invoices': invoices,
        'tanggal_mulai': tanggal_mulai,
        'tanggal_akhir': tanggal_akhir,
    }
    return render(request, 'invoice/result.html', context)
# End Accounting


# View superuser
@ login_required(login_url='login')
@ admin_only
def home(request):
    invoices = Invoice.objects.all()

    total_invoice = invoices.count()
    listofclaim = invoices.filter(status='List Of Claim').count()
    invoicing = invoices.filter(status='Invoice').count()
    mcm = invoices.filter(status='MCM').count()
    payment = invoices.filter(status='Payment').count()
    context = {
        'invoice': invoices,
        'total_invoice': total_invoice,
        'listofclaim': listofclaim,
        'invoicing': invoicing,
        'mcm': mcm,
        'payment': payment
    }
    return render(request, 'invoice/dashboard.html', context)


@ login_required(login_url='login')
@ admin_only
def invoice(request):
    invoices = Invoice.objects.filter(status='List Of Claim')
    print('invoice :', invoice)
    form = TipePostForm()

    context = {
        'invoice': invoices,
        'form': form,
    }
    return render(request, 'invoice/invoice.html', context)


@ login_required(login_url='login')
@ admin_only
def add_invoice(request):
    form = InvoiceForm()
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('invoice')
    context = {
        'title': 'Tambah List Of Claim',
        'form': form,
    }
    return render(request, 'invoice/invoice_form.html', context)


@ login_required(login_url='login')
@ admin_only
def update_invoice(request, pk):
    invoice = Invoice.objects.get(id=pk)
    # print ('i :', invoice)
    form = InvoiceForm(instance=invoice)
    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        if form.is_valid():
            form.save()
            return redirect('invoice')
    context = {
        'title': 'Update List Of Claim',
        'form': form,
    }
    return render(request, 'invoice/invoice_form.html', context)


@ login_required(login_url='login')
@ admin_only
def delete_invoice(request, pk):
    Invoice.objects.filter(id=pk).delete()
    return redirect('invoice')


@ login_required(login_url='login')
@ admin_only
def detail_invoice(request, pk):
    invoices = Invoice.objects.get(id=pk)
    bank = invoices.bank_set.all()
    total_bank = bank.count()
    nominal = bank.aggregate(nominal=Sum('nominal'))

    context = {
        'invoice': invoices,
        'bank': bank,
        'total_bank': total_bank,
        'nominal': nominal,
    }
    return render(request, 'invoice/detail_invoice.html', context)


@ login_required(login_url='login')
def add_bank(request, pk):
    invoices = Invoice.objects.get(id=pk)
    form = BankFormDetail(initial={'invoice': invoices})
    if request.method == 'POST':
        form = BankFormDetail(request.POST)
        if form.is_valid():
            form.save()
            return redirect('detail_listofclaim', pk)
    context = {
        'title': 'Tambah Bank',
        'invoice': invoices,
        'form': form,
    }
    return render(request, 'invoice/bank_form.html', context)


@ login_required(login_url='login')
def delete_bank(request, pk):
    bank = Bank.objects.get(id=pk)
    bank.delete()
    invoice_id = bank.invoice.id
    # print ('id :', invoice_id)
    return redirect('detail_listofclaim', invoice_id)


@ login_required(login_url='login')
def update_bank_admin(request, pk):
    bank = Bank.objects.get(id=pk)
    form = BankFormDetail(instance=bank)
    if request.method == 'POST':
        form = BankFormDetail(request.POST, instance=bank)
        if form.is_valid():
            form.save()
            return redirect('detail_listofclaim', pk)
    context = {
        'title': 'Update Bank',
        'form': form,
    }
    return render(request, 'invoice/bank_form.html', context)


# @login_required(login_url='login')
# def post_potongan(request, pk):
#     invoice = Invoice.objects.get(id=pk)
#     form = PotonganPostForm()
#     if request.method == 'POST':
#         form = PotonganPostForm(request.POST, instance=invoice)
#         if form.is_valid():
#             form.save()
#             return redirect('invoicing')
#     context = {
#         'form': form,
#         'invoice': invoice,
#         'title': 'Apply & Post Tipe Transaksi',
#     }
#     return render(request, 'invoice/post_potongan.html', context)


@ login_required(login_url='login')
@ admin_only
def department(request):
    return render(request, 'invoice/department.html')


@ login_required(login_url='login')
@ admin_only
def bank(request):
    return render(request, 'invoice/bank.html')
