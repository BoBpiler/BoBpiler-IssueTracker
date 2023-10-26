import requests
import json

max_take = 40

# URL
url = "https://sendvsfeedback2.azurewebsites.net/api/searchquery/searchV2"

removed_state = ["notabug", "duplicate"] #
removed_roadmap = ["vs-cpp-roadmap" , "vs2022-roadmap"] # roadmap이란말이 포함되어있으면 제거 

def get_msvc_issue(page) :
    # 헤더 설정
    headers = {
        "Host": "sendvsfeedback2.azurewebsites.net",
        "Content-Length": "826",
        "Sec-Ch-Ua": "",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Sec-Ch-Ua-Mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.97 Safari/537.36",
        "Sec-Ch-Ua-Platform": "",
        "Origin": "https://developercommunity.visualstudio.com",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://developercommunity.visualstudio.com/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "close"
    }

    # 바디 (JSON) 데이터
    data = {
        "searchFor": {
            "source": "developer-community",
            "tags": [
                {"type": "feedbackSessionId", "value": "WEB_78dcbe97-ebee-4afe-8a1f-9999"},
                {"type": "vs-otuid", "value": None},
                {"type": "vote-userid", "value": None},
                {"type": "vs-providerid", "value": None},
                {"type": "vsts-email", "value": None},
                {"type": "vsts-displayname", "value": None}
            ],
            "version": 20220110,
            "text": "",
            "customerChosenArea": None,
            "user": "",
            "title": "",
            "dotNetEntries": [],
            "watsonEntries": []
        },
        "skip": page,
        "take": max_take,
        "sort": "relevance",
        "filter": "all",
        "spaceIds": ["62"],
        "stateGroup": None,
        "version": 3,
        "topicsToFilterBy": [],
        "returnTotalCount": False,
        "typesFilterFlags": 3,
        "includeCountsByType": True,
        "searchStartTimeMsec": 1698322985385,
        "searchSource": "SearchPage",
        "clientVersion": "1.0.151",
        "capabilities": {
            "canDisplayTypedMarkdown": True,
            "expRichEditor": True,
            "rawTextSupport": True,
            "expFlights": ""
        }
    }

    # POST 요청 보내기
    response = requests.post(url, headers=headers, json=data)

    # 응답 확인
    data = response.json()
    # JSON 문자열로 변환
    json_string = json.dumps(data, indent=4)

    # print(json_string)

    # print(data)
    print(len(data["results"]))
    for d in data["results"]:
        print("TITLE : ", d["title"])
        print("TAGS : ")
        for tag in d["tags"] :
            print(tag["value"], ", ")
        print("STATE : ", d["state"])
        print("LINK : ", d["communityUrl"])
        print("CREATED TIME : ", d["createdDateUtc"])
        print('TEXT : ', d["text"])
        print(d)
        print()
        print()

get_msvc_issue(120)