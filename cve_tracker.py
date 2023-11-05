import requests

def fetch_cve_data(keyword, num_pages):
    cve_items = []

    for i in range(num_pages):
        url = "https://services.nvd.nist.gov/rest/json/cves/1.0"
        params = {
            'keyword': keyword,
            'resultsPerPage': 10,  # 한 페이지 당 결과 수
            'startIndex': i * 10  # 시작 인덱스
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            cve_items.extend(data['result']['CVE_Items'])
        else:
            print("Failed to fetch data:", response.status_code)

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

def main():
    keyword = input("Enter the keyword: ")
    num_pages = int(input("Enter the number of pages to fetch: "))

    cve_items = fetch_cve_data(keyword, num_pages)
    save_to_md(cve_items, keyword)

if __name__ == "__main__":
    main()

