import os
import time

import pandas as pd
import matplotlib.pyplot as pl


LOGS_DIR = "/service_data"
LOGS_PATH = os.path.join(LOGS_DIR, "service_log.csv")


while True:
    try:
        print(f"Считывание данных ...")
        df = pd.read_csv(LOGS_PATH, usecols=["absolute_error"])

        fig = pl.hist(df["absolute_error"].values)
        pl.title("Гистограмма")
        pl.xlabel("absolute_error")
        path = os.path.join(LOGS_DIR, "absolute_error.png")
        pl.savefig(path)
        pl.close()
        print(f"Гистограма обновлена в {path}")
    except Exception as e:
        print(f"{e}")
    time.sleep(5)
