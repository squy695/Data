from cProfile import run
import random
import pandas as pd
import locust.stats
from locust import HttpUser, between, task, LoadTestShape, events
import time

locust.stats.CSV_STATS_INTERVAL_SEC = 5
locust.stats.CSV_STATS_FLUSH_INTERVAL_SEC = 5

products = [
'0PUK6V6EV0',
'1YMWWN1N4O',
'2ZYFJ3GM2N',
'66VCHSJNUP',
'6E92ZMYYFZ',
'9SIQT8TOJO',
'L9ECAV7KIM',
'LS4PSXUNUM',
'OLJCESPC7Z']


class WebsiteUser(HttpUser):
    wait_time = between(0.5, 1.5)

    @task
    def index(self):
        headers = {"Connection": "close"}
        self.client.get("/", headers=headers)



class DynamicStress(LoadTestShape):
    """
    Settings:
        min_users -- min users
        max_users -- max users
        time_limit -- total length of test
    """
    wave_df = pd.read_csv('onlineboutique/locust/wiki/1.csv')
    wave_list = wave_df['count'].tolist()
    time_limit = 1* 60 * 60
    df = pd.DataFrame(columns=["stamp", "uc"])

    def tick(self):
        run_time = round(self.get_run_time())
        index = int(run_time)

        if run_time < self.time_limit:
            user_count = self.wave_list[index]
            return (round(user_count), 5)
        else:
            return None
        
