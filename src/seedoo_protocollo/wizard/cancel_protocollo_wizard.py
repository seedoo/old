# -*- coding: utf-8 -*-
# This file is part of Seedoo.  The COPYRIGHT file at the top level of
# this module contains the full copyright notices and license terms.

import logging
from openerp.osv import fields, osv
from openerp.tools import (
    DEFAULT_SERVER_DATETIME_FORMAT as DSDF)
from tools.translate import _
import time
from openerp import netsvc

_logger = logging.getLogger(__name__)


class wizard(osv.TransientModel):
    """
        A wizard to manage the cancel state of protocol
    """
    _name = 'protocollo.cancel.wizard'
    _description = 'Cancel Protocol Management'

    _columns = {
        'name': fields.char(
            'Causa Cancellazione',
            required=True,
            readonly=False
        ),
        'user_id': fields.many2one(
            'res.users',
            'Responsabile',
            readonly=True
        ),
        'date_cancel': fields.datetime(
            'Data Cancellazione',
            required=True,
            readonly=True
        ),
    }

    _defaults = {
        'user_id': lambda obj, cr, uid, context: uid,
        'date_cancel': fields.datetime.now
    }

    def action_cancel(self, cr, uid, ids, context=None):
        wizard = self.browse(cr, uid, ids[0], context)
        if wizard.name and wizard.date_cancel:
            protocollo_obj = self.pool.get('protocollo.protocollo')
            historical_obj = self.pool.get('protocollo.history')
            historical = {}
            historical['name'] = wizard.date_cancel
            historical['user_id'] = wizard.user_id.id
            historical['description'] = wizard.name
            historical['type'] = 'cancel'
            history_id = historical_obj.create(cr, uid, historical)
            vals = {}
            vals['history_ids'] = [[4, history_id]]
            protocollo_obj.write(
                cr,
                uid,
                context['active_id'],
                vals
            )
            wf_service = netsvc.LocalService('workflow')
            wf_service.trg_validate(
                uid,
                'protocollo.protocollo',
                context['active_id'], 'cancel', cr
            )
        return {'type': 'ir.actions.act_window_close'}
