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


@app.route('/dashboard', methods=['GET'])
def dashboard():  
    pareto = requests.get(f"{ML_URL}/pareto").json()
    rotacion = requests.get(f"{ML_URL}/rotacion").json()
    ticket_promedio = requests.get(f"{ML_URL}/ticket_promedio").json()

    return render_template(
        "dash.html",
        datapareto=pareto,
        datarotacion=rotacion,
        dataticket_promedio=ticket_promedio
    )
   
@app.route('/api/pareto', methods=['GET'])
def pareto(): 
    res = requests.get(f"{ML_URL}/pareto")
    return jsonify(res.json())


@app.route('/api/rotacion', methods=['GET'])
def rotacion(): 
    res = requests.get(f"{ML_URL}/rotacion")
    return jsonify(res.json())


@app.route('/api/ticket_promedio', methods=['GET'])
def ticket_promedio(): 
    res = requests.get(f"{ML_URL}/ticket_promedio")
    return jsonify(res.json())


app.config["TEMPLATES_AUTO_RELOAD"] = True
app.jinja_env.auto_reload = True

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)



