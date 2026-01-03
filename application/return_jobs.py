import json
import httpx
from domain.models.graph_job_result import GraphJobResult
from domain.settings import get_settings

settings = get_settings()


async def return_result_to_gsq(result: GraphJobResult):
    async with httpx.AsyncClient() as client:
        r = await client.post(settings.gsq_url,
                              headers={'Authorization': f'Bearer {settings.gsq_auth_token}'},
                              data=json.dumps(result.to_dict()))
        if r.status_code != 200:
            raise Exception(f'HTTP status code {r.status_code}: {r.text}')
        else:
            return 200
