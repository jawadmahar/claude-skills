# Delivery Sales Metrics - Definitions

These definitions apply to food delivery platform reporting (Uber Eats,
Deliveroo, Just Eat) across Mahar Group food businesses (UFO Food Ltd /
Wraps and Wings, Cafe UFO, Mahar Coffee Ltd).

## Core metrics

| Metric | Definition |
|--------|------------|
| **Gross sales** | Total order value **including** promotional discounts. The headline figure before any promo is deducted. |
| **Net sales** | Gross sales **excluding** promotional discounts, i.e. what customers actually paid. `Net = Gross - promo discount`. |
| **Promo discount** | `Gross - Net`. The value of discounts funded against the orders in the period. |
| **Royalty (commission)** | Platform commission, charged on **net sales**. Default 30%, plus VAT at 20%. |
| **Ads** | Sponsored listings / platform marketing spend, plus VAT at 20%. |
| **Payout** | The cash the business actually receives: `Net - (royalty + VAT) - (ads + VAT)`. |
| **Contribution** | `Payout - food cost`. Profit after platform fees, ads and ingredients, **before** labour, rent and other fixed costs. Food cost defaults to 25% of net sales. |

## Formulae

```
promo_discount   = gross - net
royalty_incl_vat = net * royalty_rate * (1 + vat_rate)        # default 0.30, 0.20
ads_incl_vat     = ads * (1 + vat_rate)
payout           = net - royalty_incl_vat - ads_incl_vat
food_cost        = net * food_cost_rate                       # default 0.25
contribution     = payout - food_cost
```

With the default 30% royalty and 20% VAT, royalty consumes **36% of net sales**,
so before ads the payout is **64% of net**. Ads then reduce it further. In
practice the UFO Food data lands at roughly **49% of net** as the final payout.

## Reverse-engineering ad spend

Platform statements do not always split out ad spend cleanly. If the actual
bank payout is known, ad spend (incl VAT) can be derived:

```
ads_incl_vat = net - royalty_incl_vat - actual_payout
```

The `payout_calculator.py` script does this automatically when `actual_payout`
is supplied but `ads` is not.

## Worked example (UFO Food Ltd, June 2026)

| | Wk 1-7 Jun (light promo) | Wk 8-14 Jun (heavy promo) |
|---|---|---|
| Gross sales | £5,589.92 | £7,955.43 |
| Net sales | £4,885.03 | £6,394.03 |
| Promo discount | £704.89 (12.6% of gross) | £1,561.40 (19.6% of gross) |
| Royalty incl VAT | £1,758.61 | £2,301.85 |
| Ads incl VAT (implied) | £769.03 | £961.05 |
| Payout | £2,357.39 (48.3% of net) | £3,131.13 (49.0% of net) |
| Food cost (est, 25%) | £1,221.26 | £1,598.51 |
| Contribution | £1,136.13 | £1,532.62 |

Payouts confirmed from bank transfers: w/e 07 Jun = Uber £1,195.51 + Deliveroo
£1,161.88; w/e 14 Jun = the two "Wraps an" credits (£1,409.71 + £1,721.42).

## Reading the promotion verdict

The comparison answers "are we better off with heavier promotions?" by looking
at **contribution**, not just sales:

- Heavier promo only pays if the **extra net sales it drives** more than cover
  the extra discount, extra commission and extra food cost.
- A deeper discount applied to orders that would have happened anyway is pure
  margin loss. The promo only wins when it brings **incremental orders** - so
  always sense-check order-count growth alongside the figures.
- Two weeks is a directional signal, not proof. Weather, day-of-week mix and
  seasonality also move sales. Track several cycles before fixing a promo
  strategy.
