# -*- coding: utf-8 -*-
# This file is part of Seedoo.  The COPYRIGHT file at the top level of
# this module contains the full copyright notices and license terms.

import logging
from openerp.osv import fields, osv
from tools.translate import _
import datetime


_logger = logging.getLogger(__name__)


class wizard(osv.TransientModel):
    """
        A wizard to manage the creation of emergency registry
    """
    _name = 'protocollo.emergency.registry.wizard'
    _description = 'Create Emergency Registry Management'

    _columns = {
        'name': fields.char(
            'Causa Emergenza',
            size=256,
            required=True,
            readonly=False),
        'user_id': fields.many2one(
            'res.users',
            'Responsabile',
            readonly=True),
        'date_start': fields.datetime(
            'Data Inizio Emergenza',
            required=True,
            readonly=False),
        'date_end': fields.datetime(
            'Data Fine Emergenza',
            required=True,
            readonly=False),
        'registry': fields.many2one(
            'protocollo.registry',
            'Registro',
            required=True,
            readonly=False,
            ),
        'number': fields.integer('Numero Protocolli in Emergenza',
                                 required=True),
        }

    def _get_default_registry(self, cr, uid, context=None):
        if context is None:
            context = {}
        registry_obj = self.pool.get('protocollo.registry')
        result = registry_obj.get_registry_for_user(cr, uid)
        if not result:
            raise osv.except_osv(
                _('Attenzione!'),
                _('Utente non abilitato!'))
            return False
        else:
            return result

    _defaults = {
        'registry': _get_default_registry,
        'user_id': lambda obj, cr, uid, context: uid,
    }

    def view_init(self, cr, uid, fields_list, context=None):
        if context is None:
            context = {}
        emergency_registry_obj = self.pool.get('protocollo.emergency.registry')
        reg_ids = emergency_registry_obj.search(cr,
                                                uid,
                                                [('state', '=', 'draft')]
                                                )
        if len(reg_ids) > 0:
                raise osv.except_osv(_('Attenzione'), _('Esiste gia\' un \
                protocollo di emergenza aperto'))
        return {'type': 'ir.actions.act_window_close'}

    def _get_next_number(self, cr, uid, registry):
        sequence_obj = self.pool.get('ir.sequence')
        protocol_obj = self.pool.get('protocollo.protocollo')
        last_id = protocol_obj.search(
            cr, uid,
            [('state', 'in', ('registered', 'notify'))],
            limit=1,
            order='registration_date desc'
        )
        if last_id:
            now = datetime.datetime.now()
            last = protocol_obj.browse(cr, uid, last_id[0])
            if last.registration_date[0:4] < str(now.year):
                seq_id = sequence_obj.search(
                    cr, uid,
                    [
                        ('code',
                         '=',
                         registry.sequence.code)
                    ])
                sequence_obj.write(cr, uid, seq_id, {'number_next': 1})
        next_num = sequence_obj.get(cr,
                                    uid,
                                    registry.sequence.code) or None
        if not next_num:
            raise osv.except_osv(_('Errore'),
                                 _('Il sistema ha riscontrato un errore \
                                 nel reperimento del numero protocollo'))
        return next_num

    def action_create(self, cr, uid, ids, context=None):
        wizard = self.browse(cr, uid, ids[0], context)
        if wizard.name and wizard.date_start:
            emergency_registry_obj = self.pool.\
                get('protocollo.emergency.registry')
            emergency_registry_line_obj = self.pool.\
                get('protocollo.emergency.registry.line')
            line_ids = []
            line_vals = {}
            for num in range(wizard.number):
                line_vals['name'] = self._get_next_number(
                    cr,
                    uid,
                    wizard.registry
                    )
                line_ids.append(emergency_registry_line_obj.create(
                    cr,
                    uid,
                    line_vals,
                    ))
            vals = {
                'name': wizard.name,
                'user_id': wizard.user_id.id,
                'date_start': wizard.date_start,
                'date_end': wizard.date_end,
                'registry': wizard.registry.id,
                'emergency_ids': [[6, 0, line_ids]]
            }
            emergency_registry_obj.create(cr, uid, vals)
        return {'type': 'ir.actions.act_window_close'}
