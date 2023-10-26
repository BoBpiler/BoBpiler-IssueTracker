import requests
import datetime
import json

# 현재 날짜에서 5년 전의 날짜 계산
end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=5*365)  # 대략적인 5년 전

# 검색 키워드 리스트 - 추가 및 제거로 조절이 가능합니다.
search_keywords = ["optimization", "miscompilation"]

# GCC의 버그질라 API 엔드포인트 및 키워드 설정
gcc_base_url = "https://gcc.gnu.org/bugzilla/rest.cgi/bug"
params = {
    "keywords": "", 
    "chfieldfrom": start_date,  
    "chfieldto": end_date,  
    "include_fields": "id,summary,status,resolution,component,version,severity,creation_time,last_change_time,keywords",
}

# 모든 키워드에 대한 버그 검색 결과를 담는 리스트
bugs = []
# 한 번의 검색에 키워드 한 개만 가능해서 for문을 통해서 여러 번 검색
for search_keyword in search_keywords:
    params['keywords'] = search_keyword
    response = requests.get(gcc_base_url, params=params)
    bugs.extend(response.json().get("bugs", []))

# 버그 id를 기반으로 중복 제거
unique_bugs = {bug['id']: bug for bug in bugs}.values()  # 중복 제거

# 탐지된 모든 버그의 상세 정보를 저장하는 리스트
details_list = []
# 결과를 readable하게 가공해서 md 파일로 저장
with open("gcc.md", "w", encoding="utf-8") as md_file:

    for bug in unique_bugs:
        # 각 버그의 코멘트를 가져오는 API 호출
        comment_url = f"{gcc_base_url}/{bug['id']}/comment"
        comment_response = requests.get(comment_url)
        comments_data = comment_response.json().get("bugs", {}).get(str(bug['id']), {}).get("comments", [])
        description = comments_data[0]['text'] if comments_data else "No comments available."  # 첫 번째 코멘트를 본문 내용으로 사용
        
        # 상세 정보를 딕셔너리로 조합
        details = {
            "compiler": "gcc",
            "title": bug['summary'],
            "open_at": bug['creation_time'],
            "last_modified_date": bug['last_change_time'],
            "link": f"https://gcc.gnu.org/bugzilla/show_bug.cgi?id={bug['id']}",
            "status": bug['status'],
            "tags": bug['keywords'],
            "component": bug['component'],
            "version": bug['version'],
            "severity": bug['severity'],
            "contents": description,
        }
        
        details_list.append(details)

        md_file.write("\n\n")  # 구분선
        md_file.write(f"### compiler : `gcc`\n")
        md_file.write(f"### title : `{details['title']}`\n")
        md_file.write(f"### open_at : `{details['open_at']}`\n")
        md_file.write(f"### last_modified_date : `{details['last_modified_date']}`\n")
        md_file.write(f"### link : {details['link']}\n")
        md_file.write(f"### status : `{details['status']}`\n")
        md_file.write(f"### tags : `{', '.join(details['tags'])}`\n")
        md_file.write(f"### component : `{details['component']}`\n")
        md_file.write(f"### version : `{details['version']}`\n")
        md_file.write(f"### severity : `{details['severity']}`\n")
        md_file.write(f"### contents :\n{description}\n\n\n")
        md_file.write("---\n")  # 구분선

# details_list를 JSON 파일로 저장
with open("gcc.json", "w", encoding="utf-8") as json_file:
    json.dump(details_list, json_file, ensure_ascii=False, indent=4)