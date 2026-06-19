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
| **Contribution** | `Payout - food cost`. Profit after platform fees, ads and ingredients, **before** labour, rent and other fixed costs. Food cost defaults to 33% of net sales. |
| **In-store sales** | EPOS sales (inc VAT, after discount). No platform commission or ads apply, so in-store contribution = `in-store sales x (1 - food cost rate)`. |
| **Total sales** | `Delivery net + in-store sales` (inc VAT). The base for the labour-cost ratio, since labour serves both channels. |
| **Labour cost** | `Labour hours x hourly rate` (or a direct cost). Expressed as a % of total sales. |
| **Contribution after labour** | `Delivery contribution + in-store contribution - labour cost`. The closest figure to operating profit, but still **before** VAT remittance, rent, utilities, packaging and card fees. |

## Formulae

```
promo_discount   = gross - net
royalty_incl_vat = net * royalty_rate * (1 + vat_rate)        # default 0.30, 0.20
ads_incl_vat     = ads * (1 + vat_rate)
payout           = net - royalty_incl_vat - ads_incl_vat
food_cost        = net * food_cost_rate                       # default 0.33
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
| Payout (delivery) | £2,357.39 (48.3% of net) | £3,131.13 (49.0% of net) |
| Food cost on delivery (33%) | £1,612.06 | £2,110.03 |
| Delivery contribution | £745.33 | £1,021.10 |
| In-store sales (inc VAT) | £2,072.67 | £1,526.05 |
| In-store contribution (67%) | £1,388.69 | £1,022.45 |
| Kiosk sales (inc VAT) | £430.00 | £277.00 |
| Kiosk contribution (67%) | £288.10 | £185.59 |
| Total sales (inc VAT) | £7,387.70 | £8,197.08 |
| Contribution before labour | £2,422.12 | £2,229.14 |
| Labour | 233 hrs = £2,330 (31.5%) | 221 hrs = £2,210 (27.0%) |
| **Contribution after labour** | **£92.12** | **£19.14** |

Payouts confirmed from bank transfers: w/e 07 Jun = Uber £1,195.51 + Deliveroo
£1,161.88; w/e 14 Jun = the two "Wraps an" credits (£1,409.71 + £1,721.42).
Labour: 233 / 221 staff hours at £10/hr. In-store from EPOS (ValueIncVAT);
kiosk sales added separately (same 67% contribution, no commission).

> **VAT and fixed costs are NOT in these figures.** Contribution after labour
> is before VAT remitted to HMRC, rent, utilities, packaging and card fees.
> Once the high-margin in-store and kiosk channels are included, the LIGHT-promo
> week is the more profitable of the two: the heavy-promo week grew low-margin
> delivery but lost higher-margin in-store and kiosk sales (apparent
> cannibalisation), leaving it worse off after labour - see "Reading the verdict".

## Food cost validation (bank statement, 19 Mar - 18 Jun 2026)

The 33% food cost assumption was checked against ~3 months of UFO Food bank data
using `food_cost_from_statement.py`:

- Ingredients (Bidfood/3663 £16,052, Brakes £9,328, Danbury Oils, Korea Foods,
  Tuk Tuk Mart, Tesco/Iceland): £26,057
- Packaging / consumables (Amazon): £787
- wrapswings.store nominated-supplier portal (branded packaging + nominated food
  lines, i.e. COGS): £6,207
- **Total COGS: £33,051**
- Net sales (reconstructed): ~£101,027
- **Food cost: ~33% of net sales** - confirms the 33% assumption.

Caveats: purchases not consumption (stock timing), reconstructed sales (delivery
payouts grossed up at ~49% + in-store sweeps + own-app), and mixed VAT rating on
food. For an exact figure, feed real EPOS + platform net sales via `--sales`.

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
