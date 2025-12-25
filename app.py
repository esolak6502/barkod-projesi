from flask import Flask, request
import requests

app = Flask(__name__)

# Başlangıçta kalori değerini "0" olarak tutuyoruz
last_calories = "0"

@app.route('/update', methods=['POST'])
def update():
    global last_calories
    data = request.get_json()
    barcode = data.get('value1') # IFTTT'den gelen barkod değeri
    
    # Open Food Facts API sorgusu
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    try:
        response = requests.get(url).json()
        if response.get('status') == 1:
            product = response.get('product', {})
            nutriments = product.get('nutriments', {})
            # 100g başına kalori değerini al (yoksa 0 al)
            calories = nutriments.get('energy-kcal_100g', 0)
            last_calories = str(calories)
        else:
            last_calories = "0"
    except:
        last_calories = "0" # Bağlantı hatası olursa sıfırla
        
    return "Tamam", 200

@app.route('/get_data', methods=['GET'])
def get_data():
    # Bu yeni format PictoBlox'un veriyi tanımasını sağlar
    return {"kalori": last_calories}

if __name__ == "__main__":
    app.run()
