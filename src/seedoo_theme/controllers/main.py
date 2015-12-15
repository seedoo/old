# -*- coding: utf-8 -*-
# This file is part of Seedoo.  The COPYRIGHT file at the top level of
# this module contains the full copyright notices and license terms.

from openerp.addons.web import controllers
controllers.main.html_template = controllers.main.html_template.replace(
    "/web/static/src/img/favicon.ico", "/seedoo_theme/static/src/img/favicon.ico"
    ).replace("<title>OpenERP</title>", "<title>Seedoo</title>")
