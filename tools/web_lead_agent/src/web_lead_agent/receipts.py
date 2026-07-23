"""回执解析：成功、失败、未知；未知不自动重试。"""

from __future__ import annotations

from web_lead_agent.contracts import SendReceipt


SUCCESS_MARKERS = ("success", "thank you", "received", "submitted", "message sent")


def receipt_from_http(
    target_url: str,
    idempotency_key: str,
    http_status: int | None,
    body: str,
    error: str = "",
) -> SendReceipt:
    if error:
        return SendReceipt(
            status="FAILED",
            http_status=http_status,
            target_url=target_url,
            idempotency_key=idempotency_key,
            reason=error,
            retry_scheduled=False,
        )
    if http_status is not None and http_status >= 400:
        return SendReceipt(
            status="FAILED",
            http_status=http_status,
            target_url=target_url,
            idempotency_key=idempotency_key,
            reason=f"http_status:{http_status}",
            retry_scheduled=False,
        )
    lowered = body.lower()
    if any(marker in lowered for marker in SUCCESS_MARKERS):
        return SendReceipt(
            status="SUCCESS",
            http_status=http_status,
            target_url=target_url,
            idempotency_key=idempotency_key,
            reason="success_marker_detected",
            retry_scheduled=False,
        )
    return SendReceipt(
        status="UNKNOWN",
        http_status=http_status,
        target_url=target_url,
        idempotency_key=idempotency_key,
        reason="no_success_marker",
        retry_scheduled=False,
    )
