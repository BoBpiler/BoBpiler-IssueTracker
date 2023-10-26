import requests
import datetime

# 현재 날짜에서 5년 전의 날짜 계산
end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=5*365)  # 대략적인 5년 전

# GCC의 버그질라 API 엔드포인트 및 키워드 설정
base_url = "https://gcc.gnu.org/bugzilla/rest.cgi/bug"
params = {
    "keywords": "optimization", 
    "chfieldfrom": start_date,  
    "chfieldto": end_date,  
    "include_fields": "id,summary,status,resolution,component,version,severity,creation_time,last_change_time,keywords",
}

response = requests.get(base_url, params=params)

# 결과 확인 및 출력
bugs = response.json().get("bugs", [])
for bug in bugs:
    print("*"*100) # 구분선
    # 각 버그의 코멘트를 가져오는 API 호출
    comment_url = f"{base_url}/{bug['id']}/comment"
    comment_response = requests.get(comment_url)
    comments_data = comment_response.json().get("bugs", {}).get(str(bug['id']), {}).get("comments", [])
    description = comments_data[0]['text'] if comments_data else "No comments available."  # 첫 번째 코멘트를 본문 내용으로 사용
    # 상세 정보를 딕셔너리로 조합
    details = {
        "link": f"https://gcc.gnu.org/bugzilla/show_bug.cgi?id={bug['id']}",
        "title": bug['summary'],
        "status": bug['status'],
        "component": bug['component'],
        "version": bug['version'],
        "severity": bug['severity'],
        "reported_date": bug['creation_time'],
        "modified_date": bug['last_change_time'],
        "keywords": bug['keywords'],
        "contents": description,
    }
    link = f"link: {details['link']}"
    title = f"title: {details['title']}"
    status = f"status: {details['status']}"
    component = f"component: {details['component']}"
    version = f"version: {details['version']}"
    severity = f"severity: {details['severity']}"
    reported_date = f"reported_date: {details['reported_date']}" 
    modified_date = f"modified_date: {details['modified_date']}" 
    keywords = f"keywords: {details['keywords']}"
    contents = f"contents: {description}"
    print(link)
    print(title)
    print(status)
    print(component)
    print(version)
    print(severity)
    print(reported_date)
    print(modified_date)
    print(keywords)
    print(contents)

