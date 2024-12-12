# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import pprint

from bugbot import logger
from bugbot.bzcleaner import BzCleaner


class FileNewBugs(BzCleaner):
    """A Bugbot rule template that files new bugs."""

    def __init__(self) -> None:
        super().__init__()
        # Implement function to retrieve information from dashboard and populate the list of bugs
        # The following bug data is placeholder
        self.bugs = [
            {
                "product": "Core",
                "component": "Performance",
                "summary": "Investigate performance issue for top stack [STACK_SIGNATURE]",
                "description": (
                    "This bug tracks a performance issue identified in Florian's dashboard: "
                    "https://fqueze.github.io/hang-stats/. The stack signature for this issue is [STACK_SIGNATURE].\n\n"
                ),
                "whiteboard": "[bhr]",
                "keywords": ["perf"],
                "platform": "All",
                "op_sys": "All",
                "version": "unspecified",
                "severity": "normal",
                "priority": "P3",
                "flags": [
                    {"name": "performance_impact", "status": "?"},
                ],
            },
        ]

    def get_bugs(self, date):
        self.query_url = None
        bugs = {}
        for num, bug in enumerate(self.bugs):
            logger.info("Processing bug data: %s", pprint.pformat(bug))

            if self.dryrun:
                bug_id = num
                logger.info("Dry-run: Would create bug: %s", bug)
                # bug = {"id": bug_id}
            else:
                pass
                # try:
                #     bug = utils.create_bug(data)
                #     bug_id = str(bug["id"])
                #     logger.info("Bug created: %s", bug_id)
                # except HTTPError as e:
                #     logger.error("Failed to create bug: %s. Error: %s", data["summary"], str(e))
                #     continue

            bugs[bug_id] = {
                "id": bug_id,
                "product": bug["product"],
                "component": bug["component"],
                "summary": bug["summary"],
            }
        return bugs

    def description(self) -> str:
        return "A rule that files new bugs."

    def columns(self):
        return ["id", "product", "component", "summary"]


if __name__ == "__main__":
    FileNewBugs().run()
