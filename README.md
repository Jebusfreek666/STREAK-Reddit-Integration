# STREAK — Reddit Integration (Access Request)

**Status: proposed / not approved / not collecting Reddit data.** This public repository documents a limited, read-only Reddit integration proposed for a separate private personal-finance application, STREAK. It is provided for Reddit developer-access review. The full STREAK trading application is **not** published here.

## Purpose

STREAK is a locally operated, private Windows research tool intended to identify U.S.-listed common stocks receiving an unusual increase in *genuine* bullish discussion, initially in **r/wallstreetbets**. Its research seeks to distinguish new conviction from bearish views, sarcasm, option-position language, already-realized gains, repeated messages, and apparent promotions. Reddit signals would be combined with independently sourced market data and risk controls.

Initial output would be **private, read-only research rankings and simulated trades**. If separately validated and enabled later, those rankings might influence **automated purchases and sales in the owner's personal brokerage account**. This intended financial/trading use is disclosed explicitly, even though the software is not sold or distributed. The applicant requests Reddit's determination of whether that use is permitted, restricted, commercial, or requires another agreement.

## Proposed API usage (subject to written approval)

- **Target:** Public submissions and comments in `r/wallstreetbets`, through Reddit-approved programmatic access only.
- **Method:** Read-only, incremental monitoring with bounded calls and rate-limit observance; no posting, voting, DMs, moderation, or user interaction.
- **Fields requested where authorized:** Post/comment IDs, creation timestamps, score, thread context, limited public author signals, and message text necessary for sentiment classification.
- **Analysis:** Ticker detection, deduplication, participant-diversity estimation, time-window momentum, and cautious bullish/bearish/neutral/abstain classification.
- **External processor requested:** OpenAI model for inference-only classification of minimized relevant text, **only if Reddit explicitly authorizes this transfer and any applicable contractual terms are satisfied**. No fine-tuning or model training is planned.
- **Reporting:** Aggregate, private sentiment indicators only; no republishing or licensing Reddit content, and no individual-user dossiers.

## Governance and current blockers

**No approved Reddit API application or scope has been established.** The code in this repository is a small demonstration of intended collection boundaries, **not** a production collector or permission to access Reddit. It refuses collection in the absence of explicit documented approval evidence. Such a local flag is an internal safeguard, **not a replacement for Reddit's approval**.

A real deployment must separately verify: Reddit authorization for the specific financial use, comments, and any external AI processing; approved authentication; per-endpoint rate limits; deletion/retention handling; consent and privacy obligations; continuity/coverage; incident response; and changes to Reddit's terms. If approval is not granted, the Reddit integration will not run. No bypass by scraping or undocumented endpoints is planned.

See [DATA_HANDLING.md](DATA_HANDLING.md) for retention and deletion commitments and [collector_preview.py](collector_preview.py) for a deliberately bounded example. **No credentials, authentication tokens, brokerage integration, trading strategy, or order-writing code is included.**

## Why not Devvit?

STREAK is a standalone Windows service outside Reddit, using a separate private financial research pipeline. The planned workflow includes historical comparison, local processing, optional consented third-party AI inference, and potential personal brokerage trading. We request Reddit's guidance on whether the Data API or an alternative licensed arrangement supports these off-platform and financial-use requirements. We do not claim that Devvit permits the application or that it has been approved.

## Running the offline example

The demonstration tests use only Python's standard library and synthetic fake Reddit objects:

```shell
python -m unittest discover -s tests -v
```

No Reddit API credentials or Internet connection are needed for those tests. The example makes no real API calls without an injected authorized client and explicit approval evidence; there is **no provided live-run script**.

## Contact and scope

This repository is a public technical overview for an access request, not an invitation to use Reddit data. The owner will provide additional details to Reddit privately if required. It is not affiliated with, sponsored by, or endorsed by Reddit, Robinhood, or OpenAI.
