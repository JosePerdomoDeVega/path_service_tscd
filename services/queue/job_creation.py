import json
from domain.models.job import Job


def get_job_from_sqs_message(msg):
    body = json.loads(msg["Body"])
    receipt_handle = msg.get("ReceiptHandle")

    job_id = body.get("job_id")
    operation = body.get("operation")
    callback_url = body.get("callback_url")
    storage_key = body.get("storage_key")
    payload = get_payload(body)

    return Job(
        job_id=job_id,
        operation=operation,
        storage_key=storage_key,
        payload=payload,
        callback_url=callback_url,
        result=None,
        receipt_handle=receipt_handle,
    )


def get_payload(body):
    payload = {}
    for key in body.keys():
        if key in ['origin_word', 'destination_word', 'max_depth', 'degree']:
            payload[key] = body[key]
    return payload
