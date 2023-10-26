import requests
import datetime

# 현재 날짜에서 5년 전의 날짜 계산
end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=5*365)  # 대략적인 5년 전

# 버그질라 API 엔드포인트 및 키워드 설정
base_url = "https://bugzilla.mozilla.org/rest/bug"
params = {
    "keywords": "optimization",  # 예시 키워드
    "chfieldfrom": start_date,  # 변경 시작 날짜
    "chfieldto": end_date,      # 변경 끝 날짜
    "include_fields": "id,summary,status,resolution"  # 원하는 필드만 포함
}

response = requests.get(base_url, params=params)

# 결과 확인 및 출력
bugs = response.json().get("bugs", [])
for bug in bugs:
    print(f"ID: {bug['id']}, Summary: {bug['summary']}, Status: {bug['status']}, Resolution: {bug['resolution']}")


