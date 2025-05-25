from appeals.api.common import Common
from appeals.config.config import Config


async def get_ping() -> dict:
    url = f"{Config.api_address}/ping"
    response = await Common.http.get(url)
    data = response.json()
    if response.status_code == 200:
        return data
    else:
        return {"status": response.status_code}


async def post_ping(
        op: str,
        num: int = 0
):
    url = f"{Config.api_address}/ping"
    headers={"accept": "application/json"}
    params = {
        "op": op,
        "value": num
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
