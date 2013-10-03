# -*- encoding: utf-8 -*-

{
    'name': 'ISF HGH COA - Accounting',
    'version': '0.4',
    'depends': ['account_accountant', 'isf_currency_slsh'],
    'author': 'Antonio Verni for ISF',
    'description': """
Hargeisa General Hospital Chart of Accounts
================================================

Hargeisa General Hospital accounting chart and localization.
    """,
    'license': 'AGPL-3',
    'category': 'Localization/Account Charts',
    'data': [
        'data/account.account.type.csv',
        'data/account.account.csv',
        ],
    'demo': [],
    'installable': True,
    'auto_install': False
}
