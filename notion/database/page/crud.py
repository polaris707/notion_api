import requests

def getHeaders(api_key):
    return {
        "Accept": "application/json",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }


def makePayload(db_id, msg):
    payload = {
        "properties":{}
    }

    # root depth
    if db_id:
        payload.update({
            "parent": {
                "type": "database_id",
                "database_id": db_id
            }
        })
    if msg.get("archived"):
        payload.update({
            "archived": msg.get("archived")
        })
    if msg.get("icon"):
        payload.update({
            "icon": {
                "emoji": msg.get("icon"),
                "type": "emoji"
            },
        })
    # properties
    if msg.get("title"):
        payload["properties"].update({
            "Name": {
                "title": [
                    {
                        "type": "text",
                        "text": {
                            "content": msg.get("title")
                        }
                    }
                ]
            }
        })
    if msg.get("status"):
        payload["properties"].update({
            "Status": {
                "select": {
                    "name": msg.get("status")
                }
            }
        })
    if msg.get("tag"):
        payload["properties"].update({
            "Tag": {
                "multi_select": [{"name":t} for t in msg.get("tag")]
            }
        })
    if msg.get("due_date"):
        payload["properties"].update({
            "Due date": {
                "date": {
                    "start": msg.get("due_date")
                }
            }
        })

    return payload


def createPage(db_id, api_base_url, api_key, msg):
    payload = makePayload(db_id, msg)
    response = requests.post(api_base_url["create"], json=payload, headers=getHeaders(api_key))
    return response.json()


def selectPage(db_id, api_base_url, api_key, msg):
    filter = {
        "page_size": 1,
        "filter": {
            "and": [
                {
                    "property": "Name",
                    "title": {"equals": msg.get("title")}
                },
                {
                    "property": "Due date",
                    "date": {"equals": msg.get("due_date")}
                },
            ]
        }
    }

    response = requests.post(api_base_url["select"].format(db_id), json=filter, headers=getHeaders(api_key))
    return response.json()["results"][0]


def getPageId(db_id, api_base_url, api_key, msg):
    page = selectPage(db_id, api_base_url, api_key, msg)
    if not page.get("id"):
        raise Exception("there is not page_id")
    return page.get("id")


def updatePage(page_id, db_id, api_base_url, api_key, msg):
    payload = makePayload(db_id, msg)
    response = requests.patch(api_base_url["update"].format(page_id), json=payload, headers=getHeaders(api_key))
    return response.json()


def deletePage(page_id, api_base_url, api_key, **_):
    payload = {
        "archived": True
    }
    response = requests.patch(api_base_url["update"].format(page_id), json=payload, headers=getHeaders(api_key))
    return response.json()