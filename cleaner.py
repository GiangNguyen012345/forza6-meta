import json
import re

def clean_database():
    input_file = "db.json"
    output_file = "db_sach_se.json"
    
    print(f"🧹 Đang nạp dữ liệu từ {input_file} để dọn rác...")
    
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Không tìm thấy file {input_file}. Hãy đảm bảo nó nằm cùng thư mục với code.")
        return

    clean_data = {}
    
    # Danh sách các từ khóa "xe giả" bị cào nhầm từ Fandom Wiki
    junk_car_keywords = ["COST:", "ASPIRATION", "MAXIMUM", "MINIMUM", "TORQUE", "POWER"]
    
    cars_cleaned = 0
    cars_deleted = 0

    for car_name, classes in raw_data.items():
        # 1. Xóa sổ các "xe giả"
        if any(kw in car_name.upper() for kw in junk_car_keywords):
            cars_deleted += 1
            continue
            
        clean_data[car_name] = {}
        
        for class_name, content in classes.items():
            # Nếu là list động cơ từ Wiki, giữ nguyên vì nó đã sạch sẵn
            if class_name == "ENGINE_SWAPS_AVAILABLE":
                clean_data[car_name][class_name] = content
                continue
            
            # 2. Thuật toán Cắt rác: Chỉ lấy nội dung từ chữ "Conversion |" đến "Notes |"
            start_match = re.search(r'(Conversion\s*\||Engine Swap:)', content)
            end_match = re.search(r'(\|\s*Notes\s*\||\|\s*More by this author\s*\||\|\s*Quick Comment\s*\|)', content)
            
            if start_match and end_match:
                start_idx = start_match.start()
                end_idx = end_match.start()
                
                # Rút trích phần ruột tinh khiết
                useful_text = content[start_idx:end_idx].strip()
                
                # Dọn dẹp khoảng trắng thừa cho đẹp mắt
                useful_text = re.sub(r'\s*\|\s*', ' | ', useful_text)
                
                clean_data[car_name][class_name] = useful_text
            else:
                # Trường hợp ngoại lệ không theo cấu trúc, giữ lại tạm
                clean_data[car_name][class_name] = "Data bị lỗi định dạng web. Khuyên dùng: Giữ máy Zin hoặc Swap Racing V8."
                
        cars_cleaned += 1

    # Xuất ra file mới
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(clean_data, f, indent=2, ensure_ascii=False)
        
    print("=========================================================")
    print(f"✅ ĐÃ DỌN RÁC THÀNH CÔNG!")
    print(f"🗑️ Đã xóa bỏ {cars_deleted} thẻ dữ liệu lỗi (Cost, Power...).")
    print(f"✨ Đã làm sạch thông số Tune cho {cars_cleaned} chiếc xe.")
    print(f"📦 Dữ liệu sạch đã được lưu vào file: '{output_file}'")
    print("=========================================================")
    print("👉 Hãy mở file db_sach_se.json lên, copy toàn bộ chữ bên trong và cập nhật lên GitHub của bạn!")

if __name__ == "__main__":
    clean_database()
