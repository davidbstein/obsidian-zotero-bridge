# first line: 1
@_memory.cache
def do_zot_get(path, group_id=None, user_id=ZOT_LIB_ID, params=None, api_key=ZOT_API_KEY, last_modified_version=0):
    params = params or {}
    params["key"] = api_key
    if group_id:
        user_or_group_prefix = f"groups/{group_id}"
    else:
        user_or_group_prefix = f"users/{user_id}"        
    headers = {
        "Zotero-API-Key": api_key,
        "If-Modified-Since-Version": str(last_modified_version)
    }
    resp = requests.get(f"{ZOT_API_URL}/{user_or_group_prefix}/{path}", params=params, headers=headers)
    assert resp.status_code == 200, (resp.status_code, resp.url, resp.text)
    to_ret = resp.json()
    if type(to_ret) != list:
        return to_ret
    while next_url:=_get_next_zot_link(resp.headers):
        print(resp.headers)
        resp = requests.get(next_url, params=params, headers=headers)
        to_ret.extend(resp.json())
    return to_ret
