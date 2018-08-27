import tushare as ts
import pickle

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
    print("h")
    hist = ts.get_h_data(stock_id, start=start_date, end=end_date)
    print("done")
    sync_list = ['open', 'close', 'high', 'low']
    rm_list = ['ma5', 'ma10', 'ma20', 'price_change', 'p_change']
    print(raw_k['open'].values)
    for sync in sync_list:
        #pass
        raw[sync] = raw_k[sync].values
    
    raw = raw.drop(rm_list, axis=1)

    print(raw[:6])
    print(hist[:6])
    print(raw_k[:6])
    
if __name__=="__main__":
    #get_data()
    adj('600016', '2018-07-03', '2018-07-10')
