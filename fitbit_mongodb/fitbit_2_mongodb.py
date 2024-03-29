#!/usr/bin/env python3

import argparse
import datetime as dt
import fitbit
import logging
import os
import sys
from pymongo import MongoClient
from pymongo.helpers import DuplicateKeyError
from refresh_tokens import get_fresh_tokens
from fitbit_mongodb.connect_mongodb import mongodb_client

class Loader():
    """ Data loader for Fitbit into MongoDB """

    def __init__(self, verbose=None):
        """ Set up connection details """
        if not verbose:
            log_level = logging.INFO
        else:
            log_level = logging.DEBUG
        stdout_handler = logging.StreamHandler(sys.stdout)
        logging.basicConfig(
            level=log_level,
            handlers=[stdout_handler]
        )
        self.logger = logging.getLogger(name="fitbit-mongodb-loader")

        # get clientinfo from mongodb
        ci = mongodb_client.fitbit.client_info
        d = [i for i in ci.find()][0]
        try:
            key = d["CLIENT_ID"]
            secret = d["CLIENT_SECRET"]
            access_token = d["ACCESS_TOKEN"]
            refresh_token = d["REFRESH_TOKEN"]
            self.fitbit_client = fitbit.Fitbit(
                key,
                secret,
                access_token=access_token,
                refresh_token=refresh_token
            )
        except Exception as e:
            print(e)
            key,secret,access_token,refresh_token = get_fresh_tokens()
            self.fitbit_client = fitbit.Fitbit(
                key,
                secret,
                access_token=access_token,
                refresh_token=refresh_token
            )
        # Create MongoDB connection
        # mongodb_client = MongoClient()
        self.db = mongodb_client.fitbit

        # Empty vars -- need to be filled by child class
        self.collection_name = None
        self.document_key = None
        self.timestamp_key = None
        self.request_args = {}

    def configure_collection(self):
        """ Ensure that the collection is created and indexed """
        if not self.document_key:
            raise ValueError("self.document_key must not be None")
        if not self.timestamp_key:
            raise ValueError("self.timestamp_key must not be None")
        # Define index
        self.mongodb_index = "{}.0.{}".format(
            self.document_key,
            self.timestamp_key
        )
        # Create collection if not exists
        if not self.collection_name in self.db.list_collection_names():
            self.db.create_collection(self.collection_name)
        # Make sure unique index is created
        collection = self.db.get_collection(self.collection_name)
        collection.create_index(self.mongodb_index, unique=True)

    def get_fitbit_data(self, request_args):
        """ Get FitBit data """
        return self.fitbit_client.time_series(**request_args)

    def load_date(self, date=None, update=False):
        """
        Load data from a specific date
        """
        self.request_args["base_date"] = date

        # First make sure MongoDB is set up properly
        self.configure_collection()
        collection = self.db.get_collection(name=self.collection_name)

        # Check if data is already in MongoDB
        mongo_query = {
            self.mongodb_index: date
        }
        cursor = collection.find(mongo_query)
        documents = [x for x in cursor]
        document_count = len(documents)
        self.logger.debug(
            "MongoDB query {} returned {} documents".format(
                mongo_query,
                document_count
            )
        )
        if document_count > 0:
            if document_count > 1:
                raise RuntimeError(
                    "Duplicate entry detected, your database "
                    "is missing the uniqueness constrained index."
                )
            # Exactly one match was found
            if not update:
                self.logger.warning(
                    (
                        "Document already exists in {} for this date, "
                        "skipping {}"
                    ).format(
                        self.collection_name,
                        date
                    )
                )
                return None
            else:
                document_id = documents[0]["_id"]

        # Get data from FitBit API
        self.logger.info("Connecting to FitBit API...")
        data_blob = self.get_fitbit_data(self.request_args)

        # Load data into MongoDB
        if update:
            collection.replace_one(
                {"_id": document_id},
                data_blob
            )
            self.logger.info(
                "Updated document {} for date {}".format(
                    document_id,
                    date
                )
            )
        else:
            try:
                collection.insert_one(data_blob)
                self.logger.info(
                    "Successfully wrote record for {}".format(
                        date
                    )
                )
            except DuplicateKeyError:
                self.logger.warning(
                    (
                        "Entry already exists, "
                        "failed to write data for date {}"
                    ).format(
                        date
                    )
                )
        return True

    def load_days(self, days=None):
        """
        Load data for <days> full days into the past
        from FitBit into MongoDB
        """
        if days is None or type(days) != int:
            raise TypeError("days must be an integer")
        today = dt.datetime.today()
        days_back = days
        all_dates = []
        while days_back > 0:
            date_text = dt.datetime.strftime(
                today - dt.timedelta(days=days_back),
                "%Y-%m-%d"
            )
            self.logger.debug("date_text: {}".format(date_text))
            all_dates.append(date_text)
            days_back -= 1
        self.logger.info("Preparing to load dates {}".format(all_dates))

        for base_date in all_dates:
            self.load_date(base_date)

class HeartLoader(Loader):
    """ Heart rate loader """
    def __init__(self, *args, **kwargs):
        super(HeartLoader, self).__init__(*args, **kwargs)
        self.collection_name = "heart"
        self.document_key = "activities-heart"
        self.timestamp_key = "dateTime"
        self.request_args = {
            "resource": "activities/heart",
            "detail_level": "1min"
        }

    def get_fitbit_data(self, request_args):
        """ Override parent for heart rate """
        return self.fitbit_client.intraday_time_series(**request_args)

class SleepLoader(Loader):
    """ Sleep data loader """
    def __init__(self, *args, **kwargs):
        super(SleepLoader, self).__init__(*args, **kwargs)
        self.collection_name = "sleep"
        self.document_key = "sleep"
        self.timestamp_key = "dateOfSleep"
        self.request_args = {}

    def get_fitbit_data(self, request_args):
        """ Get sleep data """
        date = dt.datetime.strptime(
            request_args["base_date"],
            "%Y-%m-%d"
        )
        return self.fitbit_client.get_sleep(date)

class StepLoader(Loader):
    """ Step data """
    def __init__(self, *args, **kwargs):
        super(StepLoader, self).__init__(*args, **kwargs)
        self.collection_name = "steps"
        self.document_key = "activities-steps"
        self.timestamp_key = "dateTime"
        self.request_args = {
            "resource": "activities/steps",
            "period": "1d"
        }

class FloorLoader(Loader):
    """ Floor data """
    def __init__(self, *args, **kwargs):
        super(FloorLoader, self).__init__(*args, **kwargs)
        self.collection_name = "floors"
        self.document_key = "activities-floors"
        self.timestamp_key = "dateTime"
        self.request_args = {
            "resource": "activities/floors",
            "period": "1d"
        }

class DistanceLoader(Loader):
    """ Distance data """
    def __init__(self, *args, **kwargs):
        super(DistanceLoader, self).__init__(*args, **kwargs)
        self.collection_name = "distance"
        self.document_key = "activities-distance"
        self.timestamp_key = "dateTime"
        self.request_args = {
            "resource": "activities/distance",
            "period": "1d"
        }

class CaloriesLoader(Loader):
    """ Calories data """
    def __init__(self, *args, **kwargs):
        super(CaloriesLoader, self).__init__(*args, **kwargs)
        self.collection_name = "calories"
        self.document_key = "activities-calories"
        self.timestamp_key = "dateTime"
        self.request_args = {
            "resource": "activities/calories",
            "period": "1d"
        }

class ActivityLoader(Loader):
    """ Activity data (walking, running, etc) """
    def __init__(self, *args, **kwargs):
        super(ActivityLoader, self).__init__(*args, **kwargs)

    def load(self, *args, **kwargs):
        # Prepare list of configs to use for the load method
        activity_types = [
            {
                "collection_name": "activity_sedentary",
                "document_key": "activities-minutesSedentary",
                "timestamp_key": "dateTime",
                "request_args": {
                    "resource": "activities/minutesSedentary",
                    "period": "1d"
                }
            },
            {
                "collection_name": "activity_lightly_active",
                "document_key": "activities-minutesLightlyActive",
                "timestamp_key": "dateTime",
                "request_args": {
                    "resource": "activities/minutesLightlyActive",
                    "period": "1d"
                }
            },
            {
                "collection_name": "activity_fairly_active",
                "document_key": "activities-minutesFairlyActive",
                "timestamp_key": "dateTime",
                "request_args": {
                    "resource": "activities/minutesFairlyActive",
                    "period": "1d"
                }
            },
            {
                "collection_name": "activity_very_active",
                "document_key": "activities-minutesVeryActive",
                "timestamp_key": "dateTime",
                "request_args": {
                    "resource": "activities/minutesVeryActive",
                    "period": "1d"
                }
            }
        ]
        for t in activity_types:
            self.collection_name = t["collection_name"]
            self.document_key = t["document_key"]
            self.timestamp_key = t["timestamp_key"]
            self.request_args = t["request_args"]
            # Call the parent's load method for each activity type
            super(ActivityLoader, self).load(*args, **kwargs)

def parse_args(args, type_choices):
    """ Parse CLI arguments """
    parser = argparse.ArgumentParser(
        description="Load FitBit data into MongoDB"
    )
    parser.add_argument(
        "--type",
        required=True,
        choices=type_choices
    )
    parser.add_argument(
        "--days",
        type=int,
        required=False
    )
    parser.add_argument(
        "--date",
        type=str,
        required=False
    )
    parser.add_argument(
        "--update",
        help="Update existing entry",
        action="store_true",
        required=False
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true"
    )
    parsed = parser.parse_args(args)
    if (parsed.days and parsed.date) or (parsed.date and parsed.days):
        parser.error("--date and --days are mutually exclusive")
    if parsed.days and parsed.days < 1:
        parser.error("Minimum days is 1")
    return parsed

def main():
    type_choices = {
        "heart": "HeartLoader",
        # "sleep": "SleepLoader",
        # "steps": "StepLoader",
        # "floors": "FloorLoader",
        # "distance": "DistanceLoader",
        # "activity": "ActivityLoader",
        # "calories": "CaloriesLoader"
    }

    for key in type_choices:
        type_choice = type_choices[key]
        loader = eval(
            "{}()".format(type_choice))

    loader.load_days(days=50)
    # loader.load_date(date=parsed.date, update=parsed.update)
    # if parsed.days:
    #     loader.load_days(days=parsed.days)
    # elif parsed.date:
    #     loader.load_date(date=parsed.date, update=parsed.update)
    # else:
    #     print("Exiting.")

if __name__ == "__main__":
    main()