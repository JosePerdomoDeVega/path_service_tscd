from typing import Any, Dict, Optional
from pydantic import BaseModel


class Job(BaseModel):
    job_id: str
    operation: str
    payload: Dict[str, Any]
    callback_url: str

    result: Optional[Dict[str, Any]] = None
    storage_key: Optional[str] = None
    receipt_handle: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "job_id": self.job_id,
            "operation": self.operation,
            "payload": self.payload,
            "callback_url": self.callback_url,
            "result": self.result,
            "receipt_handle": self.receipt_handle,
        }

    def get_valid_payload(self) -> Dict[str, Any]:
        valid_payload = {}
        for k, v in self.payload.items():
            if v != 'None' and v is not None:
                valid_payload[k] = v
        print(valid_payload)
        return valid_payload
