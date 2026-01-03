from typing import Any, Dict
from pydantic import BaseModel

from domain.models.job import Job


class GraphJobResult(BaseModel):
    job_id: str
    operation: str
    storage_key: str
    payload: Dict[str, Any]
    callback_url: str
    result: Dict[str, Any]
    errors: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "job_id": self.job_id,
            "operation": self.operation,
            "storage_key": self.storage_key,
            "payload": self.payload,
            "callback_url": self.callback_url,
            "result": self.result,
            "errors": self.errors
        }


def get_graph_result(job: Job, result: dict, errors: dict) -> GraphJobResult:
    return GraphJobResult(job_id=job.job_id,
                          operation=job.operation,
                          payload=job.payload,
                          callback_url=job.callback_url,
                          storage_key=job.storage_key,
                          result=result,
                          errors=errors)
