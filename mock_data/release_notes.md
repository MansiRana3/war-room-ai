# Release Notes — Dashboard 2.0
**Release date:** 2026-03-08  
**Version:** 4.2.0  
**Rolled out to:** 100% of users

## What changed
- Complete redesign of the main dashboard with real-time data widgets
- New payment flow with one-click checkout
- Rebuilt API layer for faster data fetching
- New onboarding checklist for first-time users

## Known risks at time of launch
- The new API layer was only load-tested up to 60% of expected traffic
- One unresolved bug in the payment module on iOS 17.4 (marked low priority)
- Database migration was done live — no rollback snapshot was taken
- Third-party analytics SDK was updated same day (not isolated)

## Rollback plan
- Partial rollback possible for the API layer only
- Full rollback requires 4–6 hours of manual database work
- No feature flag in place — rollback affects all users simultaneously

## Sign-off
- Engineering lead: approved
- QA: approved with noted exceptions
- Security review: pending (waived for timeline)