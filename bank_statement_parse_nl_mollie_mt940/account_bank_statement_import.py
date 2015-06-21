# -*- coding: utf-8 -*-
"""Parse a MT940 Mollie file."""
import logging

from openerp import models
from .mt940 import MT940Parser as Parser


_LOGGER = logging.getLogger(__name__)


class AccountBankStatementImport(models.TransientModel):
    """Add parsing of Mollie mt940 files to bank statement import."""
    _inherit = 'account.bank.statement.import'

    def _parse_file(self, cr, uid, data_file, context=None):
        """Parse a MT940 Mollie file."""
        parser = Parser()
        try:
            _LOGGER.debug("Try parsing with MT940 Mollie.")
            return parser.parse(data_file)
        except ValueError:
            # Returning super will call next candidate:
            _LOGGER.debug("Statement file was not a MT940 Mollie file.")
            return super(AccountBankStatementImport, self)._parse_file(
                cr, uid, data_file, context=context)
