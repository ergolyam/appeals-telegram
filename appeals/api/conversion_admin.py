from appeals.core.common import Common
from appeals.config.config import Config


async def get_all_conversions(
    passwd: str,
) -> list:
    url = f"{Config.api_address}/conversions"
    headers={"accept": "application/json"}
    response = await Common.http.get(
        url,
        headers=headers,
        auth=( 'admin', passwd )
    )
    data = response.json()
    if response.status_code == 200:
        return data
    else:
        return [{"status_code": response.status_code, "data": data}]


if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
