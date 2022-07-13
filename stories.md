# Stories to create unit tests

TAX = 30%

1. Got 600 EUR transfer for a European invoice (500 EUR gros; 20% * 500 EUR = 100 EUR VAT)
  -> 100 EUR VAT --> pay to the treasury
  -> 30% x 500 EUR of income tax --> pay to the tax office (different transfer destination than VAT)
  -> 70% x 500 EUR of income net --> transfer to my personal bank account
  
2. The same, but paid 10% of gros income (10% * 500 EUR = 50 EUR) of costs (e.g. freelance platform). They also collected 20% of the cost (20% * 50 EUR = 10 EUR) as VAT (that they paid to the treasery).
  -> 100 EUR - 10 EUR = 90 EUR VAT --> pay to the treasury
  -> tax: I pay the tax based on the gros income no matter if I have costs or not (VARIANT A); most companies pay tax on (gros income - costs) (VARIANT B):
      -> VARIANT A: 30% x 500 EUR of income tax --> pay to the tax office
      -> VARIANT B: 30% x (500 EUR - 50 EUR = 450 EUR) of income tax --> pay to the tax office
  -> 50 EUR + 10 EUR VAT --> I need to pay as costs
  -> VARIANT A:
      -> ... what's left I can get as salary
  -> VARIANT B:
      -> ... what's left I can get as salary
      
3. Ticket/hotel reimbursement of 500 EUR
  -> Just transfer back to my personal account 500 EUR
  
4. Overseas invoice (like 1. but without VAT)

5. Like 1 + 2

6. Like 4 + 2.

7. Integration of the above to get the expected summary of
  - how much I need to pay the costs
  - VAT
  - tax
  - can transfer to my personal account (salary net + reimbursements)
