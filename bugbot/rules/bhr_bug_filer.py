from selenium import webdriver
from selenium.webdriver.common.by import By

DASHBOARD_URL = "https://fqueze.github.io/hang-stats/"

BUGZILLA_API_URL = "https://bugzilla.mozilla.org/rest/bug"
BUGZILLA_API_KEY = "your_bugzilla_api_key_here"

BUG_DESCRIPTION_TEMPLATE = """
This bug is automatically filed for the stack:

Stack: {stack}
Total Time: {total_time}
Count: {count}

Please investigate the hang and take appropriate action.
"""


def fetch_dynamic_dashboard_data(url: str):
    driver = webdriver.Firefox()
    driver.get(url)

    driver.implicitly_wait(10)

    rows = driver.find_elements(By.XPATH, "//table/tbody/tr")

    data = []
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) >= 3:
            data.append(
                {
                    "rank": cells[0].text.strip(),
                    "total_time": cells[1].text.strip(),
                    "count": cells[2].text.strip(),
                    "stack": cells[3].text.strip() if len(cells) > 3 else None,
                }
            )

    driver.quit()
    return data


def filter_stacks_without_bugs(data):
    unassociated_stacks = []
    for item in data:
        if "Bug" not in item["stack"] and "Total" not in item["rank"]:
            unassociated_stacks.append(item)
    return unassociated_stacks


def create_bug(stack, dry_run=True):
    new_bug = {
        "summary": f"Investigate hang stack: {stack['stack']}",
        "product": "Core",
        "component": "General",
        "status_whiteboard": "[hang-stack-investigation]",
        "type": "task",
        "description": BUG_DESCRIPTION_TEMPLATE.format(
            stack=stack["stack"],
            total_time=stack["total_time"],
            count=stack["count"],
        ),
        "version": "unspecified",
    }

    if dry_run:
        print(f"Dry-run: Would create bug with the following data:\n{new_bug}")
    else:
        pass
        # response = requests.post(
        #     BUGZILLA_API_URL,
        #     headers={"Authorization": f"Bearer {BUGZILLA_API_KEY}"},
        #     json=new_bug,
        # )
        # if response.status_code == 201:
        #     print(f"Bug created successfully: {response.json()['id']}")
        # else:
        #     print(f"Failed to create bug: {response.status_code} {response.text}")


def main(dry_run=True):
    data = fetch_dynamic_dashboard_data(DASHBOARD_URL)

    unassociated_stacks = filter_stacks_without_bugs(data)

    print("Unassociated Stacks:")
    for stack in unassociated_stacks:
        print(stack)
        create_bug(stack, dry_run)


if __name__ == "__main__":
    main(dry_run=True)
