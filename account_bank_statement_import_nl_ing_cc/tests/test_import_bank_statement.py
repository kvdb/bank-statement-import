
# -*- coding: utf-8 -*-

from openerp.tests.common import TransactionCase
from openerp.modules.module import get_module_resource


class TestINGCCFile(TransactionCase):
    """Tests for import bank statement ING CC file format
    (account.bank.statement.import)
    """

    def setUp(self):
        super(TestINGCCFile, self).setUp()
        self.statement_import_model = self.env['account.bank.statement.import']
        self.statement_line_model = self.env['account.bank.statement.line']

    def test_ing_cc_file_import(self):
        from openerp.tools import float_compare
        file_path = get_module_resource(
            'account_bank_statement_import_nl_ing_cc',
            'test_ing_cc_file', 'test_ing_cc.txt')
        data_file = open(file_path, 'rb').read().encode('base64')
        bank_statement_import = self.statement_import_model.with_context(
            journal_id=self.ref('account.bank_journal')).create(
            dict(data_file=data_file))
        bank_statement_import.import_file()
        bank_statement = self.statement_line_model.search(
            [('name', '=', 'GOOGLE *SVCS123 ADVERTISING SERVICES')],
            limit=1)[0].statement_id
        assert float_compare(bank_statement.balance_end_real, -0.26, 2) == 0
