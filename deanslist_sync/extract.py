import copy
import gzip
import json
import os
import pathlib
import traceback
from datetime import datetime

import requests
from dateutil.relativedelta import relativedelta
from google.cloud import storage
from settings import current_academic_year, endpoint_queries, first_academic_year

GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")
INSTANCE_NAME = os.getenv("INSTANCE_NAME")
DL_APP_CREDS = os.getenv("DEANSLIST_APPLICATION_CREDENTIALS")

PROJECT_PATH = pathlib.Path(__file__).absolute().parent
BASE_URL = f"https://{INSTANCE_NAME}.deanslistsoftware.com/api"

GCS_STORAGE_CLIENT = storage.Client()
GCS_BUCKET = GCS_STORAGE_CLIENT.bucket(GCS_BUCKET_NAME)


def get_endpoint_data(path, params):
    response = requests.get(url=f"{BASE_URL}/{path}", params=params)
    response.raise_for_status()

    response_json = response.json()
    data = response_json.get("data", [])
    deleted_data = [
        dict(d, **{"is_deleted": 1}) for d in response_json.get("deleted_data", []) if d
    ]
    return data + deleted_data


def is_date_param(key):
    return key in ["StartDate", "EndDate", "sdt", "edt"]


def update_param_val(val, decrement):
    new_val = datetime.strptime(val, "%Y-%m-%d") - relativedelta(years=(decrement + 1))
    return new_val.strftime("%Y-%m-%d")


def generate_historical_query(endpoint, decrement):
    new_endpt = copy.deepcopy(endpoint)
    new_params = new_endpt.pop("parameters")

    new_params.pop("UpdatedSince", None)
    new_params.pop("apikey", None)

    updated_params = {
        k: (update_param_val(v, decrement) if is_date_param(k) else v)
        for k, v in new_params.items()
    }
    new_endpt["parameters"] = updated_params
    return new_endpt


def main(school, queries):
    school_region = school["region-name"]
    school_name = school["school-name"]
    api_key = school["key"]
    print(f"{school_region} - {school_name}")

    school_queries = copy.deepcopy(queries)
    for q in school_queries:
        endpt_name = q.get("name", {})
        endpt_path = q.get("path")
        query_params = copy.deepcopy(q.get("parameters", {}))
        print(f"\t{endpt_name} - {query_params}")

        query_params_fmt = "".join(
            [f"{k}{v.replace('-', '')}" for k, v in query_params.items()]
        )
        query_params.update({"apikey": api_key})

        try:
            print(f"\t\tGET {endpt_path}")
            endpt_data = get_endpoint_data(endpt_path, query_params)

            data_path = PROJECT_PATH / "data" / school_region / endpt_name / school_name
            if not data_path.exists():
                data_path.mkdir(parents=True)
                print(f"\t\tCreated {'/'.join(data_path.parts[-4:])}...")

                if list(filter(is_date_param, query_params.keys())):
                    print("\t\tGenerating historical queries...")
                    for i, y in enumerate(
                        range(first_academic_year, current_academic_year)
                    ):
                        hist_query = generate_historical_query(q, i)
                        school_queries.append(hist_query)

            if endpt_data:
                if query_params_fmt:
                    data_filename = (
                        f"{endpt_name}_{school_name}_{query_params_fmt}.json.gz"
                    )
                else:
                    data_filename = f"{endpt_name}_{school_name}.json.gz"
                data_filepath = data_path / data_filename

                # save to json.gz
                with gzip.open(data_filepath, "wt", encoding="utf-8") as f:
                    json.dump(endpt_data, f)
                print(f"\t\tSaved to {'/'.join(data_filepath.parts[-5:])}!")

                # upload to GCS
                destination_blob_name = (
                    f"deanslist/{'/'.join(data_filepath.parts[-4:])}"
                )
                blob = GCS_BUCKET.blob(destination_blob_name)
                blob.upload_from_filename(data_filepath)
                print(f"\t\tUploaded to {destination_blob_name}!")
        except Exception as xc:
            print(xc)
            print(traceback.format_exc())
            continue


if __name__ == "__main__":
    try:
        with open(DL_APP_CREDS) as f:
            api_keys = json.load(f)

        for school in api_keys:
            main(school, endpoint_queries)
    except Exception as xc:
        print(xc)
        print(traceback.format_exc())
