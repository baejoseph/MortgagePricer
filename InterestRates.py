class InterestRates:
  """A class to capture interest rate info"""
  def __init__(self, **kwargs):
    self.set_times(kwargs['times'])
    self.set_rates(**kwargs)

  def set_times(self, values):
    self._times = values

  def get_times(self):
    return self._times

  def set_rates(self, **kwargs):
    self._rates = kwargs['rates']

    if 'margin' in kwargs:
      self._rates = [x + kwargs['margin'] for x in self._rates]

    if ('fixed_term' in kwargs) and ('fixed_rate' in kwargs):
      fixed_term = kwargs['fixed_term']
      fixed_rate = kwargs['fixed_rate']
      time_rates = [(t,r) for t,r in zip(self._times, self._rates)]

      indices = [i for i, tup in enumerate(time_rates) if tup[0] < fixed_term]
      for index in indices[::-1]:
        time_rates.pop(index)
      fixed_times = [round(x/12,4) for x in range(fixed_term*12)]
      for time in fixed_times:
        time_rates.append((time, fixed_rate))
      new_times = []
      new_rates = []
      for tupl in sorted(time_rates):
        new_times.append(tupl[0])
        new_rates.append(tupl[1])
      self._times = new_times
      self._rates = new_rates

  def get_rates(self):
    return self._rates

  def get_rate(self, time, interpolation = 'linear'):
    return np.interp(time, self._times, self._rates)

  def plot_rates(self):
    ax = plt.gca()
    ax.set_xlabel('years')
    ax.set_ylabel('rates (%)')
    ax.plot(self._times, self._rates)
    return ax

  def monthly_rates(self, term=None):
    if term is None: term = self._times[-1]

    new_times = [round(x/12,4) for x in range(term*12)]
    self._rates = [self.get_rate(time) for time in new_times]
    self._times = new_times
