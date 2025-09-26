from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
import os

app = Flask(__name__, static_folder="static", template_folder="templates")


# โหลดโมเดล
model = joblib.load("survival_model.pkl")

@app.route("/")
def home():
    return render_template("safepath.html")  # แสดงหน้าเว็บหลัก

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    
    features = np.array([[
        data["GCS"], data["RTS"], data["ISS"], data["Ais3"], data["RR"],
        data["Ais2"], data["Ais6"], data["Risk5"], data["Ais4"], data["Ais1"],
        data["Ais5"], data["AGE"], data["Risk1"], data["Risk4"], data["PR"],
        data["SBP"], data["Time"], data["SEX"], data["Injp"]
    ]])

    prob = model.predict_proba(features)[0][1]
    pred = model.predict(features)[0]

    return jsonify({
        "prediction": int(pred),
        "survivalProb": round(prob*100, 2)
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
