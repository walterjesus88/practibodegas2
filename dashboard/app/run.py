from flask import Flask, render_template, jsonify
import os
import requests

app = Flask(__name__)

ML_URL = os.getenv('MLSERVICE_URL', 'http://mlservice:8001')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/apriori_run')
def apriori_run():
    r = requests.post(f"{ML_URL}/apriori/run", json={"min_support":0.02, "min_confidence":0.3})
    return jsonify(r.json())

@app.route('/api/correlacion')
def correlacion():
    r = requests.get(f"{ML_URL}/correlacion")
    print('estoy en correlaciondddddddddddddddddddd')
    response = r.json()
    
    print("📌 JSON recibido:", response)

    if "categories" not in response or "matrix" not in response:
        return "Error: JSON incompleto", 500
    
    if len(response["matrix"]) != len(response["categories"]):
        raise ValueError("Matrix debe ser cuadrada con tamaño igual a categories")

    # categorias = [
    #     "Chocolates y Galletas",
    #     "Cafés y Bebidas",
    #     "Fórmulas Infantiles",
    #     "Mascotas",
    #     "Cocina y Repostería",
    #     "Leches Vegetales",
    #   ]

    # matrix = [
    #     [0, 0.36, 0.22, 0.15, 0.05, 0.12],
    #     [0.36, 0, 0.42, 0.09, 0.15, 0.25],
    #     [0.22, 0.42, 0, 0.1, 0.35, 0.19],
    #     [0.15, 0.09, 0.1, 0, 0.14, 0.12],
    #     [0.05, 0.15, 0.35, 0.14, 0, 0.31],
    #     [0.12, 0.25, 0.19, 0.12, 0.31, 0],
    #   ]

    print('passooooooo')

    return render_template(
        'correlaciones.html',
        data=response["matrix"],
        categorias=response["categories"]
    )


#{'matrix': [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]], 'categories': ['Alimento húmedo Cat ','dog chow']}
#FASTAPI_URL = "http://mlservice:8001"

@app.route("/apriori")
def apriori_runs():
    print({'adafafffsf'})
    res = requests.get(f"{ML_URL}/apriori/runs")
    runs = res.json()
    return render_template("apriori_runs.html", runs=runs)


@app.route("/apriori/<int:run_id>")
def apriori_rules(run_id):
    res = requests.get(f"{ML_URL}/apriori/runs/{run_id}/rules")
    rules = res.json()
    return render_template("apriori_rules.html", rules=rules)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)



