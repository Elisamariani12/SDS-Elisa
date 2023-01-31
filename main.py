from flask import Flask, request, make_response, jsonify
from DialogControl import DialogControl
import pandas as pd

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    events_data_df=pd.read_csv('database.csv',sep=";")
    req = request.get_json(force=True)
    dialog_control = DialogControl()
    dialog_control.handleRequest(events_data_df)
    response = dialog_control.getResponse()
    return make_response(jsonify(response))


if __name__ == '__main__':
    app.run()
