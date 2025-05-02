from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd

app = Flask(__name__)
CORS(app)

model = joblib.load('model/XGBoostRNModel.joblib')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json

        required_fields = [
            'classf',
            'vlr_renda_media_fam',
            'cod_local_domic_fam',
            'qtd_comodos_domic_fam',
            'qtd_comodos_dormitorio_fam',
            'cod_material_piso_fam',
            'cod_material_domic_fam',
            'cod_agua_canalizada_fam',
            'cod_abaste_agua_domic_fam',
            'cod_banheiro_domic_fam',
            'cod_destino_lixo_domic_fam',
            'cod_iluminacao_domic_fam',
            'cod_calcamento_domic_fam',
            'ind_familia_quilombola_fam',
            'qtde_pessoas'
        ]

        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"error": f"Campos ausentes: {', '.join(missing_fields)}"}), 400

        try:
            features = [
                int(data['classf']),
                float(data['vlr_renda_media_fam']),
                int(data['cod_local_domic_fam']),
                int(data['qtd_comodos_domic_fam']),
                int(data['qtd_comodos_dormitorio_fam']),
                int(data['cod_material_piso_fam']),
                int(data['cod_material_domic_fam']),
                int(data['cod_agua_canalizada_fam']),
                int(data['cod_abaste_agua_domic_fam']),
                int(data['cod_banheiro_domic_fam']),
                int(data['cod_destino_lixo_domic_fam']),
                int(data['cod_iluminacao_domic_fam']),
                int(data['cod_calcamento_domic_fam']),
                int(data['ind_familia_quilombola_fam']),
                int(data['qtde_pessoas']),
            ]
        except (ValueError, TypeError):
            return jsonify({"error": "Erro ao converter tipos. Verifique se todos os campos têm valores numéricos válidos."}), 400

        input_df = pd.DataFrame([features], columns=required_fields)

        prediction = model.predict(input_df)[0]
        confidence_score = max(model.predict_proba(input_df)[0])

        return jsonify({
            "prediction_result": int(prediction),
            "confidence_score": round(float(confidence_score), 4)
        }), 200


    except Exception as e:
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
