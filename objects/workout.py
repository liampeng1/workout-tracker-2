
from datetime import datetime
from typing import List
import json

class Workout:

  def __init__(self, date_time: datetime, input_string: str, notes: str) -> None:
    self.date_time = date_time
    self.input_string = input_string
    self.notes = notes

  @staticmethod
  def from_dict(source: dict):
    workout_type = source['workout_type']
    if workout_type == Run.type_name:
      return Run.from_dict(source)
    elif workout_type == Lift.type_name:
      return Lift.from_dict(source)
    else:
      raise Exception(f'Workout Type: {workout_type} not supported')

  def to_dict(self):
    return {
      'workout_type': self.type_name,
      'date_time': self.date_time,
      'input_string': self.input_string,
      'notes': self.notes
    }
  
  def __str__(self):
    return f'{self.type_name} at {str(self.date_time)}'

class Run(Workout):

  type_name = 'RUN'

  def __init__(self, date_time: datetime, input_string: str, notes: str, distance_mi: float, duration_sec: int) -> None:
      super().__init__(date_time, input_string, notes)
      self.distance_mi = distance_mi
      self.duration_sec = duration_sec

  @staticmethod
  def from_dict(source: dict):
    return Run(source['date_time'], source['input_string'], source['notes'], source['distance_mi'], source['duration_sec'])

  def to_dict(self):
    d = super().to_dict()
    d['distance_mi'] = self.distance_mi
    d['duration_sec'] = self.duration_sec
    return d
  
  def __str__(self) -> str:
    dur_min, dur_sec = self.duration_sec // 60, self.duration_sec % 60
    return f'''{super().__str__()}
    Distance: {self.distance_mi} mi
    Duration: {dur_min}:{dur_sec}
    '''

class Lift:

  def __init__(self, lift_name: str, sets: List[int]) -> None:
    self.lift_name = lift_name
    self.sets = sets

  @staticmethod
  def from_dict(source: dict):
    return Lift(source['lift_name'], source['sets'])

  def to_dict(self):
    return {
      'lift_name': self.lift_name,
      'sets': self.sets
    }

  def __str__(self):
    sets_str = ', '.join(self.sets)
    return f'{self.lift_name}: {sets_str}'

class Gym(Workout):

  type_name = 'GYM'

  def __init__(self, date_time: datetime, input_string: str, notes: str, lifts: List[Lift]) -> None:
    super().__init__(date_time, input_string, notes)
    self.lifts = lifts

  @staticmethod
  def from_dict(source: dict):
    lifts = [Lift(lift_source) for lift_source in source['lifts']]
    return Gym(source['date_time'], source['input_string'], source['notes'], lifts)

  def to_dict(self):
    d = super().to_dict()
    d['distance_mi'] = self.distance_mi
    d['duration_sec'] = self.duration_sec
    return d
  
  def __str__(self) -> str:
    lifts_str = '\n'.join([str(lift) for lift in self.lifts])
    return f'''{super().__str__()}
    {lifts_str}
    '''