from tkinter import filedialog
from datetime import datetime, timedelta
from math import ceil
import matplotlib.pyplot as plt

TIMESTEP_MINUTES: float = 5

class Analizer(object):
  """Central object for all tasks concerning turning raw time log text file into a plot"""
  def __init__(self):
    self.fp = filedialog.askopenfile()
    self.content = self.fp.readlines() 
    self.timestamps = [
      datetime.strptime(x.replace('\n', '').strip(), '%H:%M %d-%m-%Y') 
      for x in self.content
      ]
    
  def segregate_timestamps(self) -> None:
    """function that aggregares raw timestamps to steps separated by TIMESTEP_MINUTES"""
    self.first = self.timestamps[0]
    self.last = self.timestamps[-1]
    period = self.last - self.first
    period = period.total_seconds() / ( TIMESTEP_MINUTES * 60 ) # total TIMESTEP_MINUTES minute blocks
    segregated = {
      step: [
          x for x in self.timestamps 
          if 
          x >= (self.first + (timedelta(minutes = step * TIMESTEP_MINUTES)))  
          and
          x < (self.first + (timedelta(minutes = (step + 1) * TIMESTEP_MINUTES)))
        ]
      for step in range( ceil(period) )
      }
    self.segregated = segregated

  def plot_segregated(self) -> None:
    """plots the segregated data and displays the plot"""
    x_axis = [( self.first + timedelta(minutes = step * TIMESTEP_MINUTES) ).strftime('%H:%M') for step in self.segregated.keys()]
    y_axis = [len( timestamps ) for timestamps in self.segregated.values()]
    plt.plot(x_axis, y_axis)
    plt.yticks(
        [ 
          min([len(x) for x in self.segregated.values()]) - 1, 
          max([len(x) for x in self.segregated.values()]) + 1, 
          1 
        ]
      )
    plt.show() 
    
if __name__ == '__main__':
  client = Analizer()
  client.segregate_timestamps()
  client.plot_segregated()