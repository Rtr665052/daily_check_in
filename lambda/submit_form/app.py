import json
import os
from datetime import datetime, timezone
import boto3

TABLE_NAME = os.environ.get("TABLE_NAME", "").strip()

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME) if TABLE_NAME else None


def build_response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "content-type",
            "Access-Control-Allow-Methods": "POST, OPTIONS"
        },
        "body": json.dumps(body)
    }


def lambda_handler(event, context):
    method = (
        event.get("requestContext", {})
        .get("http", {})
        .get("method", "")
    )

    if method == "OPTIONS":
        return build_response(200, {"message": "OK"})

    if not TABLE_NAME or table is None:
        return build_response(500, {
            "message": "Submission failed",
            "error": "TABLE_NAME environment variable is missing"
        })

    try:
        raw_body = event.get("body") or "{}"

        # handle base64-encoded bodies just in case
        if event.get("isBase64Encoded"):
            import base64
            raw_body = base64.b64decode(raw_body).decode("utf-8")

        body = json.loads(raw_body)

        token_raw = body.get("token")
        if not token_raw:
            return build_response(400, {"message": "Missing token"})

        # token may already be a dict, or it may be a JSON string
        if isinstance(token_raw, str):
            try:
                token = json.loads(token_raw)
            except json.JSONDecodeError:
                return build_response(400, {"message": "Invalid token format"})
        elif isinstance(token_raw, dict):
            token = token_raw
        else:
            return build_response(400, {"message": "Invalid token format"})

        person_id = token.get("person_id")
        token_date = token.get("date")
        submission_date = body.get("date")

        if not person_id:
            return build_response(400, {"message": "Missing person_id in token"})

        if not submission_date:
            return build_response(400, {"message": "Missing submission date"})

        if token_date != submission_date:
            return build_response(400, {"message": "Token date mismatch"})

        item = {
            "person_id": person_id,
            "submission_date": submission_date,
            "nutrition_score": body.get("nutrition_score"),
            "nutrition_notes": body.get("nutrition_notes", ""),
            "finances_score": body.get("finances_score"),
            "finances_notes": body.get("finances_notes", ""),
            "mental_score": body.get("mental_score"),
            "mental_notes": body.get("mental_notes", ""),
            "submitted_at": datetime.now(timezone.utc).isoformat()
        }

        table.put_item(Item=item)

        return build_response(200, {
            "message": "Check-in submitted successfully"
        })

    except Exception as exc:
        return build_response(500, {
            "message": "Submission failed",
            "error": str(exc)
        })