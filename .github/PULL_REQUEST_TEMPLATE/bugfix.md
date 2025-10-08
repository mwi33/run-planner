# Bugfix Summary
Concise description of the bug and fix.


## Steps to Reproduce
1. …
2. …
3. …


## Root Cause Analysis
What caused it? Include a brief technical explanation.


## Fix Approach
What changed and why this is safe.


## Regression Coverage
- [ ] Added/updated tests that fail without this fix
- [ ] Negative tests where relevant


## Verification
- [ ] Local reproduce → fix verified
- [ ] `pytest -q` passes
- [ ] `pre-commit run --all-files`


## Impact / Risk
User‑facing changes? Performance? Data migration?


## Rollback Plan
How to revert safely if needed.


## Checklist
- [ ] CI green
- [ ] Linked issue(s)
- [ ] Docs updated if behavior changed
- [ ] Ready for review (remove Draft)