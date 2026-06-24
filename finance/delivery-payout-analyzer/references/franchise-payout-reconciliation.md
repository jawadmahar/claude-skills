# Franchise payout reconciliation (W&W -> UFO Food Ltd)

UFO Food Ltd trades as a **Wraps & Wings (Eatphoria) franchisee**. The delivery
platforms pay the franchisor (W&W); W&W deducts a royalty and pays the store.
So the payout has THREE layers, not two.

## The waterfall (per £1 of net delivery sales)

Customer order -> **platform (Uber/Deliveroo) takes commission + ads + VAT** ->
W&W receives the remainder -> **W&W takes royalty + VAT** -> store payout.

## Four invoices reconciled (May-Jun 2026)

| Invoice | Platform | Period | Gross | Disc | Net | W&W roy+VAT | Payout | Platform take | Payout % net |
|---------|----------|--------|------:|-----:|----:|------------:|-------:|--------------:|-------------:|
| ERP-2371 | Uber | 01-07 Jun | 2,472.85 | 270.76 | 2,202.09 | 121.45 | 1,195.51 | 885.13 (40.2%) | 54.3% |
| ERP-2306 | Deliveroo | 25-31 May | 2,418.08 | 0.00 | 2,439.28 | 143.81 | 1,555.61 | 739.86 (30.3%) | 63.8% |
| ERP-2271 | Uber | 25-31 May | 2,225.96 | 249.80 | 1,976.16 | 109.50 | 1,112.59 | 754.07 (38.2%) | 56.3% |
| ERP-2202 | Uber | 18-24 May | 3,039.29 | 529.17 | 2,510.12 | 140.90 | 1,441.10 | 928.12 (37.0%) | 57.4% |

W&W franchise royalty is consistently **~4.6-4.9% of net + 20% VAT** - small and
contractual, NOT the 30% sometimes assumed for "royalty".

## Full decomposition - Uber, 01-07 Jun (commission 25% contracted, ad spend known = £132.95)

| Layer | Amount | % of net | Reclaimable? |
|-------|-------:|---------:|--------------|
| Net sales | 2,202.09 | 100% | - |
| Uber commission (contracted 25%) | 550.52 | 25.0% | no (real cost) |
| Uber ads | 132.95 | 6.0% | no (real cost) |
| **Other Uber fees (unexplained)** | 54.14 | 2.5% | no - query this |
| Uber VAT | 147.52 | 6.7% | **yes - reclaimed** |
| W&W royalty | 101.21 | 4.6% | no (real cost) |
| W&W VAT | 20.24 | 0.9% | **yes - reclaimed** |
| **Store payout** | **1,195.51** | **54.3%** | - |

Commission is contracted at **25%** (Uber and Deliveroo). With that fixed, the
implied Uber take still runs **37-40% of net**, so beyond 25% commission + ~6% ads
there is a residual of roughly **2.5-3% of net (~£55-145/week) in unexplained
"other" Uber fees** plus reclaimable VAT. That residual is the line to itemise
with the platform/franchisor.

- Real cost (ex reclaimable VAT): ~37-38% of net.
- Reclaimable VAT: ~7.6% of net - returns on the VAT return, not a true loss.

## Where the money goes (answering "where is the 14% leaking?")

Nothing is unaccounted for. Beyond the assumed 30% commission + 7% ads, the rest is:
- **~5% W&W franchise royalty** (+ VAT) - contractual, fixed
- **~7-8% VAT** on platform + franchise charges - **reclaimable**, returns on the VAT return
- platform commission/fees sitting slightly above the round 30%

The only genuinely controllable leaks are:
1. **Ad spend** - especially Deliveroo (ROAS ~2x vs Uber ~9x).
2. **Discounts** - £270-529 per Uber week (11-17% of gross). Confirm whether these
   are merchant-funded or platform-funded ("30% funded by Uber" offers cost the
   store nothing; merchant-funded ones are a real, controllable cost).

## Flags to query with the franchisor

- **Two different billing entities.** Invoices ERP-2371/2306/2271 are from
  "Wraps & Wings Ltd, 73 Cornhill, London, VAT 518154790"; invoice ERP-2202 is
  from "130A Bethnal Green Road, London, VAT 372335012" - a different address and
  VAT number under the same trading name. Worth confirming which entity is the
  correct counterparty.
- Ask for an itemised breakdown of the platform deduction (commission vs ads vs
  fees) so it is not bundled invisibly before the W&W invoice.
