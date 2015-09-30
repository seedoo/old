# -*- encoding: utf-8 -*-
# This file is part of Seedoo.  The COPYRIGHT file at the top level of
# this module contains the full copyright notices and license terms.

from openerp import SUPERUSER_ID
from openerp.osv import orm,  fields
from tools.translate import _


class hr_department_collaborator(orm.Model):
    _name = 'hr.department.collaborator'

    _columns = {
        'department_id': fields.many2one('hr.department',
                                         'Department',
                                         required=True),
        'name': fields.many2one('res.users', 'Collaborator', required=True),
        'to_notify': fields.boolean('To be notified by mail'),
    }


class hr_department(orm.Model):
    _inherit = 'hr.department'

    _columns = {
        'description': fields.text('Office Description'),
        'assignable': fields.boolean('Office Assignable'),
        'collaborator_ids': fields.one2many(
            'hr.department.collaborator',
            'department_id',
            'Collaborators'
            )
        }

    def write(self, cr, uid, ids, vals, context=None):
        if context is None:
            context = {}
        if not ids:
            return True
        if not hasattr(ids, '__iter__'):
            ids = [ids]

        objsdep = self.browse(cr, uid, ids, context=context)
        for dep in objsdep:
            if dep.manager_id.user_id is not None:
                manager_id = dep.manager_id.user_id.id
                if (
                        vals.get('collaborator_ids') or
                        vals.get('manager_id') or
                        vals.get('type')):
                    if ((uid == SUPERUSER_ID) or (uid == manager_id)):
                        res = super(hr_department, self).write(
                            cr, uid, ids, vals, context
                            )
                    else:
                        raise orm.except_orm(
                            'Error !',
                            "Only the administrator or manager"
                            "can change configuration fields"
                        )
                else:
                    res = super(hr_department, self).write(
                        cr, uid, ids, vals, context)
            else:
                res = super(hr_department, self).write(
                    cr, uid, ids, vals, context)
        return res
