from io import BytesIO
from appeals.core.common import Common
from appeals.config.config import Config


async def post_conversion(
    user_id: int,
    head: str,
    text: str
) -> list:
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
        return [{"status_code": response.status_code, "data": data}]


async def pin_files_conversion(
    user_id: int,
    conv_id: str,
    filename: str,
    mime: str,
    raw_file: BytesIO
) -> list:
    url = f"{Config.api_address}/users/{user_id}/conversions/{conv_id}/files"
    headers={"accept": "application/json"}
    raw_file.seek(0)
    files = {"files": (filename, raw_file, mime)}
    response = await Common.http.post(
        url,
        headers=headers,
        files=files
    )
    data = response.json()
    if response.status_code == 200:
        return data
    else:
        return [{"status_code": response.status_code, "data": data}]


async def get_conversions(
    user_id: int,
) -> list:
    url = f"{Config.api_address}/users/{user_id}/conversions"
    headers={"accept": "application/json"}
    response = await Common.http.get(
        url,
        headers=headers
    )
    data = response.json()
    if response.status_code == 200:
        return data
    else:
        return [{"status_code": response.status_code, "data": data}]


async def get_conversion(
    user_id: int,
    conv_id: int
) -> list:
    url = f"{Config.api_address}/users/{user_id}/conversions/{conv_id}"
    headers={"accept": "application/json"}
    response = await Common.http.get(
        url,
        headers=headers
    )
    data = response.json()
    if response.status_code == 200:
        return data
    else:
        return [{"status_code": response.status_code, "data": data}]


async def get_file_conversion(
    user_id: int,
    conv_id: int,
    file_id: int
) -> BytesIO:
    url = f"{Config.api_address}/users/{user_id}/conversions/{conv_id}/files/{file_id}"
    async with Common.http.stream("GET", url) as r:
        r.raise_for_status()
        buffer = BytesIO()
        async for chunk in r.aiter_bytes():
            buffer.write(chunk)

    buffer.seek(0)
    return buffer


if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
