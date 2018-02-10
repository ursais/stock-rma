# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class RmaOrder(models.Model):
    _inherit = "rma.order"

    @api.multi
    def _compute_po_count(self):
        for rec in self:
            po_count = 0
            for line in rec.rma_line_ids:
                po_count += len(self.env['purchase.order'].search(
                    [('origin', '=', line.name)]).ids)
            rec.po_count = po_count

    @api.multi
    def _compute_origin_po_count(self):
        for rma in self:
            purchases = rma.mapped(
                'rma_line_ids.purchase_order_line_id.order_id')
            rma.origin_po_count = len(purchases)

    po_count = fields.Integer(
        compute='_compute_po_count', string='# of PO')
    origin_po_count = fields.Integer(
        compute='_compute_origin_po_count', string='# of Origin PO')

    @api.multi
    def action_view_purchase_order(self):
        action = self.env.ref('purchase.purchase_rfq')
        result = action.read()[0]
        po_ids = self.env['purchase.order'].search(
            [('origin', '=', self.name)]).ids
        if not po_ids:
            raise ValidationError(_("No purchase order found!"))
        result['domain'] = [('id', 'in', po_ids)]
        return result

    @api.multi
    def action_view_origin_purchase_order(self):
        action = self.env.ref('purchase.purchase_rfq')
        result = action.read()[0]
        po_ids = self.mapped(
            'rma_line_ids.purchase_order_line_id.order_id').ids
        if not po_ids:
            raise ValidationError(_("No purchase order found!"))
        result['domain'] = [('id', 'in', po_ids)]
        return result
