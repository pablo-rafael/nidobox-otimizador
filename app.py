from flask import Flask, render_template, request, jsonify
from otimizador import calcular_otimizacao

app = Flask(__name__)

# Rota para renderizar a página principal (HTML)
@app.route('/')
def index():
    return render_template('index.html')

# Rota da API que recebe os dados do formulário e devolve o cálculo
@app.route('/otimizar', methods=['POST'])
def otimizar():
    dados = request.get_json()
    
    orcamento = dados.get('orcamento', 0)
    teto_pct = dados.get('teto_pct', 100)
    canais = dados.get('canais', [])
    
    try:
        resultado = calcular_otimizacao(orcamento, teto_pct, canais)
        return jsonify({"sucesso": True, "dados": resultado})
    except Exception as e:
        return jsonify({"sucesso": False, "erro": str(e)})

if __name__ == '__main__':
    # Configuração para rodar no servidor em nuvem
    app.run(host='0.0.0.0', port=5000, debug=True)