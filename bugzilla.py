import requests
import datetime
import json
import os
from concurrent.futures import ThreadPoolExecutor, wait

# 검색 키워드 리스트 - 추가 및 삭제가 가능합니다.
keywords = ["optimization", "miscompilation"]

# gcc components에서 c, c++과 관련이 있는 컴포넌트 종류 리스트
gcc_relevant_components = [
    "c", "c++", "demangler", "libstdc++", "preprocessor", "objc++", 
    "lto", "middle-end", "rtl-optimization", "tree-optimization", 
    "target", "plugins", "libgcc"
]

# 폴더를 생성하는 함수
def create_folder(formatted_time):
    output_directory = f"output/{formatted_time}"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    return output_directory


# unique_bugs를 chunk_size만큼 나눠서 여러 파일에 저장하는 함수 (md 파일의 길이가 만 줄이 넘지 않도록 하기 위해서 160개로 끊었음)
def save_to_files(base_url, compiler_name, formatted_time, unique_bugs, chunk_size=160):
    
    num_chunks = len(unique_bugs) // chunk_size + (1 if len(unique_bugs) % chunk_size else 0)
    output_directory = create_folder(formatted_time)  # 폴더 생성 및 경로 가져오기

    for chunk_idx in range(num_chunks):
        start_idx = chunk_idx * chunk_size
        end_idx = start_idx + chunk_size
        current_chunk = list(unique_bugs)[start_idx:end_idx]

        # chunk 별로 파일 이름 수정
        md_filename = f"{output_directory}/{compiler_name}_bugzilla_{formatted_time}_chunk_{chunk_idx + 1}.md"
        json_filename = f"{output_directory}/{compiler_name}_bugzilla_{formatted_time}_chunk_{chunk_idx + 1}.json"

        # 각 chunk에 대한 데이터 저장 로직 
        with open(md_filename, "w", encoding="utf-8") as md_file, open(json_filename, "w", encoding="utf-8") as json_file:
            # 파일의 상단에 청크 관련 정보를 기록
            md_file.write(f"### Total Bugs Detected: {len(unique_bugs)}\n")
            md_file.write(f"### Current Chunk: {chunk_idx + 1} of {num_chunks}\n")
            md_file.write(f"### Bugs in this Chunk: {len(current_chunk)} (From bug {start_idx + 1} to {end_idx if end_idx < len(unique_bugs) else len(unique_bugs)})\n")
            md_file.write("---\n")  # 구분선
            details_list = []
            for bug in current_chunk:
                comment_url = f"{base_url}/{bug['id']}/comment"
                comment_response = requests.get(comment_url)
                comments_data = comment_response.json().get("bugs", {}).get(str(bug['id']), {}).get("comments", [])
                description = comments_data[0]['text'] if comments_data else "No comments available."           # 첫 번째 코멘트를 본문 내용으로 사용
                
                # 상세 정보를 딕셔너리로 조합
                details = {
                    "compiler": f"{compiler_name}",
                    "title": bug['summary'],
                    "open_at": bug['creation_time'],
                    "last_modified_date": bug['last_change_time'],
                    "link": f"{base_url.replace('rest.cgi/bug', 'show_bug.cgi')}?id={bug['id']}",
                    "status": bug['status'],
                    "tags": bug['keywords'],
                    "component": bug['component'],
                    "version": bug['version'],
                    "severity": bug['severity'],
                    "contents": description,
                }
                
                details_list.append(details)

                md_file.write("\n\n")  # 구분선
                md_file.write(f"### compiler : `{compiler_name}`\n")
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
            json.dump(details_list, json_file, ensure_ascii=False, indent=4)

# 버그질라에서 버그 리포팅을 수집하는 함수
def scraping_bugs_from_bugzilla(base_url, compiler_name, search_keywords):
    # 현재 날짜에서 5년 전의 날짜 계산
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=5*365)  # 대략적인 5년 전
    now = datetime.datetime.now()    # 현재 시간을 기반으로 md, json 파일 이름을 생성함
    formatted_time = now.strftime('%Y%m%d_%H%M%S')  # Format the datetime object to string: YYYYMMDD_HHMMSS

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
        response = requests.get(base_url, params=params)
        bugs.extend(response.json().get("bugs", []))

    if compiler_name == 'gcc':
        # 버그 id를 기반으로 중복 제거 및 관련 컴포넌트 필터링
        unique_bugs = {bug['id']: bug for bug in bugs if bug['component'] in gcc_relevant_components}.values()
    else:
        # 버그 id를 기반으로 중복 제거
        unique_bugs = {bug['id']: bug for bug in bugs}.values()
    
    # unique_bugs를 파일로 저장, chunk size 기준으로 md, json 파일 생성
    save_to_files(base_url, compiler_name, formatted_time, unique_bugs)


if __name__ == "__main__":
    # ThreadPoolExecutor를 사용하여 병렬 처리
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(scraping_bugs_from_bugzilla, "https://gcc.gnu.org/bugzilla/rest.cgi/bug", "gcc", keywords),
            executor.submit(scraping_bugs_from_bugzilla, "https://bugs.llvm.org/rest.cgi/bug", "llvm", keywords)
        ]
        wait(futures)
