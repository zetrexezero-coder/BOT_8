# أنشئ ملف config.py جديد أو أعد تسمية هذا الملف إلى config.py في نفس المجلد واستيراده، ثم مدد هذه الفئة.
import json
import os


def get_user_list(config, key):
    with open("{}/SaitamaRobot/{}".format(os.getcwd(), config), "r") as json_file:
        return json.load(json_file)[key]


# أنشئ ملف config.py جديد أو أعد تسمية هذا الملف إلى config.py في نفس المجلد واستيراده، ثم مدد هذه الفئة.
class Config(object):
    LOGGER = True
    # مطلوب
    # سجل الدخول إلى https://my.telegram.org وملء هذه الفتحات بالتفاصيل المعطاة منه

    API_ID = 123456  # قيمة عددية، لا تستخدم ""
    API_HASH = "awoo"
    TOKEN = "BOT_TOKEN"  # كانت هذه المتغير تسمى API_KEY لكنها الآن TOKEN، عدّل وفقاً لذلك.
    OWNER_ID = 792109647  # إذا لم تكن تعرف، شغّل البوت واكتب /id في دردشتك الخاصة معه، أيضاً عدد صحيح
    OWNER_USERNAME = "Sawada"
    SUPPORT_CHAT = "OnePunchSupport"  # مجموعة الدعم الخاصة بك، لا تضف @
    JOIN_LOGGER = (
        -1001253661229
    )  # يطبع أي مجموعة جديدة يتم إضافة البوت إليها، يطبع فقط الاسم والمعرف.
    EVENT_LOGS = (
        -1001190806654
    )  # يطبع معلومات مثل gbans وترقيات sudo وحالات تفعيل/تعطيل الذكاء الاصطناعي التي قد تساعد في تصحيح الأخطاء

    # موصى به
    SQLALCHEMY_DATABASE_URI = "something://somewhat:user@hosturl:port/databasename"  # مطلوب لأي وحدات قاعدة بيانات # أنها "URI" وليس "URL" حيث أن heroku وما شابه تقبلها فقط كـ URI
    LOAD = []
    NO_LOAD = ["rss", "cleaner", "connection", "math"]
    WEBHOOK = False
    INFOPIC = True
    URL = None
    SPAMWATCH_API = ""  # اذهب إلى support.spamwat.ch للحصول على المفتاح
    SPAMWATCH_SUPPORT_CHAT = "@SpamWatchSupport"

    # اختياري
    ##قائمة بالمعرفات - (وليس أسماء المستخدمين) للمستخدمين الذين لديهم وصول sudo للبوت.
    DRAGONS = get_user_list("elevated_users.json", "sudos")
    ##قائمة بالمعرفات - (وليس أسماء المستخدمين) للمطورين الذين سيكون لديهم نفس الأذونات مثل المالك
    DEV_USERS = get_user_list("elevated_users.json", "devs")
    ##قائمة بالمعرفات (وليس أسماء المستخدمين) للمستخدمين الذين يُسمح لهم بـ gban، لكن يمكن أيضاً حظرهم.
    DEMONS = get_user_list("elevated_users.json", "supports")
    # قائمة بالمعرفات (وليس أسماء المستخدمين) للمستخدمين الذين لن يتم حظرهم/طردهم من قبل البوت.
    TIGERS = get_user_list("elevated_users.json", "tigers")
    WOLVES = get_user_list("elevated_users.json", "whitelists")
    DONATION_LINK = None  # على سبيل المثال، paypal
    CERT_PATH = None
    PORT = 5000
    DEL_CMDS = True  # حذف الأوامر التي لا يمتلك المستخدمون إمكانية الوصول إليها، مثل حذف /ban إذا استخدمه غير مسؤول.
    STRICT_GBAN = True
    WORKERS = (
        8  # عدد الخيوط الفرعية المراد استخدامها. عيّن عدد الخيوط التي يستخدمها معالجك
    )
    BAN_STICKER = ""  # معرف ملصق بطاقة الحظر من ماري، البوت سيرسل هذا الملصق قبل حظر أو طرد مستخدم من الدردشة.
    ALLOW_EXCL = True  # السماح بأوامر ! بالإضافة إلى / (اترك هذا صحيح حتى تعمل القائمة السوداء)
    CASH_API_KEY = (
        "awoo"  # احصل على مفتاح API الخاص بك من https://www.alphavantage.co/support/#api-key
    )
    TIME_API_KEY = "awoo"  # احصل على مفتاح API الخاص بك من https://timezonedb.com/api
    WALL_API = (
        "awoo"  # للخلفيات، احصل على واحد من https://wall.alphacoders.com/api.php
    )
    AI_API_KEY = "awoo"  # للدردشة الآلية، احصل على واحد من https://coffeehouse.intellivoid.net/dashboard
    BL_CHATS = []  # قائمة بالمجموعات التي تريد إدراجها في القائمة السوداء.
    SPAMMERS = None


class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True