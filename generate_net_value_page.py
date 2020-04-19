import pandas as pd
import sys
import os

def make():
    df = pd.read_excel('/Users/alex/Dropbox/CTA/FundReport.xlsx', sheet_name = '样本外周度', names = ['date', 'net_value'],
                    header=-1)
    date_str = str(list([d.date().strftime('%Y-%m-%d') for d in df['date']]))
    data_str = str(list(df['net_value']))
    template = open('net_value_template.html').read()
    template = template.replace('dates_pos', date_str)
    template = template.replace('net_value_pos', data_str)
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