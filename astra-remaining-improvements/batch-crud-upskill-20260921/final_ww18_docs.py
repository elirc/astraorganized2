from pathlib import Path
P=Path(__file__).resolve().parent.parent/'stage/b17f4c546008/astraupskill'
for p in P.glob('*.md'):
 t=p.read_text().replace("'''",'').replace(".''",'.').replace('Root’s pure lab','The pure lab').replace('root-owned','captured').replace('root-provided','recorded')
 t=t.replace('allowed quantity and threshold edges','allowed lifecycle edges and exact discount thresholds').replace('allowed threshold edges','exact discount thresholds')
 t=t.replace('because the service approval plan treats deal-desk discounting as finance-sensitive','because the policy result treats deal-desk discounting as finance-sensitive')
 if p.name=='VERIFICATION.md':t+='\nRun `node --experimental-vm-modules --test tests/quote-transition-policy.test.mjs` from the project directory. Quantity min/max behavior is inspected source and an exercise; the captured cases do not comprehensively test both quantity endpoints. The exact money examples use 10,000 base cents, 9,000 and 8,000 threshold prices, and 7,900 above-threshold pricing.\n'
 if p.name=='05-PRACTICE.md':t='''# Graded practice

Work these without the solutions open. For each answer, identify the exact comparison or arithmetic expression in quote-policy.ts, predict the return value or statusCode, and distinguish source inspection from a case executed by the captured lab.

Exercise one: a rule covers quantities 5 through 10. Predict selection at 5, 10, and 11. Explain why a missing applicable rule differs from a missing product.

Exercise two: base price is 12,000 cents, submitted price is 10,800 and quantity is 3. Compute subtotal, total, discount cents and discount percentage. Show units beside every number.

Exercise three: floor is 8,000. Compare submitting 8,000 and 7,999. Identify where execution stops in the failing case.

Exercise four: deal-desk threshold is 15, finance threshold is 10, discount is 20. Predict flags, then add an unsupported contract term.

Exercise five: remove the product from the supplied catalog. Predict whether totals exist.

Exercise six: compare DRAFT to PENDING_APPROVAL with CONVERTED_TO_ORDER to APPROVED.

Exercise seven: explain which service and repository operations would be needed to turn the returned flags into persisted approvals. Design one failure-injection test for that integration; do not claim the pure lab executes it.
'''
 p.write_text(t,encoding='utf-8')
