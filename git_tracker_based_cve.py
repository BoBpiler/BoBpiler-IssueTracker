import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta

def read_git_key(key_path):
    with open(key_path, 'r', encoding='utf-8') as file:
        github_token = file.read().strip()
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {github_token}",
            "X-GitHub-Api-Version": "2022-11-28"
        }
    return headers

def calculate_dates(n_months):
    n_months_ago = datetime.utcnow() - relativedelta(months=n_months)
    since = n_months_ago.strftime("%Y-%m-%dT%H:%M:%SZ")
    until = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    return since, until

def filter_commits_by_cve_id(commits, cve_id):
    # CVE ID를 포함하는 커밋만 필터링
    filtered_commits = [commit for commit in commits if cve_id in commit['commit']['message']]
    return filtered_commits

def search_commit_for_cve(cve_id, commits):
    # 가져온 커밋 데이터에서 CVE ID를 포함하는 커밋만 필터링
    filtered_commits = filter_commits_by_cve_id(commits, cve_id)
    return filtered_commits

def get_github_commits(url, headers, params):
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def fetch_cve_data(keyword):
    cve_items = []
    page = 0

    while True:
        url = "https://services.nvd.nist.gov/rest/json/cves/1.0"
        params = {
            'keyword': keyword,
            'resultsPerPage': 10,  # 한 페이지 당 결과 수
            'startIndex': page * 10  # 시작 인덱스
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            # 결과가 더 이상 없으면 반복 중단
            if data['result']['CVE_Items']:
                cve_items.extend(data['result']['CVE_Items'])
                page += 1
            else:
                break
        elif response.status_code == 403:
            # 403 에러 발생 시 중단
            print("Access denied. Stopping the data fetch: HTTP 403.")
            break
        else:
            print(f"Failed to fetch data: HTTP {response.status_code}. Stopping the data fetch.")
            break

    return cve_items

def save_to_md(cve_items, keyword):
    filename = f"{keyword}_cve_list.md"

    with open(filename, 'w') as f:
        for item in cve_items:
            cve_id = item['cve']['CVE_data_meta']['ID']
            description = item['cve']['description']['description_data'][0]['value']
            published_date = item['publishedDate']
            last_modified_date = item['lastModifiedDate']

            f.write(f"## {cve_id}\n")
            f.write(f"**Description:** {description}\n")
            f.write(f"**Published Date:** {published_date}\n")
            f.write(f"**Last Modified Date:** {last_modified_date}\n")
            f.write(f"{'-' * 50}\n\n")

    print(f"Data saved to {filename}")

# def save_commit_to_markdown(commit_sha, commit_number, base_url, headers, chunk):
#     # 커밋 갯수가 1000의 배수마다 새로운 파일로 저장
#     file_number = commit_number // chunk + 1
#     file_name = f"commit_report_{file_number}.md"
    
#     url = f"{base_url}/{commit_sha}"
#     response = requests.get(url, headers=headers)
#     if response.status_code == 200:
#         commit_info = response.json()
#         # print(commit_info['commit']['committer']['date'])
#         with open(file_name, "a", encoding="utf-8") as md_file:
#             # 목차 추가
#             if commit_number % chunk == 1:
#                 md_file.write("# 목차\n")
#                 for i in range(1, chunk+1):
#                     md_file.write(f"- [{i}](#{i})\n")
#                 md_file.write("\n")
#             md_file.write(f"# {commit_number}\n\n")
#             md_file.write(f"**Time : {commit_info['commit']['committer']['date']}**\n\n")
#             md_file.write(f"**Commit URL**: [{commit_info['html_url']}]({commit_info['html_url']})\n\n")
#             md_file.write(f"**Commit Message**:\n\n```\n{commit_info['commit']['message']}\n```\n\n")
            
#             md_file.write("### Files Changed\n\n")
#             for file in commit_info["files"]:
#                 md_file.write(f"- **File Name**: {file['filename']}\n")
#                 md_file.write(f"  - **Patch**:\n\n```diff\n{file['patch']}\n```\n\n")
#         print(f"Commit report #{commit_number} saved to {file_name}")
#     else:
#         response.raise_for_status()


# save_commit_to_markdown 함수를 commit_sha를 인자로 받도록 수정
def save_commit_to_markdown(commit_sha, commit_number, base_url, headers, file_name, chunk):
    url = f"{base_url}/{commit_sha}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        commit_info = response.json()
        with open(file_name, "a", encoding="utf-8") as md_file:
            if commit_number % chunk == 1:
                md_file.write("# 목차\n")
                for i in range(commit_number, commit_number + chunk):
                    md_file.write(f"- [{i}](#{i})\n")
                md_file.write("\n")
            md_file.write(f"## Commit {commit_number}\n\n")
            md_file.write(f"**Timestamp**: {commit_info['commit']['committer']['date']}  \n")
            md_file.write(f"**Author**: {commit_info['commit']['committer']['name']}  \n")
            md_file.write(f"**Commit URL**: [View Commit]({commit_info['html_url']})  \n\n")
            md_file.write(f"**Message**:  \n")
            md_file.write(f"```\n{commit_info['commit']['message']}\n```\n\n")

            if 'files' in commit_info:
                md_file.write("### Files Changed\n\n")
                for file in commit_info['files']:
                    md_file.write(f"- **{file['filename']}**  \n")
                    if 'patch' in file:
                        md_file.write(f"```diff\n{file['patch']}\n```\n\n")
        print(f"Saved commit {commit_number} to {file_name}")
    else:
        response.raise_for_status()



def main():
    headers = read_git_key('git.key')
    owner = input("GitHub repository owner (e.g., openssl): ")
    repo = input("GitHub repository name (e.g., openssl): ")
    cve_keyword = input("Enter the CVE keyword (e.g., openssl): ")
    base_url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    months = 36
    chunk = 100
    commit_count = 0
    file_number = 1
    file_name = f"commit_report_{file_number}.md"
    since, until = calculate_dates(months)

    # 모든 커밋을 가져옵니다.
    commits_data = []
    page = 1  # GitHub 페이지는 1부터 시작
    while True:
        params = {'since': since, 'until': until, 'page': page, 'per_page': 100}
        try:
            commits = get_github_commits(base_url, headers, params)
            if not commits:
                break
            commits_data.extend(commits)
            page += 1
        except requests.exceptions.HTTPError as err:
            print(f"HTTP error occurred: {err}")
            break
        except Exception as err:
            print(f"An error occurred: {err}")
            break

    # CVE 데이터를 가져옵니다.
    cve_items = fetch_cve_data(cve_keyword)  
    if cve_items:
        # CVE 데이터를 Markdown으로 저장합니다.
        save_to_md(cve_items, cve_keyword)
        print(f"CVE data for {cve_keyword} saved.")
    else:
        print("No CVE data found.")
        return

    # 각 CVE ID에 대해 필터링된 커밋을 검색하고 저장합니다.
    for cve_item in cve_items:
        cve_id = cve_item['cve']['CVE_data_meta']['ID']
        filtered_commits = filter_commits_by_cve_id(commits_data, cve_id)
        if filtered_commits:
            for commit in filtered_commits:
                if commit_count % chunk == 0 and commit_count != 0:
                    file_number += 1
                    file_name = f"commit_report_{file_number}.md"
                commit_count += 1
                commit_sha = commit['sha']  # 여기서 커밋의 SHA를 가져옵니다.
                save_commit_to_markdown(commit_sha, commit_count, base_url, headers, file_name, chunk)
        else:
            print(f"No commits found for CVE {cve_id}")

    print(f"Total commits processed: {commit_count}")



if __name__ == "__main__":
    main()
