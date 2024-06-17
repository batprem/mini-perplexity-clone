import requests
import json
import re


def get_vqd(query: str) -> str:
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", # noqa
        "accept-language": "en-TH,en;q=0.9",
        "priority": "u=0, i",
        "referer": "https://duckduckgo.com/",
        "sec-ch-ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"', # noqa
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36", # noqa
    }

    params = {
        "q": query,
        "t": "h_",
    }

    response = requests.get(
        "https://duckduckgo.com/", params=params, headers=headers
    )

    html = response.text

    found = re.search('vqd="(([0-9]|-)*)"', html, re.IGNORECASE)
    if found:
        vqd = found.group(0).replace("vqd=", "").strip('"')
        return vqd


def get_data(q: str, vqd: str, language: str = "th-th") -> list:
    params = {
        "q": q,
        "l": language,
        "s": "0",
        "a": "h_",
        "dl": "th",
        "ct": "TH",
        "vqd": vqd,
    }
    response = requests.get("https://links.duckduckgo.com/d.js", params=params)

    return json.loads(
        response.text.split("DDG.pageLayout.load('d',")[-1].split(");")[0]
    )


def clean_data(raw_search_result: dict) -> dict:
    header = raw_search_result.get("a")
    sample_text = raw_search_result.get("t")
    url = raw_search_result.get("c")
    post_date = raw_search_result.get("e")

    return {
        "header": header,
        "sample_text": sample_text,
        "url": url,
        "post_date": post_date,
    }


def search(q: str) -> list:
    vqd = get_vqd(q)

    raw_search_results = get_data(q, vqd)
    cleaned_results = [
        clean_data(raw_search_result)
        for raw_search_result in raw_search_results
    ]
    return cleaned_results


if __name__ == "__main__":
    print(search("ดูดวงราศีเมถุน"))


# Output:
# [
#   {'header': '...', 'sample_text': '...', 'url': '', 'post_date': ''}
#   {'header': '...', 'sample_text': '...', 'url': '', 'post_date': ''}
# ...
# ]
