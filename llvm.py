import requests
import json

GITHUB_TOKEN = "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"

labels = ["clang:frontend", "clang:codegen", 
          "c99", "c++26", "c23", "c++23", "c++20", "c17", "c++17", "c++14", "c11", "c++11", "c++", "c"]
discard_labels = ["question", "c++/cli", "clang:analysis", "code"]

def get_llvm_issue() :
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    params = {
        # "labels": "backend:RISC-V",
        "per_page": 100,
        "page": 1
    }

    url = "https://api.github.com/repos/llvm/llvm-project/issues"

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        issues = list(response.json())
        for issue in issues :
            first_issue_json = json.dumps(issue, indent=4)
            print(first_issue_json)
    else:
        print(f"Error {response.status_code}: {response.text}")

get_llvm_issue()