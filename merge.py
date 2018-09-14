#!/usr/bin/python3.5
import tushare as ts
import pandas as pd
import pickle
import os


def get_data():
    '''
    raw = ts.get_hist_data('002236', start='2018-01-01')
    sraw = raw[:3]

    save('sraw.data', sraw)2018-06-25
    print(sraw)
    '''
    sraw = load('sraw.data')
    print(sraw)
    new_index = sraw.index
    new_index = new_index.insert(0, '2018-06-26')
    new_index = new_index.delete(3)
    print(new_index)
    print(sraw)

def save(filename, data):
    with open(filename, 'wb') as f:
            pickle.dump(data, f)

def load(filename):
    data = None
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    return data 


def adj(stock_id, start_date, end_date):
    print("k")
    raw_k = ts.get_k_data(stock_id, start=start_date, end=end_date)
    print("hist")
    raw = ts.get_hist_data(stock_id, start=start_date, end=end_date)
    print("done")
    sync_list = ['open', 'close', 'high', 'low']
    rm_list = ['ma5', 'ma10', 'ma20', 'price_change', 'p_change']
    print(raw_k['open'].values)
    for sync in sync_list:
        #pass
        raw[sync] = raw_k[sync].values
    
    raw = raw.drop(rm_list, axis=1)
    raw.to_csv(stock_file_name(stock_id))
    print(raw[:6])
    #print(hist[:6])
    print(raw_k[:6])

def stock_file_name(stock_id):
    return "%s.csv" % stock_id

def cut_df(df, start_date, end_date):
    df = df.iloc[::-1]
    df = df.truncate(before=start_date, after=end_date)
    res = df.iloc[::-1]
    return res

def read_stock_by_ts(stock_id, start_date, end_date):
    print("read stock from internet by ts")
    print("get k")
    raw_k = ts.get_k_data(stock_id, start=start_date, end=end_date)
    print("get hist")
    raw = ts.get_hist_data(stock_id, start=start_date, end=end_date)
    print("done")
    sync_list = ['open', 'close', 'high', 'low']
    rm_list = ['ma5', 'ma10', 'ma20', 'price_change', 'p_change']
    for sync in sync_list:
        raw[sync] = raw_k[sync].values
    
    raw = raw.drop(rm_list, axis=1)
    raw = raw.set_index('date')
    return raw

def read_stock_hist(stock_id, start_date, end_date):
    start, end, df = load_stock(stock_id)
    if start !=[] and start>=start_date and end <=end_date:

        return cut_df(df, start_date, end_date)

    raw = read_stock_by_ts(stock_id, start_date, end_date)
    raw.to_csv(stock_file_name(stock_id))
    return raw

def load_stock(stock_id):
    filename = stock_file_name(stock_id)
    if not os.path.isfile(filename):
        print("Not exist %s" % filename)
        return [], [], []

    df = pd.read_csv(filename)
    df = df.set_index('date')
    return df.index.min(), df.index.max(), df

if __name__=="__main__":
    #get_data()
    #adj('600016', '2018-07-03', '2018-07-20')
    raw = read_stock_hist('600017', '2018-07-03', '2018-07-20')
    print(raw[:4])
