# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 KTec S.r.l.
#    (<http://www.ktec.it>).
#
#    Copyright (C) 2014 Associazione Odoo Italia
#    (<http://www.odoo-italia.org>).
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

from openerp.osv import orm
from openerp.osv import fields


class ResPartner(orm.Model):
    _inherit = 'res.partner'

    _columns = {
        'legal_type': fields.selection(
                [
                    ('individual', 'Persona Fisica'),
                    ('legal', 'Azienda privata'),
                    ('government', 'Amministrazione pubblica')
                ], 'Tipologia', size=32, required=False),

        'pa_type': fields.selection(
                [
                    ('pa', 'Amministrazione Principale'),
                    ('aoo', 'Area Organizzativa Omogenea'),
                    ('uo', 'Unità Organizzativa')], 'Tipologia amministrazione', size=5, required=False),

        'super_type': fields.char('super_type', size=5, required=False),

        'ident_code': fields.char(
                'Codice Identificativo Area (AOO)',
                size=256,
                required=False),

        'ammi_code': fields.char(
                'Codice Amministrazione',
                size=256,
                required=False),

        'ipa_code': fields.char(
                'Codice Unità Organizzativa',
                size=256,
                required=False),

        'parent_pa_id': fields.many2one("res.partner", "Organizzazione di Appartenenza", required=False),
        'parent_pa_type': fields.related('parent_pa_id', 'pa_type', type='selection', readonly=True, string='Tipologia amministrazione padre'),
        'child_pa_ids': fields.one2many("res.partner", "parent_pa_id", "Strutture Afferenti", required=False)

    }

    def on_change_pa_type(self, cr, uid, ids, pa_type):
        res = {'value': {}}

        if pa_type=='aoo':
            res['value']['super_type'] = 'pa'
        elif pa_type=='uo':
            res['value']['super_type'] = 'aoo'

        return res
