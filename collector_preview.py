"""Review-only sketch of STREAK's proposed *read-only* public-Reddit adapter.

No credentials, API client construction, scheduler, storage, AI, or trading actions.
A separately approved, authenticated PRAW read-only client would be injected.
Local policy values DO NOT substitute for approval from Reddit.
"""
from __future__ import annotations

import hashlib
import hmac
from datetime import datetime, timedelta, timezone
from typing import Any, Mapping


class PermissionRequired(RuntimeError):
    """Fail closed unless Reddit permissions have been independently verified."""


def require_approval(evidence: Mapping[str, Any], *, include_comments: bool) -> None:
    if not evidence.get("reddit_approval_reference"):
        raise PermissionRequired("WRITTEN_REDDIT_APPROVAL_REFERENCE_REQUIRED")
    if evidence.get("public_posts_approved") is not True:
        raise PermissionRequired("POSTS_SCOPE_NOT_APPROVED")
    if evidence.get("personal_financial_use_approved") is not True:
        raise PermissionRequired("FINANCIAL_USE_SCOPE_NOT_APPROVED")
    if include_comments and evidence.get("comments_approved") is not True:
        raise PermissionRequired("COMMENTS_SCOPE_NOT_APPROVED")
    # External AI permission must be checked separately *before* transmission.


def normalized_record(item: Any, *, kind: str, received: datetime, author_key: bytes) -> dict:
    """Normalize only authorized public content. Text stays in caller memory."""
    if kind not in ("post", "comment"):
        raise ValueError("UNKNOWN_KIND")
    if received.tzinfo is None or len(author_key) < 32:
        raise ValueError("UTC_TIMESTAMP_AND_32_BYTE_KEY_REQUIRED")
    created = datetime.fromtimestamp(float(item.created_utc), tz=timezone.utc)
    if created > received.astimezone(timezone.utc):
        raise ValueError("FUTURE_POST_TIME")
    author = getattr(item, "author", None)
    author_hash = None if author is None else hmac.new(
        author_key, str(author).casefold().encode("utf-8"), hashlib.sha256
    ).hexdigest()
    body = str(getattr(item, "selftext" if kind == "post" else "body", "") or "")
    removed = body in ("[deleted]", "[removed]") or bool(getattr(item, "removed_by_category", None))
    text = (str(getattr(item, "title", "")) + "\n" + body).strip() if kind == "post" else body
    return {
        "source_id": ("t3_" if kind == "post" else "t1_") + str(item.id),
        "kind": kind,
        "created_at": created.isoformat(),
        "received_at": received.astimezone(timezone.utc).isoformat(),
        "author_pseudonym": author_hash,
        "removed": removed,
        "text_in_memory_only": "" if removed else text,
    }


def collect_preview(
    read_only_client: Any,
    approval_evidence: Mapping[str, Any],
    *,
    author_key: bytes,
    post_limit: int = 25,
    include_comments: bool = False,
    now: datetime | None = None,
) -> tuple[list[dict], dict]:
    """Bounded example. Does not persist Reddit text or claim complete coverage."""
    require_approval(approval_evidence, include_comments=include_comments)
    if not getattr(read_only_client, "read_only", False):
        raise PermissionRequired("CLIENT_MUST_BE_READ_ONLY")
    if not 1 <= post_limit <= 100:
        raise ValueError("POST_LIMIT_OUT_OF_BOUNDS")
    now = now or datetime.now(timezone.utc)
    cutoff = now - timedelta(hours=24)
    records = []
    visited = set()
    for post in read_only_client.subreddit("wallstreetbets").new(limit=post_limit):
        p = normalized_record(post, kind="post", received=now, author_key=author_key)
        if datetime.fromisoformat(p["created_at"]) < cutoff:
            break
        if p["source_id"] not in visited:
            records.append(p)
            visited.add(p["source_id"])
        # Comments deliberately not implemented in this minimal public example.
        # Approval for comments is still required to request that scope.
    return records, {
        "sample_only": True,
        "coverage_complete": False,
        "rate_limits_and_deletions_not_proven": True,
        "external_ai_transmission_permitted": False,
        "trading_enabled": False,
    }
