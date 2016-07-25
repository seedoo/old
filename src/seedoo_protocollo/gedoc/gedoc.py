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
