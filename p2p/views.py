# Copyright 2015 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.shortcuts import render
from p2p.forms import P2PForm

# Create your views here.
# Create your views here.
def p2p_accounting(request):
    # A HTTP POST?
    if request.method == 'POST':
        form = P2PForm(request.POST)
        if form.is_valid(): # All validation rules pass
            item_type_val = form.cleaned_data ['item_type']

            period_end_accrual_val = form.cleaned_data ['period_end_accrual']
            allow_recon_accounting = form.cleaned_data ['allow_recon_accounting']
            # setting period end accrual as a Boolean
            if  period_end_accrual_val== 'True':
                period_end_accrual_val = True
            else:
                period_end_accrual_val = False

            # setting allow recon accounting as a Boolean
            if  allow_recon_accounting == 'True':
                allow_recon_accounting  = True
            else:
                allow_recon_accounting  = False


        else:
            #this is fallback and usually not used since we are using 'Choices' in our form
            item_type_val ='Expense'
            allow_recon_accounting = False
            period_end_accrual_val =False
    else:
        #Initial load when the request != POST (e.g. GET)
        form=P2PForm()
        #setting form variables to default values for a != POST (e.g. GET request)
        item_type_val ='Expense'
        period_end_accrual_val =False
        allow_recon_accounting = False

    print(period_end_accrual_val)
    receipt_accting=  tuple(field for field in p2p_accting_list if ( field['accounting_entry']=='PO Receipt' and
                                                            field['item_type']==item_type_val and
                                                            field['period_end_accrual']== period_end_accrual_val
                                                            ) )
    deliver_accting = (field for field in p2p_accting_list  if ( field['accounting_entry']=='PO Deliver' and
                                                            field['item_type']==item_type_val
                                                            ) )
    invoice_accting = (field for field in p2p_accting_list if (field['accounting_entry']=='AP Invoice' and
                                                            field ['period_end_accrual']==period_end_accrual_val and
                                                            (field['item_type']==item_type_val or
                                                                field['item_type']=='Not Relevant')
                                                            ) )
    payment_accting = (field for field in p2p_accting_list  if (field['accounting_entry']=='AP Payment' and
                                                            field ['allow_recon_accounting']==allow_recon_accounting
                                                            ) )
    recon_accting = tuple(field for field in p2p_accting_list  if (field['accounting_entry']=='AP Payment Reco' and
                                                            field ['allow_recon_accounting']==allow_recon_accounting
                                                            ) )
    pe_accrual_accting = tuple(field for field in p2p_accting_list if (
                                                            field['accounting_entry']=='PO Receipt Accruals - Period End' and
                                                            field['item_type']==item_type_val and
                                                            field ['period_end_accrual']==period_end_accrual_val
                                                            ) )
     #list_accounting =  (d for d in list_accounting_expense if d['accounting_entry']=='PO Receipt' )
    return render(request, 'p2p/p2p_accounting.html',
        {'po_receipt_accting': receipt_accting, 'po_deliver_accting' : deliver_accting,
        'ap_invoice_accting':invoice_accting, 'ap_payment_accting':payment_accting,
        'ap_payment_recon_accting': recon_accting,'po_pe_accrual_accting': pe_accrual_accting,
        'form': form})



p2p_accting_list = [
  {
    "id":1,
    "dr_cr":"DEBIT",
    "account_description":"Receiving Inventory A/c",
    "item_type":"Expense",
    "stream":"P2P",
    "period_end_accrual":0,
    "allow_recon_accounting":0,
    "oe_line_flow":"Bill Only",
    "defaults_from":"Receiving Options",
    "journal_source":"Cost Management",
    "journal_category":"Receipts",
    "accounting_class":"Receiving Inspection",
    "notes":"NA",
    "accounting_entry":"PO Receipt"
  },
  {
    "id":2,
    "dr_cr":"CREDIT",
    "account_description":"Expense AP Accrual A/c",
    "item_type":"Expense",
    "stream":"P2P",
    "period_end_accrual":0,
    "allow_recon_accounting":0,
    "oe_line_flow":"Bill Only",
    "defaults_from":"Purchasing Options",
    "journal_source":"Cost Management",
    "journal_category":"Receiving",
    "accounting_class":"Accrual",
    "notes":"NA",
    "accounting_entry":"PO Receipt"
  },
  {
    "id":3,
    "dr_cr":"DEBIT",
    "account_description":"Expense/PO Charge A/c",
    "item_type":"Expense",
    "stream":"P2P",
    "period_end_accrual":0,
    "allow_recon_accounting":0,
    "oe_line_flow":"Bill Only",
    "defaults_from":"PO Distributions",
    "journal_source":"Cost Management",
    "journal_category":"Receiving",
    "accounting_class":"Charge",
    "notes":"NA",
    "accounting_entry":"PO Deliver"
  },
  {
    "id":4,
    "dr_cr":"CREDIT",
    "account_description":"Receiving Inventory A/c",
    "item_type":"Expense",
    "stream":"P2P",
    "period_end_accrual":0,
    "allow_recon_accounting":0,
    "oe_line_flow":"Bill Only",
    "defaults_from":"Receiving Options",
    "journal_source":"Cost Management",
    "journal_category":"Receiving",
    "accounting_class":"Receiving Inspection",
    "notes":"NA",
    "accounting_entry":"PO Deliver"
  },
  {
    "id":5,
    "dr_cr":"DEBIT",
    "account_description":"Receiving Inventory A/c",
    "item_type":"Inventory",
    "stream":"",
    "period_end_accrual":0,
    "allow_recon_accounting":0,
    "oe_line_flow":"Bill Only",
    "defaults_from":"PO Distributions",
    "journal_source":"Cost Management",
    "journal_category":"Receiving",
    "accounting_class":"Receiving Inspection",
    "notes":"NA",
    "accounting_entry":"PO Receipt"
  },
  {
    "id":6,
    "dr_cr":"CREDIT",
    "account_description":"Inventory AP Accrual A/c",
    "item_type":"Inventory",
    "stream":"",
    "period_end_accrual":0,
    "allow_recon_accounting":0,
    "oe_line_flow":"Bill Only",
    "defaults_from":"Organization Parameters",
    "journal_source":"Cost Management",
    "journal_category":"Receiving",
    "accounting_class":"Accrual",
    "notes":"NA",
    "accounting_entry":"PO Receipt"
  },
  {
    "id":7,
    "dr_cr":"DEBIT",
    "account_description":"Inventory Material A/c",
    "item_type":"Inventory",
    "stream":"",
    "period_end_accrual":0,
    "allow_recon_accounting":0,
    "oe_line_flow":"Bill Only",
    "defaults_from":"Organization Parameters",
    "journal_source":"Cost Management",
    "journal_category":"Inventory",
    "accounting_class":"Inventory Valuation",
    "notes":"NA",
    "accounting_entry":"PO Deliver"
  },
  {
    "id":8,
    "dr_cr":"CREDIT",
    "account_description":"Receiving Inventory A/c",
    "item_type":"Inventory",
    "stream":"",
    "period_end_accrual":0,
    "allow_recon_accounting":0,
    "oe_line_flow":"Bill Only",
    "defaults_from":"Receiving Options",
    "journal_source":"Cost Management",
    "journal_category":"Inventory",
    "accounting_class":"Receiving Inspection",
    "notes":"NA",
    "accounting_entry":"PO Deliver"
  },
  {
    "id":9,
    "dr_cr":"DEBIT",
    "account_description":"Expense AP Accrual A/c",
    "item_type":"Expense",
    "stream":"",
    "period_end_accrual":0,
    "allow_recon_accounting":0,
    "oe_line_flow":"Bill Only",
    "defaults_from":"Purchasing Options",
    "journal_source":"Payables",
    "journal_category":"Standard Invoices",
    "accounting_class":"Accrual",
    "notes":"NA",
    "accounting_entry":"AP Invoice"
  },
  {
    "id":10,
    "dr_cr":"CREDIT",
    "account_description":"AP Liability A/c",
    "item_type":"Expense",
    "stream":"",
    "period_end_accrual":0,
    "allow_recon_accounting":0,
    "oe_line_flow":"Bill Only",
    "defaults_from":"Supplier Site",
    "journal_source":"Payables",
    "journal_category":"Standard Invoices",
    "accounting_class":"Liability",
    "notes":"NA",
    "accounting_entry":"AP Invoice - Delete"
  },
  {
    "id":11,
    "dr_cr":"DEBIT",
    "account_description":"Cash/Bank A/c",
    "item_type":"Not Relevant",
    "stream":"",
    "period_end_accrual":0,
    "allow_recon_accounting":0,
    "oe_line_flow":"Bill Only",
    "defaults_from":"Bank Accounts",
    "journal_source":"Payables",
    "journal_category":"Reconciled Payments",
    "accounting_class":"Cash",
    "notes":"NA",
    "accounting_entry":"AP Payment"
  },
  {
    "id":12,
    "dr_cr":"CREDIT",
    "account_description":"AP Liability A/c",
    "item_type":"Not Relevant",
    "stream":"",
    "period_end_accrual":0,
    "allow_recon_accounting":0,
    "oe_line_flow":"Bill Only",
    "defaults_from":"AP Invoice Header",
    "journal_source":"Payables",
    "journal_category":"Payments",
    "accounting_class":"Liability",
    "notes":"NA",
    "accounting_entry":"AP Payment"
  },
  {
    "id":13,
    "dr_cr":"DEBIT",
    "account_description":"Expense/PO Charge A/c",
    "item_type":"Expense",
    "stream":"",
    "period_end_accrual":1,
    "allow_recon_accounting":0,
    "oe_line_flow":"Bill Only",
    "defaults_from":"PO Distributions",
    "journal_source":"Payables",
    "journal_category":"Standard Invoices",
    "accounting_class":"Item Expense",
    "notes":"#verify accounting Class and Defaults",
    "accounting_entry":"AP Invoice"
  },
  {
    "id":14,
    "dr_cr":"CREDIT",
    "account_description":"AP Liability A/c",
    "item_type":"Not Relevant",
    "stream":"",
    "period_end_accrual":1,
    "allow_recon_accounting":0,
    "oe_line_flow":"Bill Only",
    "defaults_from":"Supplier Site",
    "journal_source":"Payables",
    "journal_category":"Standard Invoices",
    "accounting_class":"Liability",
    "notes":"NA",
    "accounting_entry":"AP Invoice"
  },
  {
    "id":15,
    "dr_cr":"DEBIT",
    "account_description":"Cash/Bank A/c",
    "item_type":"Not Relevant",
    "stream":"",
    "period_end_accrual":0,
    "allow_recon_accounting":1,
    "oe_line_flow":"Bill Only",
    "defaults_from":"Bank Accounts",
    "journal_source":"Payables",
    "journal_category":"Reconciled Payments",
    "accounting_class":"Cash",
    "notes":"NA",
    "accounting_entry":"AP Payment Reco"
  },
  {
    "id":16,
    "dr_cr":"CREDIT",
    "account_description":"Cash Clearing A/c",
    "item_type":"Not Relevant",
    "stream":"",
    "period_end_accrual":0,
    "allow_recon_accounting":1,
    "oe_line_flow":"Bill Only",
    "defaults_from":"Bank Accounts",
    "journal_source":"Payables",
    "journal_category":"Reconciled Payments",
    "accounting_class":"Cash Clearing",
    "notes":"NA",
    "accounting_entry":"AP Payment Reco"
  },
  {
    "id":17,
    "dr_cr":"DEBIT",
    "account_description":"AP Liability A/c",
    "item_type":"Not Relevant",
    "stream":"",
    "period_end_accrual":0,
    "allow_recon_accounting":1,
    "oe_line_flow":"Bill Only",
    "defaults_from":"AP Invoice Header",
    "journal_source":"Payables",
    "journal_category":"Payments",
    "accounting_class":"Liability",
    "notes":"NA",
    "accounting_entry":"AP Payment"
  },
  {
    "id":18,
    "dr_cr":"CREDIT",
    "account_description":"Cash Clearing A/c",
    "item_type":"Not Relevant",
    "stream":"",
    "period_end_accrual":0,
    "allow_recon_accounting":1,
    "oe_line_flow":"Bill Only",
    "defaults_from":"Bank Accounts",
    "journal_source":"Payables",
    "journal_category":"Reconciled Payments",
    "accounting_class":"Cash Clearing",
    "notes":"NA",
    "accounting_entry":"AP Payment"
  },
  {
    "id":19,
    "dr_cr":"DEBIT",
    "account_description":"Inventory Material A/c",
    "item_type":"Inventory",
    "stream":"",
    "period_end_accrual":0,
    "allow_recon_accounting":0,
    "oe_line_flow":"Bill Only",
    "defaults_from":"Organization Parameters",
    "journal_source":"Cost Management",
    "journal_category":"Inventory",
    "accounting_class":"Inventory Valuation",
    "notes":"NA",
    "accounting_entry":"Misc. Receipt"
  },
  {
    "id":20,
    "dr_cr":"CREDIT",
    "account_description":"Inventory Offset A/c",
    "item_type":"Inventory",
    "stream":"",
    "period_end_accrual":0,
    "allow_recon_accounting":0,
    "oe_line_flow":"Bill Only",
    "defaults_from":"Manually Entered",
    "journal_source":"Cost Management",
    "journal_category":"Inventory",
    "accounting_class":"Offset",
    "notes":"NA",
    "accounting_entry":"Misc. Receipt"
  },
  {
    "id":21,
    "dr_cr":"DEBIT",
    "account_description":"Inventory A/c",
    "item_type":"Inventory",
    "stream":"",
    "period_end_accrual":0,
    "allow_recon_accounting":0,
    "oe_line_flow":"Bill Only",
    "defaults_from":"",
    "journal_source":"",
    "journal_category":"",
    "accounting_class":"",
    "notes":"NA",
    "accounting_entry":"Pick Confirm"
  },
  {
    "id":22,
    "dr_cr":"CREDIT",
    "account_description":"Inventory A/c",
    "item_type":"Inventory",
    "stream":"",
    "period_end_accrual":0,
    "allow_recon_accounting":0,
    "oe_line_flow":"Bill Only",
    "defaults_from":"",
    "journal_source":"",
    "journal_category":"",
    "accounting_class":"",
    "notes":"NA",
    "accounting_entry":"Pick Confirm"
  },
  {
    "id":23,
    "dr_cr":"DEBIT",
    "account_description":"Deferred COGS A/c",
    "item_type":"Inventory",
    "stream":"",
    "period_end_accrual":0,
    "allow_recon_accounting":0,
    "oe_line_flow":"Bill Only",
    "defaults_from":"",
    "journal_source":"",
    "journal_category":"",
    "accounting_class":"",
    "notes":"NA",
    "accounting_entry":"Ship Confirm"
  },
  {
    "id":24,
    "dr_cr":"CREDIT",
    "account_description":"Inventory A/c",
    "item_type":"Inventory",
    "stream":"",
    "period_end_accrual":0,
    "allow_recon_accounting":0,
    "oe_line_flow":"Bill Only",
    "defaults_from":"",
    "journal_source":"",
    "journal_category":"",
    "accounting_class":"",
    "notes":"NA",
    "accounting_entry":"Ship Confirm"
  },
  {
    "id":25,
    "dr_cr":"DEBIT",
    "account_description":"COGS A/c",
    "item_type":"Inventory",
    "stream":"",
    "period_end_accrual":0,
    "allow_recon_accounting":0,
    "oe_line_flow":"Bill Only",
    "defaults_from":"",
    "journal_source":"",
    "journal_category":"",
    "accounting_class":"",
    "notes":"NA",
    "accounting_entry":"Revenue Recognition"
  },
  {
    "id":26,
    "dr_cr":"CREDIT",
    "account_description":"Deferred COGS A/c",
    "item_type":"Inventory",
    "stream":"",
    "period_end_accrual":0,
    "allow_recon_accounting":0,
    "oe_line_flow":"Bill Only",
    "defaults_from":"",
    "journal_source":"",
    "journal_category":"",
    "accounting_class":"",
    "notes":"NA",
    "accounting_entry":"Revenue Recognition"
  },
  {
    "id":27,
    "dr_cr":"DEBIT",
    "account_description":"Receivable A/c",
    "item_type":"Not Relevant",
    "stream":"",
    "period_end_accrual":0,
    "allow_recon_accounting":0,
    "oe_line_flow":"Bill Only",
    "defaults_from":"Auto-Accounting Rules",
    "journal_source":"Receivables",
    "journal_category":"Sales Invoices",
    "accounting_class":"Receivable",
    "notes":"NA",
    "accounting_entry":"AR Invoice"
  },
  {
    "id":28,
    "dr_cr":"CREDIT",
    "account_description":"Revenue A/c",
    "item_type":"Not Relevant",
    "stream":"",
    "period_end_accrual":0,
    "allow_recon_accounting":0,
    "oe_line_flow":"Bill Only",
    "defaults_from":"Auto-Accounting Rules",
    "journal_source":"Receivables",
    "journal_category":"Sales Invoices",
    "accounting_class":"Revenue",
    "notes":"NA",
    "accounting_entry":"AR Invoice"
  },
  {
    "id":29,
    "dr_cr":"DEBIT",
    "account_description":"Cash Clearing A/c",
    "item_type":"Not Relevant",
    "stream":"",
    "period_end_accrual":0,
    "allow_recon_accounting":0,
    "oe_line_flow":"Bill Only",
    "defaults_from":"Payment Method",
    "journal_source":"Receivables",
    "journal_category":"Receipts",
    "accounting_class":"Remitted Cash",
    "notes":"NA",
    "accounting_entry":"AR Receipt"
  },
  {
    "id":30,
    "dr_cr":"CREDIT",
    "account_description":"Receivable A/c",
    "item_type":"Inventory",
    "stream":"",
    "period_end_accrual":0,
    "allow_recon_accounting":0,
    "oe_line_flow":"Bill Only",
    "defaults_from":"Auto-Accounting Rules",
    "journal_source":"Receivables",
    "journal_category":"Receipts",
    "accounting_class":"Receivable",
    "notes":"NA",
    "accounting_entry":"AR Receipt"
  },
  {
    "id":31,
    "dr_cr":"DEBIT",
    "account_description":"Cash/Bank A/c",
    "item_type":"Not Relevant",
    "stream":"",
    "period_end_accrual":0,
    "allow_recon_accounting":0,
    "oe_line_flow":"Bill Only",
    "defaults_from":"#",
    "journal_source":"Receivables",
    "journal_category":"Receipts",
    "accounting_class":"Cash",
    "notes":"NA",
    "accounting_entry":"AR Receipt Recon"
  },
  {
    "id":32,
    "dr_cr":"CREDIT",
    "account_description":"Cash Clearing A/c",
    "item_type":"Not Relevant",
    "stream":"",
    "period_end_accrual":0,
    "allow_recon_accounting":0,
    "oe_line_flow":"Bill Only",
    "defaults_from":"NA",
    "journal_source":"Payables",
    "journal_category":"Receipts",
    "accounting_class":"Remitted Cash",
    "notes":"NA",
    "accounting_entry":"AR Receipt Recon"
  },
  {
    "id":33,
    "dr_cr":"DEBIT",
    "account_description":"Charge A/c #",
    "item_type":"Inventory",
    "stream":"",
    "period_end_accrual":0,
    "allow_recon_accounting":0,
    "oe_line_flow":"Bill Only",
    "defaults_from":"WIP Accounting Class",
    "journal_source":"Cost Management",
    "journal_category":"Inventory",
    "accounting_class":"WIP Valuation",
    "notes":"NA",
    "accounting_entry":"WIP Issue"
  },
  {
    "id":34,
    "dr_cr":"CREDIT",
    "account_description":"Inventory Valuation A/c",
    "item_type":"Inventory",
    "stream":"",
    "period_end_accrual":0,
    "allow_recon_accounting":0,
    "oe_line_flow":"Bill Only",
    "defaults_from":"Organization Parameters",
    "journal_source":"Cost Management",
    "journal_category":"Inventory",
    "accounting_class":"Inventory Valuation",
    "notes":"NA",
    "accounting_entry":"WIP Issue"
  },
  {
    "id":35,
    "dr_cr":"DEBIT",
    "account_description":"Inventory AP Accrual A/c",
    "item_type":"Inventory",
    "stream":"",
    "period_end_accrual":0,
    "allow_recon_accounting":0,
    "oe_line_flow":"Bill Only",
    "defaults_from":"Organization Parameters",
    "journal_source":"Payables",
    "journal_category":"Standard Invoices",
    "accounting_class":"Accrual",
    "notes":"NA",
    "accounting_entry":"AP Invoice"
  },
  {
    "id":36,
    "dr_cr":"CREDIT",
    "account_description":"AP Liability A/c",
    "item_type":"Not Relevant",
    "stream":"",
    "period_end_accrual":0,
    "allow_recon_accounting":0,
    "oe_line_flow":"Bill Only",
    "defaults_from":"Supplier Site",
    "journal_source":"Payables",
    "journal_category":"Standard Invoices",
    "accounting_class":"Liability",
    "notes":"NA",
    "accounting_entry":"AP Invoice"
  },
  {
    "id":37,
    "dr_cr":"DEBIT",
    "account_description":"Expense/ PO Charge A/c",
    "item_type":"Expense",
    "stream":"",
    "period_end_accrual":1,
    "allow_recon_accounting":0,
    "oe_line_flow":"Bill Only",
    "defaults_from":"PO Distributions",
    "journal_source":"Cash Management",
    "journal_category":"Receiving",
    "accounting_class":"Charge",
    "notes":"#Check Journal category & Accting class",
    "accounting_entry":"PO Receipt Accruals - Period End"
  },
  {
    "id":38,
    "dr_cr":"CREDIT",
    "account_description":"Expense AP Accrual A/c",
    "item_type":"Expense",
    "stream":"",
    "period_end_accrual":1,
    "allow_recon_accounting":0,
    "oe_line_flow":"Bill Only",
    "defaults_from":"Purchasing Options",
    "journal_source":"Payables",
    "journal_category":"Receiving",
    "accounting_class":"Accrual",
    "notes":"#Check Journal category",
    "accounting_entry":"PO Receipt Accruals - Period End"
  }
]
