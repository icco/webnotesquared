#!/usr/bin/env python

import csv
import pylab
import datetime
from matplotlib.dates import date2num, MonthLocator, WeekdayLocator, \
                             DateFormatter, MONDAY

INPUT = 'usage.csv'

def str2date(str):
  return datetime.datetime(*[int(x) for x in str.split('-')])

def str2datetime(str):
  date, time = str.split(' ')
  tokens = date.split('-')
  tokens.extend(time.split(':'))
  return datetime.datetime(*[int(x) for x in tokens])

def timedelta2float(td):
  return float(td.days) + float(td.seconds) / (24*60*60)

def CreateTime():
  ''' workspaces create over time (bar chart) '''
  reader = csv.reader(file(INPUT, 'r'))
  date_map = {} # output
  wsid_last = -1
  for wsid, num_notes, datestr in reader:
    if wsid != wsid_last:
      key = datestr[:10]
      date_map.setdefault(key, 0)
      date_map[key] += 1
      wsid_last = wsid
  
  # now graph
  dates = date_map.keys()
  dates.sort()
  
  pylab.figure()
  ax = pylab.subplot(111)
  bars = pylab.bar([date2num(str2date(d)) for d in dates],
                   [date_map[d] for d in dates],
                   width = 0.75,
                   color = 'b')
  [bar.set_ec('b') for bar in bars]
  
  # set axes
  ax.xaxis.set_major_locator(MonthLocator(range(1,13), bymonthday=1))
  ax.xaxis.set_major_formatter(DateFormatter('%b %d, %Y'))
  ax.xaxis.set_minor_locator(WeekdayLocator(MONDAY))
  [tick.label.set_rotation('vertical') for tick in ax.xaxis.get_major_ticks()]
  ax.set_xlim([date2num(str2date(dates[0])),
               date2num(str2date(dates[-1]))])
  
  # set title
  ax.set_ylabel('number of workspaces created')
  ax.set_title('workspaces created per day')
  ax.set_position(pos = [0.08, 0.18, 0.82, 0.76])

  ax.grid(True)
  pylab.savefig('start_time')

  ax.set_ylim((0, 150))
  pylab.savefig('start_time_zoom')

def UsagePattern():
  ''' save note time relative to create note time '''
  reader = csv.reader(file(INPUT, 'r'))
  time_map = {} # output
  
  wsid_last = -1
  base_dt = None
  for wsid, num_notes, datestr in reader:
    if wsid != wsid_last:
      base_dt = str2datetime(datestr)
      wsid_last = wsid
    else:
      key = (str2datetime(datestr) - base_dt).days 
      freq = time_map.setdefault(key, {})
      freq.setdefault(num_notes, 0)
      freq[num_notes] += 1

  days = time_map.keys()
  days.sort()
  
  pylab.figure()
  ax = pylab.subplot(111)
  
  print days
  bars = pylab.bar(days,
                   [sum(time_map[d].values()) for d in days],
                   width = 0.75,
                   color = 'b')
  [bar.set_ec('b') for bar in bars]
  
  # set labels
  ax.set_title('workspaces saved relative to workspace creation')
  ax.set_xlabel('days since workspace creation')
  ax.set_ylabel('number of saves')
  ax.set_position(pos = [0.1, 0.10, 0.88, 0.84])

  ax.grid(True)
  pylab.savefig('save_relative')

  ax.set_ylim((0, 2000))
  pylab.savefig('save_relative_zoom')


def NumSaves():
  ''' histogram of number of saves per workspace '''
  reader = csv.reader(file(INPUT, 'r'))
  save_map = {} # output
  
  wsid_last = -1
  cnt = None
  for wsid, num_notes, datestr in reader:
    if wsid != wsid_last:
      if wsid_last != -1:
        save_map.setdefault(cnt, 0)
        save_map[cnt] += 1
      cnt = 1
      wsid_last = wsid
    else:
      cnt += 1
  
  saves = save_map.keys()
  saves.sort()
  
  pylab.figure()
  ax = pylab.subplot(111)
  bars = pylab.bar(saves,
                   [save_map[s] for s in saves],
                   width = 1.0,
                   color = 'b')
  [bar.set_ec('b') for bar in bars]
  
  # set labels
  ax.set_title('saves per workspace')
  ax.set_xlabel('number of saves')
  ax.set_ylabel('number of workspaces')
  ax.set_position(pos = [0.1, 0.10, 0.84, 0.84])

  ax.grid(True)
  pylab.savefig('save_frequency')

  ax.set_ylim((0, 500))
  ax.set_xlim((0, 300))
  pylab.savefig('save_frequency_zoom')


def ScatterNumNotes():
  ''' this is too busy and pretty worthless '''
  reader = csv.reader(file(INPUT, 'r'))
  pairs = []
  
  wsid_last = -1
  base_dt = None
  for wsid, num_notes, datestr in reader:
    if wsid != wsid_last:
      base_dt = str2datetime(datestr)
      wsid_last = wsid
    else:
      days = timedelta2float((str2datetime(datestr) - base_dt))
      pairs.append((days, int(num_notes)))

  pylab.figure()
  ax = pylab.subplot(111)
  polycol = pylab.scatter([p[0] for p in pairs],
                          [p[1] for p in pairs],
                          s=0.5,
                          c='b')
  polycol.set_linewidth(0)

  ax.set_title('notes vs days')
  ax.set_xlabel('days since creating workspace')
  ax.set_ylabel('number of notes')
  ax.set_position(pos = [0.1, 0.10, 0.84, 0.84])
  
  ax.set_ylim((0, 300))
  ax.set_xlim((0, 250))
  pylab.savefig('scatter')

def SaveVsTime():
  reader = csv.reader(file(INPUT, 'r'))
  date_map = {}
  for wsid, num_notes, datestr in reader:
    date = str2datetime(datestr).date()
    date_map[date] = date_map.get(date, 0) + 1

  dates = date_map.keys()
  dates.sort()
  
  pylab.figure()
  ax = pylab.subplot(111)
  lines = pylab.plot([date2num(d) for d in dates],
                   [date_map[d] for d in dates],
                   linewidth = 2,
                   color = 'b')
  #[bar.set_ec('b') for bar in bars]
  
  # set axes
  ax.xaxis.set_major_locator(MonthLocator(range(1,13), bymonthday=1))
  ax.xaxis.set_major_formatter(DateFormatter('%b %d, %Y'))
  ax.xaxis.set_minor_locator(WeekdayLocator(MONDAY))
  [tick.label.set_rotation('vertical') for tick in ax.xaxis.get_major_ticks()]
  ax.set_xlim([date2num(dates[0]), date2num(dates[-1])])
  
  # set title
  ax.set_ylabel('number of saves per day')
  ax.set_title('saves over time')
  ax.set_position(pos = [0.08, 0.18, 0.82, 0.76])

  ax.grid(True)
  pylab.savefig('saves_time')

if '__main__' == __name__:
  #CreateTime()
  #UsagePattern()
  #NumSaves()
  #ScatterNumNotes()
  SaveVsTime()
