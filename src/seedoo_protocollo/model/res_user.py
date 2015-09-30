# -*- coding: utf-8 -*-
# This file is part of Seedoo.  The COPYRIGHT file at the top level of
# this module contains the full copyright notices and license terms.

from openerp.osv import orm,  fields


class res_users(orm.Model):
    _inherit = 'res.users'

    def get_user_offices(self, cr, uid, context=None):
        cr.execute("select department_id \
                    from \
                    hr_department_collaborator \
                    where name = %d" % uid)
        return [ids[0] for ids in cr.fetchall()]
