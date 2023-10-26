import requests
import json
from datetime import datetime, timedelta

GITHUB_TOKEN = ""
get_timeout = 5
years = 5
file_name = ''
compile_name = 'LLVM'

def read_git_key(key_path):
    global file_name
    # Get current date and time
    now = datetime.now()

    # Format the datetime object to string: YYYYMMDD_HHMMSS
    formatted_time = now.strftime('%Y%m%d_%H%M%S')
    file_name = f'{compile_name}_{formatted_time}.md'
    global GITHUB_TOKEN
    with open(key_path, 'r', encoding='utf-8') as file:
        GITHUB_TOKEN = file.read()


discard_labels = ["question", "c++/cli", "clang:analysis",
                  "code-quality", "libc++", "invalid", "libstdc++", "objective-c", "crash-on-valid", "crash"]
# "clang:frontend",
labels = ["clang:codegen",
          "c99", "c++26", "c23", "c++23", "c++20", "c17", "c++17", "c++14", "c11",
          "c++11", "c++", "c", "concepts", "consteval", "constant-folding", "coroutines", "filesystem",
          "llvm:codegen", "llvm:optimizations", "miscompilation" ]

def ensure_closed_backticks(text):
    # Counter for backticks
    counter = 0
    
    # Iterate through each character in the text
    for char in text:
        if char == '`':
            counter += 1
            
    # If counter is odd, add one backtick to close it
    if counter % 2 == 1:
        text += '`'
    # If counter is divisible by 3 with a remainder, add the necessary backticks to make it a multiple of 3
    elif counter % 3 != 0:
        remainder = counter % 3
        text += '`' * (3 - remainder)
    
    return text

def save_data(issue) :
    # if issue.get("pull_request") is None:
    #     print("None")
    # else :
    #     print(issue["pull_request"])
    #return True
    with open(file_name, 'a') as f:
        # print("TITLE : ", issue["title"])
        # print("API URL : ", issue["url"])
        # print("HTML_URL : ", issue["html_url"])
        # print("BODY : ", issue["body"])
        # # print("number : ", issue["number"])
        # # open_time = datetime.strptime(issue["created_at"], "%Y-%m-%dT%H:%M:%SZ")
        # # print("CREATED TIME : ", open_time)
        

        title = "None"
        if issue["title"] is not None :
            title = issue["title"]
        created_at = "None"
        if issue["created_at"] is not None :
            created_at = issue["created_at"]
        
        html_url = "None"
        if issue["html_url"] is not None:
            html_url = issue["html_url"]
        state = "None"
        if issue["state"] is not None:
            state = issue["state"]
        body = "None"
        if issue["body"] is not None :
            body = issue["body"]
        body = ensure_closed_backticks(body)

        f.write("\n\n")
        f.write(f"### compiler : `{compile_name}`\n")
        f.write(f"### title : `{title}`\n")
        f.write("### open_at : `" + created_at + "`\n")
        f.write("### link : " + html_url + "\n")
        f.write("### status : `" + state  + "`\n")
        f.write("### tags : `")
        for label in issue["labels"]:
            f.write(label["name"] + ", ")
        f.write("`\n")

        f.write("### content : \n" + body + "")
        f.write("\n\n\n")
        f.write("---\n")
        # closed_time = None
        # if issue["closed_at"] is not None:
        #     closed_time = datetime.strptime(
        #         issue["closed_at"], "%Y-%m-%dT%H:%M:%SZ")
        # print("CLOSED TIME : ", closed_time)
        # print()
        # print("#"*100)
        # print("#"*100)
        # print()

def send_api_request(page_num):
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    params = {
        "per_page": 100,
        "page": page_num
    }
    url = "https://api.github.com/repos/llvm/llvm-project/issues"
    while True:
        try:
            response = requests.get(
                url, headers=headers, params=params, timeout=get_timeout)
            response.raise_for_status()
            break
        except requests.exceptions.RequestException as err:
            print("OOps: Something Else, retry..", err)
            continue
        except requests.exceptions.HTTPError as errh:
            print("Http Error: retry..", errh)
            continue
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting: retry..", errc)
            continue
        except requests.exceptions.Timeout as errt:
            print("Timeout Error: retry..", errt)
            continue
        except Exception as e:
            print("Unknown: retry", e)
            continue

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return []


def should_discard_issue(issue):
    # issue["pull_request"] 이 타입이 None이라면 이것또한 True한다
    if issue.get("pull_request") is not None:
        return True
    return any(iss["name"] in discard_labels for iss in issue["labels"])


def is_within_last_five_years(date_string):
    f"""
    Check if the given datetime string is within the last 5 years from the current date and time.
    
    Args:
    - date_string (str): The datetime string in the format "%Y-%m-%dT%H:%M:%SZ"

    Returns:
    - bool: True if the datetime is within the last {years} years, False otherwise.
    """
    date_object = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")
    time_difference = datetime.utcnow() - date_object

    # Check if the time difference is less than or equal to 5 years
    return time_difference <= timedelta(days=years*365)


# def print_issue_details(issue):
#     # print(issue)


def get_llvm_issue(page_num):
    issues = send_api_request(page_num)
    if issues:  # issue is Not empty
        for issue in issues:
            if not is_within_last_five_years(issue["created_at"]):
                return True

            if should_discard_issue(issue):
                continue

            if any(iss["name"] in labels for iss in issue["labels"]):
                save_data(issue)
                continue
                # Store or process the issue here

def test_case(count) :
    for i in range(1, count):
        get_llvm_issue(i)

def start_llvm_issue():
    i = 0
    while True :
        if get_llvm_issue(i) :
            break
        i = i + 1
    print("end")

read_git_key('git.key')
start_llvm_issue()