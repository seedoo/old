# -*- coding: utf-8 -*-
# This file is part of Seedoo.  The COPYRIGHT file at the top level of
# this module contains the full copyright notices and license terms.

{
    'name': 'Pdf Viewer Widget',
    'description': '''
This module add a pdf preview to binary data

This module works with OpenERP 7.0.
''',
    'version': '7.0.1',
    'author': 'Innoviu Srl',
    'category': 'Usability',
    'website': 'https://www.innoviu.com',
    'license': 'AGPL-3',
    'depends': [
        'web',
        ],
    'python': ['magic'],
    'js': ['static/src/js/web_pdf_widget.js'],
    'qweb': ['static/src/xml/web_pdf_widget.xml'],
    'installable': True,
    'auto_install': False,
}
