# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import signal
import sys
from objects.workout import Workout, Run
import datetime
from types import FrameType
import json
from flask import Flask, Request
from utils.logging import logger
from google.cloud import firestore

db = firestore.Client()

app = Flask(__name__)

@app.route("/")
def hello() -> str:
    # Use basic logging with custom fields
    logger.info(logField="custom-entry", arbitraryField="custom-entry")

    # https://cloud.google.com/run/docs/logging#correlate-logs
    logger.info("Child logger with trace Id.")

    return "Hello, World!"


@app.route('/add-workout')
def add_workout():
  workout_strings = Request.get_json()['input_string'].split('\n')
  workout_type = workout_strings[0].lower()
  if 'run' in workout_type:
    run = build_run(workout_strings)
    add_workout(run)
    d = run.to_dict()
    d['date_time'] = str(d['date_time'])
    return json.dumps(d)
  else:
    return f'Workout type: {workout_type} is not supported.'

def build_run(workout_strings):
  run_dist, run_duration, notes = float(workout_strings[1]), int(workout_strings[2]), workout_strings[3]
  return Run(datetime.now(), '\n'.join(workout_strings), notes, run_dist, run_duration)

def add_workout(workout: Workout):
  doc_name = str(workout.date_time)
  db.collection('workouts').document(doc_name).set(workout.to_dict())

def shutdown_handler(signal_int: int, frame: FrameType) -> None:
    logger.info(f"Caught Signal {signal.strsignal(signal_int)}")

    from utils.logging import flush

    flush()

    # Safely exit program
    sys.exit(0)


if __name__ == "__main__":
    # Running application locally, outside of a Google Cloud Environment

    # handles Ctrl-C termination
    signal.signal(signal.SIGINT, shutdown_handler)

    app.run(host="localhost", port=8080, debug=True)
else:
    # handles Cloud Run container termination
    signal.signal(signal.SIGTERM, shutdown_handler)
