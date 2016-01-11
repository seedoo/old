# -*- coding: utf-8 -*-
# This file is part of Seedoo.  The COPYRIGHT file at the top level of
# this module contains the full copyright notices and license terms.
import unittest
from lxml import etree

# from seedoo_protocollo.segnatura.segnatura_xml import SegnaturaXML
from segnatura_xml import SegnaturaXML
# from openerp.tests import common


# class TestModelA(common.TransactionCase):
#     def test_some_action(self):
#         """
#         Testing send pdf File and protocol it
#         with signature as typology_rac
#         """
#         cr, uid = self.cr, self.uid
#         partner_id = self.getIdDemoObj('base', 'main_partner')
#         racc_id = self.getIdDemoObj('', 'protocollo_typology_rac')
#         com_varie_id = self.getIdDemoObj('', 'protocollo_classification_6')
#         send_rec_id = self.modelProtSendRec.create(
#             cr, uid,
#             {
#                 'name': 'test_partner',
#                 'type': 'individual',
#                 'partner_id': partner_id
#             }
#         )
#         prot_id = self.modelProtocollo.create(
#             cr, uid,
#             {
#                 'type': 'out',
#                 'subject': 'test out',
#                 'typology': racc_id,
#                 'sender_receivers': [(4, send_rec_id)],
#                 'classification': com_varie_id,
#                 'datas_fname': 'test0',
#                 'datas': self.getCopyOfFile('test0', 'test_doc_src.pdf')[1],
#                 'mimetype': 'application/pdf'
#             }
#         )
#         self.assertTrue(bool(prot_id))
#         prot_obj = self.modelProtocollo.browse(cr, uid, prot_id)
#         self.assertEqual(prot_obj.state, 'draft')
#         self.assertEqual(prot_obj.fingerprint, False)
#         self.wf_service.trg_validate(
#             uid, 'protocollo.protocollo', prot_id, 'register', cr)
#         prot_obj.refresh()
#         self.assertEqual(prot_obj.state, 'registered')
#         prot_name = 'Protocollo_0000001_%d' % prot_obj.year
#         self.assertEqual(prot_obj.doc_id.name, prot_name)
#         sha1 = self.sha1OfFile(prot_obj.doc_id.id)
#         self.assertEqual(prot_obj.fingerprint, sha1)

class TestXmlGeneration(unittest.TestCase):

    def test_0_prova(self):
        print "xml generation test init"
        dtdfile = open("../data/segnatura.dtd", 'r')
        examplefile = open("../data/esempio.xml", 'r')
        exampleXML = etree.parse(examplefile)
        dtd = etree.DTD(dtdfile)

        segnaturaXml = SegnaturaXML(None)
        root = segnaturaXml.generate_segnatura_root()
        dtd.validate(root)

        # dtd.validate(exampleXML)
        print dtd.error_log.filter_from_errors()
        # self.assertTrue(dtd.validate(root))

        print dtdfile.readlines()


