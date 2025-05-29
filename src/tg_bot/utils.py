import httpx


async def send_request(
    method: str,
    url: str,
    *,
    json=None,
    params=None,
    headers=None,
    timeout=5.0,
    **kwargs
):
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.request(
                method=method,
                url=url,
                json=json,
                params=params,
                headers=headers,
                **kwargs
            )

        if response.status_code >= 400:
            raise Exception(response.text)

        return response

    except httpx.RequestError as e:
        raise Exception(f"Service unreachable: {e}")
