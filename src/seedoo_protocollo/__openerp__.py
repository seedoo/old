# -*- coding: utf-8 -*-
# This file is part of Seedoo.  The COPYRIGHT file at the top level of
# this module contains the full copyright notices and license terms.

{
    'name': 'Protocollo',
    'version': '1.0',
    'author': 'Innoviu',
    'category': 'Document Management',
    'sequence': 23,
    'summary': 'Gestione Protocollo Informatico',
    'description': """
Seedoo personalization for Public Administrations
==================================================

Manages the protocol of a Public Administration


Configuration
=============

Add your user to 'Allowed Users' of 'Registro Ufficiale'.
Set 'Codice Identificativo Area' for your company. # TODO: l10n_it_ipa

Add at least one user to 'manager sensible data protocollo'.

Create a directory tree , set openerp user as its owner and
copy the files contained in 'extras' to 'new dir path'
Set the script 'signature.sh' as executable

Configure odoo system parameter and create an new record with
Key = itext.location
Value = 'your/dir/path'

Configure ir.attachment.location
""",
    'author': 'Innoviu Srl',
    'website': 'http://www.innoviu.com',
    'depends':
        [
            'base',
            'l10n_it_pec',
            'document',
            'hr',
            'email_template',
            'report_webkit',
            'seedoo_gedoc',
            'l10n_it_pec_messages',
            'seedoo_base_ipa',
            'm2o_tree_widget'],
    'data':
        [
            'security/protocollo_security.xml',
            'security/protocollo_security_rules.xml',
            'security/ir.model.access.csv',
            'data/protocollo_sequence.xml',
            'data/protocollo_data.xml',
            'gedoc/data/gedoc_data.xml',
            'wizard/cancel_protocollo_wizard_view.xml',
            'wizard/modify_protocollo_wizard_view.xml',
            'wizard/create_protocollo_pec_wizard_view.xml',
            'wizard/modify_protocollo_pec_wizard_view.xml',
            'view/offices_view.xml',
            'view/company_view.xml',
            'view/ir_attachment_view.xml',
            'view/protocollo_view.xml',
            'view/mail_pec_view.xml',
            'view/contact_view.xml',
            'gedoc/view/gedoc_view.xml',
            'wizard/create_journal_wizard_view.xml',
            'wizard/create_emergency_registry_wizard_view.xml',
            'workflow/protocollo_workflow.xml',
            'data/protocollo_report.xml'],
    'demo': [
        'demo/data.xml',
        ],
    'installable': True,
    'application': True,
    'active': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
