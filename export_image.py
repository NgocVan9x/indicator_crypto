import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import six
import time
import matplotlib.cbook as cbook
from PIL import Image


def render_mpl_table(data, title,font_size=12, row_colors=['#f1f1f2', 'w'], edge_color='w',
                     bbox=[0, 0, 1, 1],
                     ax=None, **kwargs):
    df = pd.DataFrame()
    df['Indicator'] = ['Day Ragnge','TD Sequential','RSI(14)', 'STOCH(9,6)', 'STOCHRSI(14)','MACD(12,26,9)','ADX(14)','William%R(14)','CCI(14)','ATR(14)'
    ,'HIGHS/LOWS(14)','U Oscilator(7,14,28)','ROC(9)','SMA(5)','SMA(10)','SMA(20)','SMA(50)','SMA(100)','SMA(200)'
    ,'EMA(5)','EMA(10)','EMA(20)','EMA(50)','EMA(100)','EMA(200)','total buy signals:','total sell signal:','total neutural signal:'
    ]
    df['Number']=data['Number']
    df['Type']=data['Type']
    # if ax is None:
    fig, ax = plt.subplots(figsize=(10, 10))
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')
    mpl_table = ax.table(cellText=df.values, bbox=bbox,**kwargs)
    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(font_size)

    for k, cell in  six.iteritems(mpl_table._cells):
        if k[1]==2:
            if cell.get_text().get_text() == "Buy" or cell.get_text().get_text() == "Strong Buy":
                cell.set_text_props( color='#00cc00')
            if cell.get_text().get_text() == "Sell" or cell.get_text().get_text() == "Strong Sell":
                cell.set_text_props(color='#ff3300')
        cell.set_edgecolor(edge_color)
        cell.set_facecolor(row_colors[k[0]%len(row_colors) ])
    im = Image.open('./logo_kts.png')
    height = im.size[1]
    im = np.array(im).astype(np.float) / 255
    # plt.plot(np.arange(10), 4 * np.arange(10))
    fig.figimage(im, 0, fig.bbox.ymax - height)
    fileName=str(int(time.time()))+".png"
    ax.set_title(title,color='green', fontsize=20,fontweight='bold')
    plt.savefig(fileName)
    return fileName
if __name__ == '__main__':
    data={}
    data['Number']=['-', '-', '34.68254655798012', '20.274189346348823,41.087269056655664', '4.167057519757221,5.795519348853619', '-0.00163615968548958,-0.0010655075656238887,-0.0005706521198656912', '21.382626233536048', '-85.55211558307522', '-124.17345905918785', '0.003172424479271551', '-', '41.128537299370436', '-2.8866078743193024', '0.20222800000000038', '0.2044769999999995', '0.20560300000000015', '0.2083656000000002', '0.20322849999999967', '0.20529829999999982', '0.2024581759903571', '0.20376865880962947', '0.20528670018951736', '0.20613424609650605', '0.20581001858872247', '0.2112179995615359', '3', '16', '0']
    data['Type']=['-', '-', 'Buy', '-', '-', '-', 'Buy', 'Sell', 'Sell', 'Sell', '-', 'Buy', 'Sell', 'Sell', 'Sell', 'Sell', 'Sell', 'Sell', 'Sell', 'Sell', 'Sell', 'Sell', 'Sell', 'Sell', 'Sell', 'Buy', 'Sell', 'neutural']
    title="BTC-USDT"
    render_mpl_table(data,title)