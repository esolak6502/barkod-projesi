from flask import Flask, request, jsonify
import requests
import re

app = Flask(__name__)

# Başlangıç değeri
last_calories = "0"

@app.route('/update', methods=['POST'])
def update():
    global last_calories
    try:
        data = request.get_json()
        if not data:
            return "Veri gelmedi", 400
            
        # IFTTT'den gelen barkodu al
        barcode_raw = data.get('value1', '')
        
        # Sadece rakamları tut, boşlukları ve karakterleri temizle
        barcode = re.sub(r"\D", "", str(barcode_raw))
        
        if barcode:
            url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
            response = requests.get(url, timeout=5).json()
            
            if response.get('status') == 1:
                product = response.get('product', {})
                nutriments = product.get('nutriments', {})
                # Kalori bilgisini al
                calories = nutriments.get('energy-kcal_100g', 0)
                last_calories = str(calories)
            else:
                last_calories = "Bulunamadı"
        else:
            last_calories = "Barkod Gecersiz"
            
    except Exception as e:
        print(f"Hata detayı: {e}")
        last_calories = "0"
        
    return "Tamam", 200

@app.route('/get_data', methods=['GET'])
def get_data():
    return jsonify({"kalori": last_calories})

if __name__ == "__main__":
    import os
    # Deploy ortamları için dinamik port ayarı
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
