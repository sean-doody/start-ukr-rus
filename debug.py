# %%
import json
import gzip
# %%
def load_data(path: str) -> list:
    with gzip.open(path, "rb") as f:
        data = json.loads(f.read().decode("utf-8"))
    return data
# %%
data = load_data(r"C:\Users\Sean\Sync\start\start-ukr-rus\data\international\int09\1539397762088697857.json.gz")
# %%
