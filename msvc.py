import requests
import json
from datetime import datetime, timedelta
import os

BASE_URL = "https://sendvsfeedback2.azurewebsites.net/api/searchquery/searchV2"
MAX_TAKE = 40

REMOVED_STATE = ["notabug", "duplicate", "otherproduct", "notenoughinfo", "outofscope"]
REMOVED_ROADMAP = "roadmap" # tags

current_bug_count = 0
file_index = 1
MAX_BUGS_PER_FILE = 240
compile_name = 'MSVC'
file_name = ''
now = ''

def create_folder(formatted_time):
    output_directory = f"output/{formatted_time}"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    return output_directory

def save_data(issue) :
    global now
    formatted_time = now.strftime('%Y%m%d_%H%M%S')
    output_directory = create_folder(formatted_time)
    file_name = f'{output_directory}/{compile_name}_COMMUNITY_{formatted_time}'
    global current_bug_count
    global file_index

    if current_bug_count >= MAX_BUGS_PER_FILE:
        file_index += 1
        current_bug_count = 0
    with open(file_name + f"_{file_index}.md", 'a') as f:
        # print("TITLE : ", issue["title"])
        # print("TAGS : ")
        # for tag in issue["tags"]:
        #     print(tag["value"], ", ")
        # print("LINK : ", issue["communityUrl"])
        # print("STATE : ", issue["state"])
        # print("CREATED TIME : ", issue["createdDateUtc"])
        # print('TEXT : ', issue["text"])    

        title = "None"
        if issue["title"] is not None :
            title = issue["title"]
        
        created_at = "None"
        if issue["createdDateUtc"] is not None :
            created_at = issue["createdDateUtc"]
        
        html_url = "None"
        if issue["communityUrl"] is not None:
            html_url = issue["communityUrl"]
        
        state = "None"
        if issue["state"] is not None:
            state = issue["state"]
        
        body = "None"
        if issue["text"] is not None :
            body = issue["text"]
        

        f.write("\n\n")
        f.write(f"### compiler : `{compile_name}`\n")
        f.write(f"### title : `{title}`\n")
        f.write("### open_at : `" + created_at + "`\n")
        f.write("### link : " + html_url + "\n")
        f.write("### status : `" + state  + "`\n")
        f.write("### tags : `")
        for label in issue["tags"]:
            f.write(label["value"] + ", ")
        f.write("`\n")

        f.write("### content : \n" + body + "")
        f.write("\n\n\n")
        f.write("---\n")
    current_bug_count += 1

def create_headers():
    return {
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

def create_data(page):
    # 바디 (JSON) 데이터
    return {
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
        "take": MAX_TAKE,
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

def send_request(page):
    headers = create_headers()
    data = create_data(page)

    while True:
        try:
            response = requests.post(BASE_URL, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except (requests.ConnectionError, requests.Timeout, requests.RequestException, json.JSONDecodeError) as e:
            print(f"Error occurred: {e}, retrying.. {page}")
            continue


def print_issue_data(issue):
    print(issue)
    print("\n\n")


def is_issue_relevant(issue):
    if issue["state"] in REMOVED_STATE:  # 상태 체크
        return False
    for tag in issue["tags"]:
        if REMOVED_ROADMAP in tag["value"]:  # 태그 체크
            return False
    return True


def get_msvc_issue(page):
    data = send_request(page)

    if not data:
        return True

    print(len(data["results"]))

    for issue in data["results"]:
        if is_issue_relevant(issue):
            save_data(issue)

    return False


def main():
    global now
    now = datetime.now()
    page = 0
    while True:
        if get_msvc_issue(page):
            break
        page += MAX_TAKE
    print("end")


if __name__ == "__main__":
    main()
