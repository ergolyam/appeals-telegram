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


async def set_status_conversion(
    user_id: int,
    conv_id: int,
    status: str,
    passwd: str
) -> list:
    url = f"{Config.api_address}/users/{user_id}/conversions/{conv_id}/status"
    headers={"accept": "application/json"}
    params = {
        "status": status,
    }
    response = await Common.http.patch(
        url,
        headers=headers,
        json=params,
        auth=( 'admin', passwd )
    )
    data = response.json()
    if response.status_code == 200:
        return data
    else:
        return [{"status_code": response.status_code, "data": data}]


async def delete_conversion(
    user_id: int,
    conv_id: int,
    passwd: str
) -> list:
    url = f"{Config.api_address}/users/{user_id}/conversions/{conv_id}"
    response = await Common.http.delete(
        url,
        auth=( 'admin', passwd )
    )
    if response.status_code == 204:
        return [{"status_code": response.status_code, "data": "successfully"}]
    else:
        return [{"status_code": response.status_code, "data": "unsuccessfully"}]


if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
