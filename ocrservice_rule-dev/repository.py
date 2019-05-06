import pymongo
import uuid
import datetime
from bson.objectid import ObjectId


def get_db_manager():
    return pymongo.MongoClient("mongodb://localhost:27017")["app_rules"]
    
def insert(app):
    now = datetime.datetime.now()
    now = now.strftime("%d/%m/%Y")
    db = get_db_manager()
    apps = db["apps"]
    row = {}
    row["app_id"] = str(uuid.uuid4())
    row["created date"] = now
    for key in app:
        row[key] = app[key]
    apps.insert_one(row)

def show_all():
    db = get_db_manager()
    apps = db["apps"]
    for row in apps.find():
        print(row)

def remove_app(app_id):
    pass

def init_apps():
    app1 = {"name": "Giấy đăng kiểm", 
        "features": ["Biển đăng ký", "Loại phương tiện: (Type)", "Nhãn hiệu: (Mark)",
                "Số loại: (Model code)", "Số máy: (Engine Number)", "Số khung: (Chassis Number)",
                "Năm, nước sản xuất", "Số quản lý", "Niên hạn SD", "Số người cho phép chở"],
        "type_id": "0"
        }

    app2 = {"name": "Đăng ký xe", 
            "features": ["Họ tên/Full name", "Ngày sinh/Date of birth", "Quốc tịch/Nationality",
                    "Hạng/Class", "Nơi cư trú/Address"],
            "type_id": "0"
            }

    app3 = {"name": "Giấy đăng ký xe", 
            "features": ["Tên chủ xe (Owner's full name):", "Số máy (Engine N*):", "Địa chỉ (Address):",
                    "Số khung (Chassis N*):", "Số loại (Model Code):", "Dung tích (Capacity):",
                    "Nhãn hiệu (Brand):", "Loại xe (Type):", "Màu sơn (Color):"],
            "conf_val": 0.7,
            "rules": ["split_rule", "bot_rule"],
            "type_id": "0"
            }

    remove_all()

    insert(app1)
    insert(app2)
    insert(app3)

def get_general_apps():
    db = get_db_manager()
    return list(db["apps"].find({"type_id": "0"}))

def get_user_apps():
    db = get_db_manager()
    res = db["apps"].find({"type_id": "1"})
    if res == None:
        return []
    return list(res)
def remove_all():
    db = get_db_manager()
    apps = db["apps"]
    apps.delete_many({})

def get_app(app_id):
    db = get_db_manager()
    app = db["apps"].find_one({"app_id": app_id})
    return app

def add_app(app):
    db = get_db_manager()
    now = datetime.datetime.now()
    now = now.strftime("%d/%m/%Y")
    app_db = db["apps"]
    app["created date"] = now
    app["app_id"] = str(uuid.uuid4())
    app["type_id"] = "1"
    app_db.insert_one(app)

