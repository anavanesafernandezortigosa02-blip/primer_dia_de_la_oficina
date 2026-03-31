from pathlib import Path
from flask import Flask, jsonify, render_template_string
import pandas as pd

from ejercicio_programacion_lineal import buscar_solucion_optima, recursos_consumidos

app = Flask(__name__)
DATA_DIR = Path(__file__).resolve().parent / "data"

SELECTED_FILES = [
    "battles.csv",
    "weather.csv",
    "terrain.csv",
    "commanders.csv",
    "belligerents.csv",
]


def load_csv(name):
    path = DATA_DIR / name
    return pd.read_csv(path, encoding="utf-8", low_memory=False)


def dataset_summary():
    summary = {}
    for filename in SELECTED_FILES:
        path = DATA_DIR / filename
        if not path.exists():
            continue
        df = load_csv(filename)
        summary[filename] = {
            "rows": int(df.shape[0]),
            "columns": int(df.shape[1]),
            "sample_columns": list(df.columns[:8]),
        }
    return summary


def battle_analysis(battles_df):
    df = battles_df.copy()
    df.columns = [c.strip().lower() for c in df.columns]
    return {
        "total_battles": int(df.shape[0]),
        "distinct_wars": int(df["war"].nunique()) if "war" in df else None,
        "distinct_locations": int(df["locn"].nunique()) if "locn" in df else None,
        "top_locations": df["locn"].value_counts().head(10).to_dict() if "locn" in df else {},
        "top_wars": df["war"].value_counts().head(10).to_dict() if "war" in df else {},
        "top_campaigns": df["campgn"].value_counts().head(10).to_dict() if "campgn" in df else {},
    }


def weather_analysis(weather_df):
    df = weather_df.copy()
    df.columns = [c.strip().lower() for c in df.columns]
    report = {"total_rows": int(df.shape[0])}
    for column in ["wx1", "wx2", "wx3", "wx4", "wx5"]:
        if column in df.columns:
            report[f"{column}_counts"] = df[column].value_counts().to_dict()
    return report


def terrain_analysis(terrain_df):
    df = terrain_df.copy()
    df.columns = [c.strip().lower() for c in df.columns]
    report = {"total_rows": int(df.shape[0])}
    for column in ["terrain", "terra1", "terra2", "terra3"]:
        if column in df.columns:
            report[f"{column}_counts"] = df[column].value_counts().to_dict()
    return report


def optimization_summary():
    solution, power = buscar_solucion_optima()
    espadachines, arqueros, jinetes = solution
    consumos = recursos_consumidos(espadachines, arqueros, jinetes)
    return {
        "espadachines": int(espadachines),
        "arqueros": int(arqueros),
        "jinetes": int(jinetes),
        "power": int(power),
        "resources_used": consumos,
    }


@app.route("/")
def index():
    summary = dataset_summary()
    analysis = {
        "battles": battle_analysis(load_csv("battles.csv")),
        "weather": weather_analysis(load_csv("weather.csv")),
        "terrain": terrain_analysis(load_csv("terrain.csv")),
        "optimization": optimization_summary(),
    }
    template = """
    <html>
        <head>
            <title>Análisis de datos - Primer día de la oficina</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 2rem; }
                h1, h2 { color: #2c3e50; }
                pre { background: #f4f4f4; padding: 1rem; border-radius: 8px; overflow-x: auto; }
                .card { margin-bottom: 1.5rem; padding: 1rem 1.25rem; border: 1px solid #ddd; border-radius: 10px; }
            </style>
        </head>
        <body>
            <h1>Análisis de datos del proyecto</h1>
            <div class="card">
                <h2>Resumen de archivos CSV</h2>
                <pre>{{ summary | tojson(indent=2, ensure_ascii=False) }}</pre>
            </div>
            <div class="card">
                <h2>Análisis de batallas</h2>
                <pre>{{ analysis.battles | tojson(indent=2, ensure_ascii=False) }}</pre>
            </div>
            <div class="card">
                <h2>Análisis de clima</h2>
                <pre>{{ analysis.weather | tojson(indent=2, ensure_ascii=False) }}</pre>
            </div>
            <div class="card">
                <h2>Análisis de terreno</h2>
                <pre>{{ analysis.terrain | tojson(indent=2, ensure_ascii=False) }}</pre>
            </div>
            <div class="card">
                <h2>Optimización del ejército (programación lineal)</h2>
                <pre>{{ analysis.optimization | tojson(indent=2, ensure_ascii=False) }}</pre>
            </div>
            <div class="card">
                <h2>Rutas útiles</h2>
                <ul>
                    <li><a href="/summary">/summary</a></li>
                    <li><a href="/analysis/battles">/analysis/battles</a></li>
                    <li><a href="/analysis/weather">/analysis/weather</a></li>
                    <li><a href="/analysis/terrain">/analysis/terrain</a></li>
                    <li><a href="/analysis/optimization">/analysis/optimization</a></li>
                </ul>
            </div>
        </body>
    </html>
    """
    return render_template_string(template, summary=summary, analysis=analysis)


@app.route("/summary")
def summary_route():
    return jsonify(dataset_summary())


@app.route("/analysis/battles")
def battles_route():
    return jsonify(battle_analysis(load_csv("battles.csv")))


@app.route("/analysis/weather")
def weather_route():
    return jsonify(weather_analysis(load_csv("weather.csv")))


@app.route("/analysis/terrain")
def terrain_route():
    return jsonify(terrain_analysis(load_csv("terrain.csv")))


@app.route("/analysis/optimization")
def optimization_route():
    return jsonify(optimization_summary())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
