import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta

# 전역 변수 설정
GITHUB_TOKEN = ""
owner = "openssl"
repo = "openssl"
BASE_URL = f"https://api.github.com/repos/{owner}/{repo}/commits"
HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization": None,
    "X-GitHub-Api-Version": "2022-11-28"
}
months = 36
chunk = 100

def read_git_key(key_path):
    global GITHUB_TOKEN, HEADERS
    with open(key_path, 'r', encoding='utf-8') as file:
        GITHUB_TOKEN = file.read().strip()
        HEADERS["Authorization"] = f"Bearer {GITHUB_TOKEN}"

def calculate_dates(n_months):
    n_months_ago = datetime.utcnow() - relativedelta(months=n_months)
    since = n_months_ago.strftime("%Y-%m-%dT%H:%M:%SZ")
    until = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    return since, until

def get_github_commits(url, params):
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def save_commit_to_markdown(commit_sha, commit_number):
    # 커밋 갯수가 1000의 배수마다 새로운 파일로 저장
    file_number = commit_number // chunk + 1
    file_name = f"commit_report_{file_number}.md"
    
    url = f"{BASE_URL}/{commit_sha}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        commit_info = response.json()
        # print(commit_info['commit']['committer']['date'])
        with open(file_name, "a", encoding="utf-8") as md_file:
            # 목차 추가
            if commit_number % chunk == 1:
                md_file.write("# 목차\n")
                for i in range(1, chunk+1):
                    md_file.write(f"- [{i}](#{i})\n")
                md_file.write("\n")
            md_file.write(f"# {commit_number}\n\n")
            md_file.write(f"**Time : {commit_info['commit']['committer']['date']}**\n\n")
            md_file.write(f"**Commit URL**: [{commit_info['html_url']}]({commit_info['html_url']})\n\n")
            md_file.write(f"**Commit Message**:\n\n```\n{commit_info['commit']['message']}\n```\n\n")
            
            md_file.write("### Files Changed\n\n")
            for file in commit_info["files"]:
                md_file.write(f"- **File Name**: {file['filename']}\n")
                md_file.write(f"  - **Patch**:\n\n```diff\n{file['patch']}\n```\n\n")
        print(f"Commit report #{commit_number} saved to {file_name}")
    else:
        response.raise_for_status()

def main():
    global GITHUB_TOKEN
    read_git_key('git.key')
    page = 0
    since, until = calculate_dates(months)
    commit_count = 0
    while True:
        params = {'since': since, 'until': until, 'page': page, 'per_page': 100}
        commits_url = f"{BASE_URL}"
        try:
            commits = get_github_commits(commits_url, params)
            if not commits:
                break
            for commit in commits:
                commit_date = datetime.strptime(commit['commit']['committer']['date'], "%Y-%m-%dT%H:%M:%SZ")
                if commit_date < datetime.utcnow() - relativedelta(months=months):
                    print("2 months old commit found. Exiting...")
                    print(f"Total commits processed: {commit_count}")
                    return
                commit_count += 1
                save_commit_to_markdown(commit['sha'], commit_count)
                print("#################################")
        except requests.exceptions.HTTPError as err:
            print(f"HTTP error occurred: {err}")
        except Exception as err:
            print(f"An error occurred: {err}")
        page = page + 1

if __name__ == "__main__":
    main()
