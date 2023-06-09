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

import flask
import json
from flask.testing import FlaskClient

RUN_WORKOUT_INPUT_STRING = '''run
5
3000
Felt pretty good.'''

GYM_WORKOUT_INPUT_STRING = '''gym
squat 5 5 5 5
bench 6 8 10 8 6
Tough workout. Really sore.'''

def test_get_index(app: flask.app.Flask, client: FlaskClient) -> None:
    res = client.get("/")
    assert res.status_code == 200

def test_post_index(app: flask.app.Flask, client: FlaskClient) -> None:
    res = client.post("/")
    assert res.status_code == 405

def test_add_workout_run(app: flask.app.Flask, client: FlaskClient) -> None:
    res = client.post(
        "/add-workout",
        data=json.dumps({'input_string': RUN_WORKOUT_INPUT_STRING}),
        content_type='application/json')
    assert res.status_code == 200

def test_add_workout_gym(app: flask.app.Flask, client: FlaskClient) -> None:
    res = client.post(
        "/add-workout",
        data=json.dumps({'input_string': GYM_WORKOUT_INPUT_STRING}),
        content_type='application/json')
    assert res.status_code == 200

def test_get_workouts(app: flask.app.Flask, client: FlaskClient) -> None:
    res = client.get("/get-workouts")
    assert res.status_code == 200