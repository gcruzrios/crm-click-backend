from decimal import Decimal


def calculate_quote(
    items: list,
    discount_amount: float,
    tax_rate: float,
) -> tuple[float, float, float]:
    subtotal = sum(float(item.quantity) * float(item.unit_price) for item in items)
    taxable = subtotal - float(discount_amount)
    tax_amt = taxable * (float(tax_rate) / 100)
    total = taxable + tax_amt
    return round(subtotal, 2), round(tax_amt, 2), round(total, 2)


def compute_line_total(quantity: float, unit_price: float) -> float:
    return round(float(quantity) * float(unit_price), 2)
