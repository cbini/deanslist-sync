import os
from datetime import datetime, timedelta

from dateutil import tz
from dotenv import load_dotenv

load_dotenv()

local_tz = os.getenv("LOCAL_TIMEZONE")
current_academic_year = int(os.getenv("CURRENT_ACADEMIC_YEAR"))
first_academic_year = int(os.getenv("FIRST_ACADEMIC_YEAR"))

now = datetime.now(tz=tz.gettz(local_tz)).date()
updated_since = now - timedelta(days=3)
updated_since_strf = updated_since.strftime("%Y-%m-%d")
ay_start_date = f"{current_academic_year}-07-01"
ay_end_date = f"{current_academic_year + 1}-06-30"

endpoint_queries = [
    {"name": "terms", "path": "v1/terms"},
    {"name": "lists", "path": "v1/lists"},
    {
        "name": "users",
        "path": "beta/export/get-users.php",
        "parameters": {"show_inactive": "Y"},
    },
    {
        "name": "rosters",
        "path": "v1/rosters",
        "parameters": {"show_inactive": "Y"},
    },
    {
        "name": "communication",
        "path": "beta/export/get-comm-data.php",
        "parameters": {
            "UpdatedSince": updated_since_strf,
            "IncludeDeleted": "Y",
            "IncludePrevEnrollments": "Y",
        },
    },
    {
        "name": "followups",
        "path": "v1/followups",
        # "parameters": {
        #     "iuid": "",
        #     "cuid": "",
        #     "sid": "",
        #     "out": "",
        #     "type": "",
        # },
    },
    {
        "name": "roster_assignments",
        "path": "beta/export/get-roster-assignments.php",
        # "parameters": {"rt": ""},
    },
    {
        "name": "incidents",
        "path": "v1/incidents",
        "parameters": {
            "cf": "Y",
            "UpdatedSince": updated_since_strf,
            "StartDate": ay_start_date,
            "EndDate": ay_end_date,
            "IncludeDeleted": "Y",
        },
    },
    {
        "name": "homework",
        "path": "beta/export/get-homework-data.php",
        "parameters": {
            "sdt": ay_start_date,
            "edt": ay_end_date,
            "UpdatedSince": updated_since_strf,
            "IncludeDeleted": "Y",
        },
    },
    {
        "name": "behavior",
        "path": "beta/export/get-behavior-data.php",
        "parameters": {
            "sdt": ay_start_date,
            "edt": ay_end_date,
            "UpdatedSince": updated_since_strf,
            "IncludeDeleted": "Y",
        },
    },
    # {
    #     "name": "points_bank_book",
    #     "path": "beta/bank/get-bank-book.php",
    #     "parameters": {
    #         "rid": "",
    #         "sid": "",
    #         "stus": "",
    #     },
    # },
    # {
    #     "name": "message_center_events",
    #     "path": "v1/connect/events",
    #     "parameters": {
    #         "StartDate": "",
    #         "EndDate": "",
    #     },
    # },
    # {
    #     "name": "students",
    #     "path": "v1/students",
    #     "parameters": {
    #         "StudentID": "",
    #         "IncludeParents": "",
    #         "IncludeUnenrolled": "",
    #     },
    # },
    # {
    #     "name": "daily_attendance",
    #     "path": "v1/daily-attendance",
    #     "parameters": {
    #         "sdt": "",
    #         "edt": "",
    #         "UpdatedSince": "",
    #         "include_iac": "",
    #     },
    # },
    # {
    #     "name": "class_attendance",
    #     "path": "v1/class-attendance",
    #     "parameters": {
    #         "sdt": "",
    #         "edt": "",
    #         "UpdatedSince": "",
    #     },
    # },
    # {
    #     "name": "meals",
    #     "path": "v1/meals",
    #     "parameters": {
    #         "MealID": "",
    #         "RosterID": "",
    #         "sdt": "",
    #         "edt": "",
    #     },
    # },
]
