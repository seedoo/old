# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2016 Innoviu srl (<http://www.innoviu.it>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv


class protocollo_dossier(osv.Model):
    _inherit = 'protocollo.dossier'

    _columns = {
        'protocollo_ids': fields.many2many(
            'protocollo.protocollo',
            'dossier_protocollo_rel',
            'dossier_id', 'protocollo_id',
            'Protocolli Allegati al Fascicolo',
            readonly=True,
            states={'draft':
                    [('readonly', False)],
                    'open':
                    [('readonly', False)],
                    }
            ),
    }

    def is_document_present(self, cr, uid, ids, *args):
        for dossier in self.browse(cr, uid, ids):
            if len(dossier.protocollo_ids):
                return True
        return super(protocollo_dossier, self).\
            is_document_present(cr, uid, ids, *args)


class DocumentSearch(osv.TransientModel):
    """
        Advanced Document Search
    """
    _inherit = 'gedoc.document.search'

    def _search_action_document(
            self, cr, uid, wizard,
            search_domain, context=None):
        if wizard.name == 'protocollo.protocollo':
            if wizard.text_name:
                search_domain.append(('name', 'ilike', wizard.text_name))
            if wizard.subject:
                search_domain.append(('subject', 'ilike', wizard.subject))
            if wizard.classification_id:
                search_domain.append(
                    ('classification', '=', wizard.classification_id.id))
            if wizard.partner_id:
                search_domain.append(
                    ('sender_receivers',
                     'ilike',
                     wizard.partner_id.name)
                    )
            if wizard.office_id:
                search_domain.append(
                    ('assigne',
                     'in',
                     [wizard.office_id.id])
                    )
            if wizard.date_close_start:
                search_domain.append(
                    ('registration_date',
                     '>=',
                     wizard.date_close_start)
                    )
            if wizard.date_close_end:
                search_domain.append(
                    ('registration_date',
                     '<=',
                     wizard.date_close_end)
                    )
            return search_domain
        else:
            return search_domain
