import pandas as pd
import sys
import os
import numpy as np


def make():
    df = pd.read_excel('/Users/alex/Dropbox/CTA/FundReport.xlsx', sheet_name = '样本外周度', names = ['date', 'net_value'],
                    header=1)
    df['net_value'] = [round(float(a), 3) for a in df['net_value']]
    
    weekly_return = [0]*len(df)
    for i in range(len(df) - 1):
        weekly_return[i + 1] = df['net_value'][i+1]/df['net_value'][i] - 1
    df['weekly_return'] = weekly_return
    information_ratio = np.sqrt(52) * df['weekly_return'].mean()/df['weekly_return'].std()
    print("Information Ratio is %f"%information_ratio)
    sharpe_ratio = np.sqrt(52) * (df['weekly_return'].mean() - 0.02/52)/df['weekly_return'].std()
    print("Sharpe Ratio is %f"%sharpe_ratio)

    recent_year_return = df['weekly_return'][-52:]
    information_ratio = np.sqrt(52) * recent_year_return.mean()/recent_year_return.std()
    print("Recent Year Information Ratio is %f"%information_ratio)
    sharpe_ratio = np.sqrt(52) * (recent_year_return.mean() - 0.02/52)/recent_year_return.std()
    print("Recent Year Sharpe Ratio is %f"%sharpe_ratio)


    date_str = str(list([d.date().strftime('%Y-%m-%d') for d in df['date']]))
    data_str = str(list(df['net_value']))
    draw_down = [0]
    net_value = list(df['net_value'])
    pre_max = net_value[0]
    for i in range(1, len(net_value)):
        if net_value[i] > pre_max:
            pre_max = net_value[i]
        draw_down.append(round(-100*(1-net_value[i]/pre_max), 3))
    df = pd.read_excel('/Users/alex/Dropbox/CTA/FundReport.xlsx', sheet_name = '自营', header = 0)
    ytd = "%.2f%%"%(list(df['YTD'])[-1]*100)
    draw_down_str = str(draw_down)
    template = open('net_value_template.html').read()
    template = template.replace('dates_pos', date_str)
    template = template.replace('net_value_pos', data_str)
    template = template.replace('draw_down_pos', draw_down_str)
    template = template.replace('YTD', ytd)
    fp = open('net_value.html','w')
    fp.write(template)
    fp.close()

def send():
    cmd = 'scp net_value.html root@vps.yeshiwei.com:/var/www/html/'
    os.system(cmd)

if __name__ == "__main__":
    make()
    if len(sys.argv) == 2 and sys.argv[1] == 'send':
        send()
