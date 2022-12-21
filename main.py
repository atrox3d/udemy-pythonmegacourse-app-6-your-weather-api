from flask import Flask, render_template
import pandas as pd
from pathlib import Path

app = Flask(__name__)

DATA_DIR = "data_small"
stations_file = "stations.txt"
stations_path = Path(DATA_DIR, stations_file)
stations = pd.read_csv(str(stations_path), skiprows=17)
stations.columns = stations.columns.str.strip()
stations = stations[["STAID", "STANAME"]]

@app.route("/")
@app.route("/home/")
def home():
    print(stations.columns)
    return render_template("home.html", data=stations.to_html(index=False))


@app.route("/api/v1/<station>/<date>")
def about(station, date):
    try:
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
