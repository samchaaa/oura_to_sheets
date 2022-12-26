import pandas as pd
import datetime

# import matplotlib.pyplot as plt
# import seaborn as sns
# sns.set_style('whitegrid')

from oura_ring import OuraClient
import gspread

from config import config

def excel_date(date1):
    """
    converts datetime date to excel int date
    https://stackoverflow.com/a/9574948
    """
    temp = datetime.datetime(1899, 12, 30)    # Note, not 31st Dec but 30th!
    delta = date1 - temp
    return float(delta.days) + (float(delta.seconds) / 86400)

# read in credentials and init client
f = open(config.oura_key, 'r').read()
client = OuraClient(f)

# gets last week data for everything
tdy = datetime.datetime.strftime(datetime.datetime.today() - datetime.timedelta(days=0), '%Y-%m-%d')
ydy = datetime.datetime.strftime(datetime.datetime.today() - datetime.timedelta(days=config.days), '%Y-%m-%d')
print('retrieving from {} to {}'.format(ydy, tdy))

# # get heartrate
# hr = client.get_heart_rate(ydy, tdy)
# hr = pd.DataFrame(hr).set_index('timestamp').drop(columns=['source'])
# hr.index = [pd.to_datetime(_.replace('+00:00', '')) for _ in hr.index]
# hr.index = hr.index.tz_localize('UTC')
# hr.index = hr.index.tz_convert('Asia/Seoul')

# get sleep duration
sleep = client.get_sleep_periods(ydy, tdy)
s = [
    {
        x: _[x] for x in _ if x in [
            'day',
            'bedtime_end',
            'bedtime_start',
            'total_sleep_duration',
        ]
    } for _ in sleep
]
for _ in s:
    _['dur'] = pd.to_datetime(_['bedtime_end']) - pd.to_datetime(_['bedtime_start'])
total_sleep = pd.DataFrame(s)[['day', 'total_sleep_duration']].groupby('day').sum() / 60 / 60
print('total sleep:')
print(total_sleep)

# get avg hrv
results = []
for s in sleep:
    hrv = None
    if s['heart_rate']:
        hr = pd.DataFrame(s['heart_rate']['items'])
        # hrv = ((60000 / hr).diff() ** 2).mean() ** 0.5
        # hrv = hrv.values[0]
    results.append({
        'start': s['bedtime_start'],
        'avg_hrv': s['average_hrv'],
        # 'calc_hrv': hrv,
        'day': s['day']
    })
avg_hrv = pd.DataFrame(results)[['day', 'avg_hrv']].groupby('day').mean()
print('avg hrv:')
print(avg_hrv)

# join
to_write = total_sleep.join(avg_hrv).reset_index()
to_write['day'] = to_write['day'].apply(lambda x: excel_date(datetime.datetime.strptime(x, '%Y-%m-%d')))
print('to write to sheets:')
print(to_write)

# check what's currently in the sheet
gc = gspread.service_account(config.svc_acct_json)
sh = gc.open_by_key(config.sheet_id)
wks = sh.worksheet(config.tab_name)
data = wks.get_all_values()

# if no data, write everything
if not len(data):
    wks.update(
        [to_write.columns.to_list()] +  to_write.values.tolist()
    )

# if data, only append what's not already in data
elif len(data):
    wks.append_rows(
        [_ for _ in to_write.values.tolist()
        if _[0] not in [float(_[0].replace(',', '')) for _ in data[1:]]] # filters data to push only what's not in the sheet
    )
