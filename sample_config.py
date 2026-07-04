# أنشئ ملف config.py وأضف البيانات التالية
import json
import os


def get_user_list(config, key):
    with open("{}/SaitamaRobot/{}".format(os.getcwd(), config), "r") as json_file:
        return json.load(json_file)[key]


class Config(object):
    """إعدادات البوت"""
    LOGGER = True
    
    # البيانات المطلوبة من Telegram
    API_ID = 123456  # من https://my.telegram.org
    API_HASH = "awoo"
    TOKEN = "BOT_TOKEN"  # توكن البوت من BotFather
    OWNER_ID = 792109647  # معرفك على Telegram (اكتب !معرفي بالخاص للحصول عليه)
    OWNER_USERNAME = "اسمك"
    
    # إعدادات الدعم والسجلات
    SUPPORT_CHAT = "OnePunchSupport"
    JOIN_LOGGER = -1001253661229
    EVENT_LOGS = -1001190806654

    # إعدادات قاعدة البيانات
    SQLALCHEMY_DATABASE_URI = "postgresql://user:password@localhost:5432/db_name"
    
    # إعدادات التحميل
    LOAD = []
    NO_LOAD = ["rss", "cleaner", "connection", "math"]
    WEBHOOK = False
    INFOPIC = True
    URL = None
    
    # إعدادات SpamWatch
    SPAMWATCH_API = ""
    SPAMWATCH_SUPPORT_CHAT = "@SpamWatchSupport"

    # المستخدمون المتقدمون
    DRAGONS = get_user_list("elevated_users.json", "sudos")
    DEV_USERS = get_user_list("elevated_users.json", "devs")
    DEMONS = get_user_list("elevated_users.json", "supports")
    TIGERS = get_user_list("elevated_users.json", "tigers")
    WOLVES = get_user_list("elevated_users.json", "whitelists")
    
    # إعدادات إضافية
    DONATION_LINK = None
    CERT_PATH = None
    PORT = 5000
    DEL_CMDS = True
    STRICT_GBAN = True
    WORKERS = 8
    BAN_STICKER = ""
    ALLOW_EXCL = True  # السماح باستخدام ! بدلاً من /
    
    # مفاتيح API
    CASH_API_KEY = "awoo"
    TIME_API_KEY = "awoo"
    WALL_API = "awoo"
    AI_API_KEY = "awoo"
    BL_CHATS = []
    SPAMMERS = None


class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
