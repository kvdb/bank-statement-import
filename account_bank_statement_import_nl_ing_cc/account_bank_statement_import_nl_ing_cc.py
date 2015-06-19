# -*- encoding: utf-8 -*-
import dateutil.parser
import StringIO

from openerp.tools.translate import _
from openerp import api, models
from openerp.exceptions import Warning


class AccountBankStatementImport(models.TransientModel):
    _inherit = 'account.bank.statement.import'

    @api.model
    def _check_ing_cc(self, data_file):
        '''This method is designed to be inherited'''
        return data_file.strip().startswith('Date posted')

    @api.model
    def _parse_file(self, data_file):
        """ Import a file in ING CC format"""
        if not self._check_ing_cc(data_file):
            return super(AccountBankStatementImport, self)._parse_file(
                data_file)

        try:
            file_data = ""
            for line in StringIO.StringIO(data_file).readlines():
                file_data += line
            if '\r' in file_data:
                data_list = file_data.split('\r')
            else:
                data_list = file_data.split('\n')
            header = data_list[0].strip()
            header = header.split("\t")
            data_list = data_list[1:]
        except:
            raise Warning(_('Could not decipher the ING CC file.'))

        transactions = []
        total = 0
        statement_date = None
        statement_account_number = None

        for line in data_list:
            vals_line = {}
            line = line.strip()
            if not line:
                continue
            parts = line.split('\t')
            vals_line['date'] = dateutil.parser.parse(
                parts[0], fuzzy=True).date()
            amount = float(parts[11].replace(',', '')) * -1
            vals_line['amount'] = amount
            total += amount
            vals_line['ref'] = parts[14]
            vals_line['name'] = '{} {}'.format(parts[2], parts[7])
            statement_date = dateutil.parser.parse(
                parts[15], fuzzy=True).date()
            statement_account_number = parts[17]
            transactions.append(vals_line)

        vals_bank_statement = {
            'date': statement_date,
            'balance_end_real': total,
            'transactions': transactions,
            'currency_code': None,
            'account_number': statement_account_number
        }

        return [vals_bank_statement]
