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
    "include_fields": "id,summary,status,resolution", 
    "quicksearch": "gcc | clang"  # 이 부분은 필요에 따라 조정이 가능합니다.
}

response = requests.get(base_url, params=params)

# 결과 확인 및 출력
bugs = response.json().get("bugs", [])
for bug in bugs:
    print(f"ID: {bug['id']}, Summary: {bug['summary']}, Status: {bug['status']}, Resolution: {bug['resolution']}")


