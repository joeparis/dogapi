#!/usr/bin/env python3
import json
import os

import requests
from dotenv import load_dotenv


def get_dogs(url: str, limit: int = 5) -> requests.models.Response:
    headers = {"Content-Type": "application/json", "x-api-key": os.getenv("x-api-key")}

    params = {"limit": limit}

    return requests.get(f"{url}v1/breeds", params=params, headers=headers, timeout=2)


def set_favourite(url: str, image_id: str, sub_id: str | None = None) -> requests.models.Response:
    headers = {"Content-Type": "application/json", "x-api-key": os.getenv("x-api-key")}

    payload = {"image_id": image_id}

    if sub_id:
        payload["sub_id"] = sub_id

    data = json.dumps(payload)

    return requests.post(f"{url}v1/favourites", headers=headers, data=data, timeout=2)


def get_favourites(url: str, sub_id: str | None = None) -> requests.models.Response:
    headers = {"Content-Type": "application/json", "x-api-key": os.getenv("x-api-key")}
    params = "{}"

    if sub_id:
        params = json.dumps({"sub_id": sub_id})

    return requests.get(f"{url}v1/favourites", headers=headers, params=params, timeout=1)


def delete_favourite(url, image_id: str, sub_id: str | None = None) -> None:
    headers = {"Content-Type": "application/json", "x-api-key": os.getenv("x-api-key")}
    params = "{}"

    if sub_id:
        params = json.dumps({"sub_id": sub_id})

    requests.delete(f"{url}v1/favourites/{image_id}", headers=headers, data=params, timeout=2)


def _get_get_favourite_ids(url: str, sub_id: str | None = None) -> list[int]:
    return [fav["id"] for fav in get_favourites(url, sub_id).json()]


if __name__ == "__main__":
    URL = "https://api.thedogapi.com/"
    SUB_ID = "a8s9dufio"

    load_dotenv()

    res = get_dogs(URL)
    print(json.dumps(res.json(), indent=2))

    image_ids = ["26pHT3Qk7", "1-7cgoZSh", "rkiByec47"]
    for image_id in image_ids:
        res = set_favourite(URL, image_id, SUB_ID)
    print(json.dumps(res.json(), indent=2))

    favourite_ids = _get_get_favourite_ids(URL, SUB_ID)
    for id in favourite_ids:
        delete_favourite(URL, id, SUB_ID)

    res = get_favourites(URL, SUB_ID)
    print(json.dumps(res.json(), indent=2))
