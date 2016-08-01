# -*- coding: utf-8 -*-
# This file is part of Seedoo.  The COPYRIGHT file at the top level of
# this module contains the full copyright notices and license terms.

from report import report_sxw
import time


class ProtocolloJournalReport(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
        super(ProtocolloJournalReport, self).__init__(
            cr,
            uid,
            name, context=context
        )
        self.localcontext.update({
            'time': time
            })

