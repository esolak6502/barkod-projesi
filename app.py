@app.route('/update', methods=['POST'])
def update():
    global last_calories
    data = request.get_json()
    barcode = data.get('value1') # IFTTT'den gelen ham barkod değeri
    
    # --- YENİ EKLENEN KISIM BAŞLANGICI ---
    if barcode:
        # Önce boşlukları siler, sonra başındaki ve sonundaki gizli boşlukları temizler
        barcode = str(barcode).replace(" ", "").strip() 
    # --- YENİ EKLENEN KISIM BİTİŞİ ---
    
    # Open Food Facts API sorgusu
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    try:
        response = requests.get(url).json()
        if response.get('status') == 1:
            product = response.get('product', {})
            nutriments = product.get('nutriments', {})
            # 100g başına kalori değerini al
            calories = nutriments.get('energy-kcal_100g', 0)
            last_calories = str(calories)
        else:
            last_calories = "Bulunamadı" # 0 yerine "Bulunamadı" demek daha iyi olabilir
    except:
        last_calories = "Bağlantı Hatası" 
        
    return "Tamam", 200
