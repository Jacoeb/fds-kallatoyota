from django.urls import path
from . import views


# app_name = 'invoice'
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),

    # User
    path('home/', views.dashboardUser, name='dashboard_user'),
    path('listofclaim/', views.listOfClaim, name='listofclaim'),
    path('listofclaim/add_listofclaim/',
         views.add_listofclaim, name='add_listofclaim'),
    path('listofclaim/update_listofclaim/<str:pk>/',
         views.update_listofclaim, name='update_listofclaim'),
    path('listofclaim/detail_listofclaim/<str:pk>/',
         views.detail_listofclaim, name='detail_listofclaim'),
    path('listofclaim/delete_listofclaim/<str:pk>/',
         views.delete_listofclaim, name='delete_listofclaim'),

    # Admin Invoice
    path('admin_invoice/', views.dashboardInvoice, name='dashboard_invoice'),
    path('invoicing/', views.invoicing, name='invoicing'),
    path('invoicing/add_invoice', views.add_invoice_admin,
         name='add_invoice_admin'),
    path('invoicing/update_invoice/<str:pk>/',
         views.update_invoice_admin, name='update_invoice_admin'),
    path('invoicing/delete_listofclaim/<str:pk>/',
         views.delete_invoice_admin, name='delete_invoice_admin'),
    path('invoice/post_tipe/<str:pk>/', views.post_tipe, name='post_tipe'),

    # Admin Cashier
    path('admin_cashier/', views.dashboardCashier, name='dashboard_cashier'),
    path('mcm/', views.mcm, name='mcm'),
    path('mcm/detail_mcm/<str:pk>',
         views.detail_mcm, name='detail_mcm'),
    path('mcm/post_biaya_admin/<str:pk>/',
         views.add_biaya_admin, name='add_biaya_admin'),
    path('mcm/post_mcm/<str:pk>/', views.post_mcm, name='post_mcm'),

    # Admin Payment
    path('admin_payment/', views.dashboardPayment, name='dashboard_payment'),
    path('payment/', views.payment, name='payment'),
    path('payment/post_payment/<str:pk>',
         views.post_payment, name='post_payment'),

    # Admin Payroll
    path('admin_payroll/', views.dashboardPayroll, name='dashboard_payroll'),
    path('payroll/', views.payroll, name='payroll'),

    # SuperUser
    path('invoice/', views.invoice, name='invoice'),
    path('invoice/add_invoice', views.add_invoice, name='add_invoice'),
    path('invoice/update_invoice/<str:pk>/',
         views.update_invoice, name='update_invoice'),
    path('invoice/detail_invoice/<str:pk>/',
         views.detail_invoice, name='detail_invoice'),
    path('invoice/delete_invoice/<str:pk>/',
         views.delete_invoice, name='delete_invoice'),

    # Bank
    path('bank/', views.bank, name='bank'),
    path('invoice/add_bank/<str:pk>', views.add_bank, name='add_bank'),
    path('invoice/update_bank/<str:pk>/',
         views.update_bank, name='update_bank'),
    path('invoice/delete_bank/<str:pk>/',
         views.delete_bank, name='delete_bank'),

    # Departement
    path('department/', views.department, name='department'),

    # Report
    path('invoicing/report/', views.reportInvoice, name='report_invoice'),
    path('mcm/report/', views.reportMCM, name='report_mcm'),
    path('payment/report/', views.reportPayment, name='report_payment'),
    path('payroll/report/', views.reportPayroll, name='report_payroll'),

    # Result
    path('result/invoice/', views.resultInvoice, name='result_invoice'),
    path('result/mcm/', views.resultMCM, name='result_mcm'),
    path('result/payment/', views.resultPayment, name='result_payment'),
    path('result/payroll/', views.resultPayroll, name='result_payroll'),
]
