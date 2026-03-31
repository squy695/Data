#!/usr/bin/python3

from random import randint, choice
import base64
from locust import HttpUser, task, between, LoadTestShape
from locust.clients import HttpSession
import locust.stats
import pandas as pd

locust.stats.CSV_STATS_INTERVAL_SEC = 5 # default is 1 second
locust.stats.CSV_STATS_FLUSH_INTERVAL_SEC = 5 # Determines how often the data is flushed to disk, default is 10 seconds

def get_base64(username, password):
    string = "%s:%s" % (username, password)
    string = string.encode()
    base64string = base64.b64encode(string)
    return base64string

auth_header = get_base64("123", "123456").decode()
print(auth_header)

class httpUser(HttpUser):
    wait_time = between(0.5, 1.5)

    @task
    def load(self):
        headers = {
            "Connection": "close"
        }
        
        item_id = '03fef6ac-1896-4ce8-bd69-b798f85c6e0b'
        self.client.get("/detail.html?id={}".format(item_id), headers=headers)

class DynamicStress(LoadTestShape):
    """
    Settings:
        min_users -- min users
        max_users -- max users
        time_limit -- total length of test
    """
    wave_df = pd.read_csv('sockshop/locust/wiki/8.csv')
    wave_list = wave_df['count'].tolist()
    time_limit = 1* 60 * 60
    df = pd.DataFrame(columns=["stamp", "uc"])

    def tick(self):
        run_time = round(self.get_run_time())
        index = int(run_time)

        if run_time < self.time_limit:
            user_count = self.wave_list[index] * 0.7 / 20
            return (round(user_count), 5)
        else:
            return None