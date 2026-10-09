# Proposed data handling and privacy controls

**Proposed commitments only.** No programmatic Reddit collection has been authorized or conducted by this repository.

1. **Read-only least privilege.** Access only approved public content and only the fields needed for the declared research purpose. Never post, vote, message users, access private communities, or seek deleted/private content.
2. **Minimize raw text.** Retain text only in protected volatile memory as needed for classification and quality checks. Raw text will not be publicly redistributed or persisted to ordinary output logs. Any archival retention would require explicit Reddit permission and a documented retention period.
3. **Author privacy.** Use limited public author information if authorized. Where participant diversity is needed, replace usernames with short-lived keyed pseudonyms. Avoid identity linking, sensitive profiling, and cross-platform enrichment.
4. **Updates and removals.** Design an authorized deletion/update synchronization process. Remove affected raw content, derivative records traceable to deleted source material, and cached references as required by Reddit's policies. An item missing from a capped listing is not assumed deleted.
5. **External AI.** Do not transmit Reddit text to a third-party AI provider without explicit Reddit permission covering inference-only processing and relevant privacy, retention, and contractual terms. No training/fine-tuning on Reddit text is intended.
6. **Coverage/rate limits.** Observe quotas and back off upon rate-limit or access errors. Incomplete, stale, disconnected, or censored collections are labeled partial and are not reported as comprehensive Reddit sentiment.
7. **Protection.** Never commit client secrets, authorization codes, access tokens, real user-level raw data, or brokerage credentials. Credentials would be stored separately using protected local storage, with no credential output in logs.
8. **Purpose restriction.** Use data only within the approved Reddit scope. Financial-trading linkage and any required commercial authorization must be explicitly resolved by Reddit before data is used for that purpose.
9. **No Reddit-facing service.** The planned app is private research; no direct moderation or Reddit-user benefits are claimed.

Approval status today: **pending / not granted**. The prototype below is demonstrative, and its evidence gate is not itself proof of legal or contractual authorization.
