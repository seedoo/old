# -*- coding: utf-8 -*-
# This file is part of Seedoo.  The COPYRIGHT file at the top level of
# this module contains the full copyright notices and license terms.

import logging
from openerp.osv import fields, osv
from openerp.osv import orm
from tools.translate import _

_logger = logging.getLogger(__name__)


class wizard(osv.TransientModel):
    """
        A wizard to manage the modification of protocol object
    """
    _name = 'protocollo.modify.wizard'
    _description = 'Modify Protocollo Management'

    def set_before(self, before, label, value):
        before += label + ': ' + value + '\n'
        return before

    def set_after(self, after, label, value):
        after += label + ': ' + value + '\n'
        return after

    _columns = {
        'name': fields.char(
            'Numero Protocollo',
            size=256,
            required=True,
            readonly=True),
        'registration_date': fields.datetime('Data Registrazione',
                                             readonly=True),
        'type': fields.selection(
            [
                ('out', 'Uscita'),
                ('in', 'Ingresso'),
                ('internal', 'Interno')
            ],
            'Tipo',
            size=32,
            required=True,
            readonly=True,
        ),
        'typology': fields.many2one(
            'protocollo.typology',
            'Tipologia',
            help="Tipologia invio/ricevimento: \
                Raccomandata, Fax, PEC, etc. \
                si possono inserire nuove tipologie \
                dal menu Tipologie."
        ),
        'receiving_date': fields.datetime('Data Ricevimento',
                                          required=True,),
        'subject': fields.text('Oggetto',
                               required=True,),
        'classification': fields.many2one('protocollo.classification',
                                          'Titolario di Classificazione',
                                          required=True,),
        'sender_protocol': fields.char('Protocollo Mittente',
                                       required=False,),
        'dossier_ids': fields.many2many(
            'protocollo.dossier',
            'dossier_protocollo_pec_rel',
            'wizard_id', 'dossier_id',
            'Fascicoli'),
        'notes': fields.text('Note'),
        'cause': fields.text('Motivo della Modifica', required=True),
    }

    def _default_name(self, cr, uid, context):
        protocollo = self.pool.get('protocollo.protocollo').browse(
            cr,
            uid,
            context['active_id']
            )
        return protocollo.name

    def _default_registration_date(self, cr, uid, context):
        protocollo = self.pool.get('protocollo.protocollo').browse(
            cr,
            uid,
            context['active_id']
            )
        return protocollo.registration_date

    def _default_type(self, cr, uid, context):
        protocollo = self.pool.get('protocollo.protocollo').browse(
            cr,
            uid,
            context['active_id']
            )
        return protocollo.type

    def _default_typology(self, cr, uid, context):
        protocollo = self.pool.get('protocollo.protocollo').browse(
            cr,
            uid,
            context['active_id']
            )
        return protocollo.typology.id

    def _default_receiving_date(self, cr, uid, context):
        protocollo = self.pool.get('protocollo.protocollo').browse(
            cr,
            uid,
            context['active_id']
            )
        return protocollo.receiving_date

    def _default_subject(self, cr, uid, context):
        protocollo = self.pool.get('protocollo.protocollo').browse(
            cr,
            uid,
            context['active_id']
            )
        return protocollo.subject

    def _default_classification(self, cr, uid, context):
        protocollo = self.pool.get('protocollo.protocollo').browse(
            cr,
            uid,
            context['active_id']
            )
        return protocollo.classification.id

    def _default_sender_protocol(self, cr, uid, context):
        protocollo = self.pool.get('protocollo.protocollo').browse(
            cr,
            uid,
            context['active_id']
            )
        return protocollo.sender_protocol

    def _default_dossier_ids(self, cr, uid, context):
        protocollo = self.pool.get('protocollo.protocollo').browse(
            cr,
            uid,
            context['active_id']
            )
        return [(6, 0, protocollo.dossier_ids)]

    def _default_notes(self, cr, uid, context):
        protocollo = self.pool.get('protocollo.protocollo').browse(
            cr,
            uid,
            context['active_id']
            )
        return protocollo.notes

    _defaults = {
        'name': _default_name,
        'registration_date': _default_registration_date,
        'type': _default_type,
        'typology': _default_typology,
        'receiving_date': _default_receiving_date,
        'subject': _default_subject,
        'classification': _default_classification,
        'sender_protocol': _default_sender_protocol,
        'dossier_ids': _default_dossier_ids,
        'notes': _default_notes,
    }

    def action_save(self, cr, uid, ids, context=None):
        before = ''
        after = ''
        wizard = self.browse(cr, uid, ids[0], context)
        protocollo_obj = self.pool.get('protocollo.protocollo')
        protocollo = protocollo_obj.browse(cr,
                                           uid,
                                           context['active_id'],
                                           context=context
                                           )
        historical_obj = self.pool.get('protocollo.history')
        vals = {}
        vals['typology'] = wizard.typology.id
        if wizard.typology.id != protocollo.typology.id:
            if protocollo.typology.pec:
                raise orm.except_orm(
                    _('Attenzione!'),
                    _('Il metodo di spedizione PEC'
                      ' non puo\' essere modificato.')
                )
            elif wizard.typology.pec:
                raise orm.except_orm(
                    _('Attenzione!'),
                    _('Il metodo di spedizione PEC'
                      ' non puo\' essere inserito in questa fase.')
                )
            else:
                before = self.set_before(
                    before,
                    'Tipologia',
                    protocollo.typology.name
                )
                after = self.set_after(
                    after,
                    'Tipologia',
                    wizard.typology.name
                )
        vals['receiving_date'] = wizard.receiving_date
        before = self.set_before(
            before,
            'Data Ricevimento',
            protocollo.receiving_date or ''
            )
        after = self.set_after(
            after,
            'Data Ricevimento',
            wizard.receiving_date or ''
        )
        vals['subject'] = wizard.subject
        before = self.set_before(before, 'Oggetto', protocollo.subject or '')
        after = self.set_after(after, 'Oggetto', wizard.subject or '')
        vals['classification'] = wizard.classification.id
        before = self.set_before(
            before,
            'Titolario',
            protocollo.classification.name
        )
        after = self.set_after(
            after,
            'Titolario',
            wizard.classification.name
        )
        vals['sender_protocol'] = wizard.sender_protocol
        before = self.set_before(
            before,
            'Protocollo Mittente',
            protocollo.sender_protocol or ''
        )
        after = self.set_after(
            after,
            'Protocollo Mittente',
            wizard.sender_protocol or ''
        )
        vals['dossier_ids'] = [[6, 0, [d.id for d in wizard.dossier_ids]]]
        before = self.set_before(
            before,
            'Fascicolo',
            ', '.join([d.name for d in protocollo.dossier_ids])
        )
        after = self.set_after(
            after,
            'Fascicolo',
            ', '.join([dw.name for dw in wizard.dossier_ids])
        )
        vals['notes'] = wizard.notes
        before = self.set_before(before, 'Note', protocollo.notes or '')
        after = self.set_after(
            after,
            'Note',
            wizard.notes or ''
        )
        historical = {
            'user_id': uid,
            'description': wizard.cause,
            'type': 'modify',
            'before': before,
            'after': after,
            # 'protocol_id': context['active_id'],
        }
        history_id = historical_obj.create(cr, uid, historical)
        vals['history_ids'] = [[4, history_id]]
        protocollo_obj.write(
            cr,
            uid,
            context['active_id'],
            vals
        )
        return {'type': 'ir.actions.act_window_close'}
