from appeals.core.common import Common
from appeals.config.config import Config


async def post_conversion(
    user_id: int,
    head: str,
    text: str
):
    url = f"{Config.api_address}/conversions"
    headers={"accept": "application/json"}
    params = {
        "user_id": user_id,
        "head": head,
        "text": text,
        "status": "unviewed"
        }
    response = await Common.http.post(
        url,
        headers=headers,
        json=params
    )
    data = response.json()
    if response.status_code == 200:
        return data
    else:
        return {"status": response.status_code, "data": data}


if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
