from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Barkod verisini tutacak değişken
last_barcode_data = {"status": "Veri bekleniyor...", "calories": 0}

@app.route('/update', methods=['POST'])
def update():
    global last_barcode_data
    data = request.get_json()
    barcode = data.get('value1') # IFTTT'den gelen barkod
    
    # Open Food Facts API sorgusu
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    response = requests.get(url).json()
    
    if response.get('status') == 1:
        product = response.get('product', {})
        nutriments = product.get('nutriments', {})
        calories = nutriments.get('energy-kcal_100g', 0)
        name = product.get('product_name', 'Bilinmeyen Ürün')
        last_barcode_data = {"status": name, "calories": calories}
    else:
        last_barcode_data = {"status": "Ürün Bulunamadı", "calories": 0}
        
    return "Tamam", 200

@app.route('/get_data', methods=['GET'])
def get_data():
    return jsonify(last_barcode_data)

if __name__ == "__main__":
    app.run()
