from datetime import datetime
from dateutil.relativedelta import relativedelta
import requests, json
from lib.broker_api.announcement import Announcement
from requests.auth import HTTPBasicAuth

from repos.announcement_database import AnnouncementDatabase


class CorporateApi:
    def __init__(self, pub_key, priv_key):
        self.pub_key = pub_key
        self.priv_key = priv_key
        self.api_link = "https://broker-api.sandbox.alpaca.markets"

    def getAnnoucements(self, types, since, until, subtype=None):
        params = {"ca_types": types, "since": since, "until": until}
        print(params)
        data = requests.get(
            self.api_link + "/v1/corporate_actions/announcements",
            auth=HTTPBasicAuth(self.pub_key, self.priv_key),
            params=params,
        )

        if data.status_code != 200:
            raise Exception(f"Request failed: {data.text}")

        actions = json.loads(data.text)

        foo = []

        for action in actions:
            target_symbol = action.get("target_symbol", "")
            init_symbol = action.get("initiating_symbol", "")
            if init_symbol != "" or target_symbol != "":
                foo.append(Announcement.fromJson(action))
        return foo

    def getAllAnnouncements(self, types, since, until):
        print("STARTING")
        start_date = datetime.fromisoformat(since)
        end_date = datetime.fromisoformat(until)
        days = (end_date - start_date).days
        date_set_ammount = days // 90
        remainder_days = days % 90
        number_of_sets = date_set_ammount + 1

        date_sets = []

        for i in range(date_set_ammount):
            date_set = [start_date.strftime("%Y-%m-%d")]
            start_date += relativedelta(days=90)
            date_set.append(start_date.strftime("%Y-%m-%d"))
            start_date += relativedelta(days=1)
            date_sets.append(date_set)

        final_set = [start_date.strftime("%Y-%m-%d")]
        start_date += relativedelta(days=remainder_days - date_set_ammount)
        final_set.append(start_date.strftime("%Y-%m-%d"))
        print("FINAL SET", final_set)
        date_sets.append(final_set[::-1])

        all_announcements = []
        for date_set in date_sets:
            announcements = self.getAnnoucements(types, date_set[0], date_set[1])
            print(date_set[0], date_set[1], len(announcements))
            all_announcements += announcements

        return all_announcements


if __name__ == "__main__":
    database = AnnouncementDatabase()
    pub_key = "CK2MUIPWZYJOA0RK99NU"
    priv_key = "7NNARkkrcdEepZcIJM29PZhkvQZMxXoCXzbT9Swx"
    api_link = "https://broker-api.sandbox.alpaca.markets"

    corp = CorporateApi(pub_key, priv_key)
    announcements = corp.getAllAnnouncements(["split"], "2018-01-01", "2022-05-01")

    # announcements = corp.getAnnoucements(['split'], '2020-11-01', '2020-12-01', subtype="reverse_split")
    for announcement in announcements:
        a = database.saveAnnouncement(announcement)
        print(a)

    print(len(announcements))
