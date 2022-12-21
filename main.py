from flask import Flask, render_template
import pandas as pd
from pathlib import Path

app = Flask(__name__)


@app.route("/")
@app.route("/home/")
def home():
    return render_template("home.html")


@app.route("/api/v1/<station>/<date>")
def about(station, date):
    try:
        DATA_DIR = "data_small"
        filename = f"TG_STAID{station:>06s}.txt"
        csv_path = Path(DATA_DIR, filename)
        df = pd.read_csv(str(csv_path), skiprows=20)
        df.columns = df.columns.str.strip()
        # temperature = 23
        temperature = df.loc[df.DATE == int(date)].TG.squeeze() / 10
        return {
            "station": station,
            "date": date,
            "temperature": str(temperature)
        }
    except FileNotFoundError as e:
        return {
            "error": f"station {station} does not exist"
        }

if __name__ == '__main__':
    app.run(debug=True)
