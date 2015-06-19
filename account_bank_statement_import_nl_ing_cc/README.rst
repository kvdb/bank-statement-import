Import NL ING Credit Card Statements
====================================

This module allows you to import the Dutch ING Credit Card TSV files in Odoo as bank statements.

Installation
============

This module depends on the module *account_bank_statement_import* which
is available:
* for Odoo version 8: in the OCA project `bank-statement-import <https://github.com/OCA/bank-statement-import>`

Configuration
=============

In the menu Accounting > Configuration > Accounts > Setup your Bank Accounts,
make sure that you have your ING CC bank account with the following parameters:
* Bank Account Type: Normal Bank Account
* Account Number: the credit card number (with asterisks) of your account
* Account Journal: the journal associated to your CC account

Credits
=======

Contributors
------------

* Kees van den Broek <kvdb@d-centralize.nl>

Maintainer
----------

.. image:: http://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: http://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose mission is to support the collaborative development of Odoo features and promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.
