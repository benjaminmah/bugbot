# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from libmozdata import utils as lmdutils

from bugbot import utils
from bugbot.bzcleaner import BzCleaner
from bugbot.escalation import Escalation
from bugbot.nag_me import Nag
from bugbot.round_robin import RoundRobin


class SiteScout(BzCleaner, Nag):
    def __init__(self):
        super(SiteScout, self).__init__()
        self.lookup = utils.get_config(self.name(), "weeks-lookup", 4)
        self.escalation = Escalation(
            self.people,
            data=utils.get_config(self.name(), "escalation"),
            skiplist=utils.get_config("workflow", "supervisor_skiplist", []),
        )
        self.round_robin = RoundRobin.get_instance()
        self.date = lmdutils.get_date_ymd("today")

    def description(self):
        return "Site-Scout dependent bugs without priority or severity"

    def nag_template(self):
        return self.template()

    def nag_preamble(self):
        return """<p>
  This report lists bugs that block the <a href="https://bugzilla.mozilla.org/show_bug.cgi?id=1847294">Site-Scout meta bug (1847294)</a> but do not have a priority or severity set.
  Setting these fields helps prioritize and triage issues effectively.
</p>"""

    def get_extra_for_template(self):
        return {"nweeks": self.lookup}

    def get_extra_for_needinfo_template(self):
        return self.get_extra_for_template()

    def get_extra_for_nag_template(self):
        return self.get_extra_for_template()

    def has_product_component(self):
        return True

    def ignore_meta(self):
        return True

    def columns(self):
        return ["product", "component", "id", "summary"]

    def get_bz_params(self, date):
        fields = [
            "id",
            "summary",
            "product",
            "component",
            "priority",
            "severity",
            "triage_owner",
            "blocked",
        ]

        return {
            "include_fields": fields,
            "resolution": "---",
            "f1": "blocked",
            "o1": "equals",
            "v1": "1847294",
        }

    def handle_bug(self, bug, data):
        if bug["priority"] == "--" or bug["severity"] == "--":
            bugid = str(bug["id"])
            data[bugid] = {
                "id": bugid,
                "summary": bug["summary"],
                "product": bug["product"],
                "component": bug["component"],
            }
            return bug
        return None

    def get_mail_to_auto_ni(self, bug):
        return None

    def set_people_to_nag(self, bug, buginfo):
        priority = "default"
        if not self.filter_bug(priority):
            return None

        owners = self.round_robin.get(bug, self.date, only_one=False, has_nick=False)
        real_owner = bug.get("triage_owner")
        self.add_triage_owner(owners, real_owner=real_owner)

        if not self.add(owners, buginfo, priority=priority):
            self.add_no_manager(buginfo["id"])

        return bug


if __name__ == "__main__":
    SiteScout().run()
