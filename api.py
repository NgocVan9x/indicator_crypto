from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
from datetime import datetime
from pytz import timezone
from common import getDataAndSendBot, getChatId

app = FlaskAPI(__name__)


@app.route("/bot", methods=['POST'])
def sendToBot():
    if request.method == 'POST':
        try:
            symbol = str(request.data.get('symbol'))
            interval = str(request.data.get('interval'))
            market = str(request.data.get('market'))
            chat_ids = getChatId()
            fileName = "data_suppy_demand.png"
            getDataAndSendBot("From Supply demand", fileName,
                              chat_ids, symbol, interval, market)
            return '', status.HTTP_200_OK
        except Exception as e:
            print(e)
            return '', status.HTTP_302_FOUND


if __name__ == "__main__":
    app.run(debug=True)
