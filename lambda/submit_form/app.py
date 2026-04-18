import json
import os
from datetime import datetime, timezone
from decimal import Decimal
import base64

import boto3
from botocore.exceptions import ClientError

TABLE_NAME = os.environ.get("TABLE_NAME", "").strip()

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME) if TABLE_NAME else None


def build_response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json"
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

        if event.get("isBase64Encoded"):
            raw_body = base64.b64decode(raw_body).decode("utf-8")

        body = json.loads(raw_body)

        token_raw = body.get("token")
        if not token_raw:
            return build_response(400, {"message": "Missing token"})

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

        sleep_hours = body.get("sleep_hours")
        money_spent = body.get("money_spent")
        nutrition_score = body.get("nutrition_score")
        finances_score = body.get("finances_score")
        mental_score = body.get("mental_score")

        if not person_id:
            return build_response(400, {"message": "Missing person_id in token"})

        if not submission_date:
            return build_response(400, {"message": "Missing submission date"})

        if token_date != submission_date:
            return build_response(400, {"message": "Token date mismatch"})

        if sleep_hours is None:
            return build_response(400, {"message": "Missing sleep_hours"})

        if money_spent is None:
            return build_response(400, {"message": "Missing money_spent"})

        if nutrition_score is None:
            return build_response(400, {"message": "Missing nutrition_score"})

        if finances_score is None:
            return build_response(400, {"message": "Missing finances_score"})

        if mental_score is None:
            return build_response(400, {"message": "Missing mental_score"})

        try:
            sleep_hours = Decimal(str(sleep_hours))
            money_spent = Decimal(str(money_spent))
            nutrition_score = int(nutrition_score)
            finances_score = int(finances_score)
            mental_score = int(mental_score)
        except (ValueError, TypeError, ArithmeticError):
            return build_response(400, {"message": "One or more numeric fields are invalid"})

        if sleep_hours < 0 or sleep_hours > 24:
            return build_response(400, {"message": "sleep_hours must be between 0 and 24"})

        if money_spent < 0:
            return build_response(400, {"message": "money_spent cannot be negative"})

        for field_name, value in {
            "nutrition_score": nutrition_score,
            "finances_score": finances_score,
            "mental_score": mental_score,
        }.items():
            if value < 1 or value > 5:
                return build_response(400, {"message": f"{field_name} must be between 1 and 5"})

        item = {
            "person_id": person_id,
            "submission_date": submission_date,
            "nutrition_score": nutrition_score,
            "nutrition_notes": body.get("nutrition_notes", "").strip(),
            "finances_score": finances_score,
            "finances_notes": body.get("finances_notes", "").strip(),
            "mental_score": mental_score,
            "mental_notes": body.get("mental_notes", "").strip(),
            "sleep_hours": sleep_hours,
            "money_spent": money_spent,
            "submitted_at": datetime.now(timezone.utc).isoformat()
        }

        print(f"Saving submission for person_id={person_id}, submission_date={submission_date}")

        table.put_item(
            Item=item,
            ConditionExpression="attribute_not_exists(person_id) AND attribute_not_exists(submission_date)"
        )

        return build_response(200, {
            "message": "Check-in submitted successfully"
        })

    except ClientError as exc:
        error_code = exc.response.get("Error", {}).get("Code")

        if error_code == "ConditionalCheckFailedException":
            return build_response(409, {
                "message": "A check-in for this person and date already exists"
            })

        print(f"DynamoDB ClientError: {exc}")
        return build_response(500, {
            "message": "Submission failed",
            "error": "Database error"
        })

    except Exception as exc:
        print(f"Unhandled error: {exc}")
        return build_response(500, {
            "message": "Submission failed",
            "error": str(exc)
        })