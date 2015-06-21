# -*- coding: utf-8 -*-
"""Implement parser for MT940 files - Mollie dialect."""
import re
from string import printable
from openerp.addons.bank_statement_parse_mt940.mt940 import (
    MT940, str2amount, get_subfields, handle_common_subfields)


class MT940Parser(MT940):
    """Implement parser for MT940 files - Mollie dialect."""

    tag_61_regex = re.compile(
        r'^(?P<date>\d{6})(?P<line_date>\d{0,4})'
        r'(?P<sign>[CD])(?P<amount>\d+,\d{2})N(?P<type>.{3})'
    )

    def __init__(self):
        """Initialize parser - override at least header_regex."""
        super(MT940Parser, self).__init__()
        self.mt940_type = 'Mollie'
        self.header_lines = 0  # Number of lines to skip
        # Do not user $ for end of string below: line contains much
        # more data than just the first line.
        self.header_regex = '^:20:940'  # Start of relevant data

    def handle_tag_61(self, data):
        """Handle tag 61: transaction data."""
        super(MT940Parser, self).handle_tag_61(data)
        re_61 = self.tag_61_regex.match(data)
        if not re_61:
            raise ValueError("Cannot parse %s" % data)
        parsed_data = re_61.groupdict()
        self.current_transaction.amount = (
            str2amount(parsed_data['sign'], parsed_data['amount']))
        print(self.current_transaction)

    def handle_tag_86(self, data):
        """Handle tag 86: transaction details"""
        if not self.current_transaction:
            return
        codewords = ['TRTP', 'REMI', 'EREF', 'NAME', 'BIC', 'IBAN']
        subfields = get_subfields(data, codewords)
        transaction = self.current_transaction
        # If we have no subfields, set message to whole of data passed:
        if not subfields:
            transaction.message = data
        else:
            handle_common_subfields(transaction, subfields)
            # Use subfields for transaction details:
            if 'NAME' in subfields:
                transaction.remote_owner = ' '.join(subfields['NAME'])
        # Prevent handling tag 86 later for non transaction details:
        self.current_transaction = None
