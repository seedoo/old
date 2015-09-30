# -*- coding: utf-8 -*-
# This file is part of Seedoo.  The COPYRIGHT file at the top level of
# this module contains the full copyright notices and license terms.

from openerp.osv import fields, osv
from openerp.osv.orm import except_orm
from openerp.tools.translate import _
from openerp.addons.base.ir.ir_attachment import ir_attachment as ir_att
from openerp.modules.registry import RegistryManager
from openerp import SUPERUSER_ID
import logging
import os
import re
_logger = logging.getLogger(__name__)


class ir_attachment(osv.Model):
    _inherit = 'ir.attachment'

    def _full_path(self, cr, uid, location, path):
        # location = 'file:filestore'
        assert location.startswith('file:'), \
            "Unhandled filestore location %s" % location
        location = location[5:]

        # sanitize location name and path
        location = re.sub('[.]', '', location)
        location = location.strip('/\\')

        path = re.sub('[.]', '', path)
        path = path.strip('/\\')
        return os.path.join('/', location, cr.dbname, path)

    def _get_full_path(self, cr, uid, ids, location):
        # TODO check if removable
        if not location:
            raise except_orm(
                _('Error'), _('Please set ir_attachment.location'))
        res = self.read(cr, uid, ids, ['res_model'])
        locations = {}
        for model_location in res:
            if model_location['res_model'] == 'protocollo.protocollo':
                # TODO insert here new path for fake document
                # if the protocol is reserved and state not draft
                location_def = location + '/protocollazioni'
            elif model_location['res_model'] == 'protocollo.protocollo.imp':
                location_def = location + '/sinekarta'
            else:
                location_def = location
            locations[model_location['id']] = location_def
        return locations

    def _data_get(self, cr, uid, ids, name, arg, context=None):
        if context is None:
            context = {}
        result = {}
        location = self.pool.get('ir.config_parameter').\
            get_param(cr, uid, 'ir_attachment.location')
        locations = self._get_full_path(cr, uid, ids, location)
        bin_size = context.get('bin_size')
        for attach in self.browse(cr, uid, ids, context=context):
            if location and attach.store_fname:
                result[attach.id] = self._file_read(
                    cr,
                    uid,
                    locations[attach.id],
                    attach.store_fname,
                    bin_size)
            else:
                result[attach.id] = attach.db_datas
        return result

    def _data_set(self, cr, uid, aid, name, value, arg, context=None):
        # We dont handle setting data to null
        if not value:
            return True
        if context is None:
            context = {}
        location = self.pool.get('ir.config_parameter').\
            get_param(cr, uid, 'ir_attachment.location')
        location = self._get_full_path(cr, uid, [aid], location)[aid]
        file_size = len(value.decode('base64'))
        if location:
            attach = self.browse(cr, uid, aid, context=context)
            if attach.store_fname:
                self._file_delete(cr, uid, location, attach.store_fname)
            fname = self._file_write(cr, uid, location, value)
            # SUPERUSER_ID as probably don't have write access,
            # trigger during create
            super(ir_attachment, self).write(cr, SUPERUSER_ID, [aid],
                                             {'store_fname': fname,
                                              'file_size': file_size},
                                             context=context)
        else:
            super(ir_attachment, self).write(cr, SUPERUSER_ID, [aid],
                                             {'db_datas': value,
                                              'file_size': file_size},
                                             context=context)
        return True

    _columns = {
        'is_protocol': fields.boolean('Doc Protocollo'),
        'reserved': fields.boolean('Doc Riservato'),
        'datas': fields.function(
            _data_get,
            fnct_inv=_data_set,
            string='File Content',
            type="binary",
            nodrop=True),
    }

    def check(self, cr, uid, ids, mode, context=None, values=None):
        """Overwrite check to verify protocol attachments"""
        if not isinstance(ids, list):
            ids = [ids]

        super(ir_attachment, self).check(cr, uid, ids, mode,
                                         context=context, values=values)
        res = []
        if mode != 'read':
            if ids:
                cr.execute('SELECT DISTINCT res_model, res_id \
                    from ir_attachment \
                    WHERE id in %s', (tuple(ids),))
                res = cr.fetchall()
            elif values:
                res.append([values['res_model'], values['res_id']])
            else:
                pass
            for res_model, res_id in res:
                if res_model == 'protocollo.protocollo':
                    cr.execute('SELECT state from protocollo_protocollo \
                        WHERE id = %s', (str(res_id),))
                    state = cr.fetchone()[0]
                    if state != 'draft':
                        raise except_orm(_('Operazione non permessa'),
                                         'Si sta cercando di modificare un \
                                         protocollo registrato')

    def unlink(self, cr, uid, ids, context=None):
        if isinstance(ids, (int, long)):
            ids = [ids]
        self.check(cr, uid, ids, 'unlink', context=context)
        location = self.pool.get('ir.config_parameter').get_param(
            cr, uid, 'ir_attachment.location')
        if location:
            for attach in self.browse(cr, uid, ids, context=context):
                location = self._get_full_path(
                    cr, uid, [attach.id], location
                    )[attach.id]
                if attach.store_fname:
                    self._file_delete(cr, uid, location, attach.store_fname)
        return super(ir_att, self).unlink(cr, uid, ids, context)

