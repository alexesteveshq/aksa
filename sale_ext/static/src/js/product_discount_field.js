/** @odoo-module **/

import { registry } from "@web/core/registry";
import { ProductDiscountField } from "@sale/js/product_discount_field";
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { _lt } from "@web/core/l10n/translation";

class ProductFieldAvg extends ProductDiscountField{
    onChange(ev) {
        const x2mList = this.props.record.model.root.data.order_line;
        const orderLines = x2mList.records.filter(line => !line.data.display_type);

        if (orderLines.length < 3) {
            return;
        }

        const isFirstOrderLine = this.props.record.data.id === orderLines[0].data.id;
        if (isFirstOrderLine && sameValueAvg(orderLines)) {
            this.dialogService.add(ConfirmationDialog, {
                body: _lt("Do you want to apply this value to all lines ?"),
                confirm: () => {
                    const commands = orderLines.slice(1).map((line) => {
                        return {
                            operation: "UPDATE",
                            record: line,
                            data: {["avg_price_calc"]: Number(ev.target.value)},
                        };
                    });

                    x2mList.applyCommands('order_line', commands);
                },
            });
        }
    }
}

export function sameValueAvg(orderLines) {
    const compareValue = orderLines[1].data.avg_price_calc;
    return orderLines.slice(1).every(line => line.data.avg_price_calc === compareValue);
}

ProductFieldAvg.components = { ConfirmationDialog };
ProductFieldAvg.template = "sale.ProductDiscountField";

registry.category("fields").add("sol_avg", ProductFieldAvg)