import importlib
import time
import re
from sys import argv
from typing import Optional

from SaitamaRobot import (
    ALLOW_EXCL,
    CERT_PATH,
    DONATION_LINK,
    LOGGER,
    OWNER_ID,
    PORT,
    TOKEN,
    URL,
    WEBHOOK,
    SUPPORT_CHAT,
    dispatcher,
    StartTime,
    telethn,
    updater)

from SaitamaRobot.modules import ALL_MODULES
from SaitamaRobot.modules.helper_funcs.chat_status import is_user_admin
from SaitamaRobot.modules.helper_funcs.misc import paginate_modules
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.error import (
    BadRequest,
    ChatMigrated,
    NetworkError,
    TelegramError,
    TimedOut,
    Unauthorized,
)
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
)
from telegram.ext.dispatcher import DispatcherHandlerStop, run_async
from telegram.utils.helpers import escape_markdown


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["ث", "د", "س", "أيام"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time


PM_START_TEXT = """
هلا {}، أنا {}!
أنا بوت لإدارة القروبات بطابع الأنمي.
صُنعت من محبي الأنمي لمحبي الأنمي!
"""

HELP_STRINGS = """
هلا! اسمي *{}*.
أنا بوت قوي لإدارة القروبات! شاهد ما يلي لتتعرف على الأشياء التي يمكنني مساعدتك بها.

الأوامر *الرئيسية* المتوفرة:
 • !مساعدة: يرسل لك هذه الرسالة
 • !مساعدة <اسم القسم>: معلومات عن قسم معين
 • !تبرع: معلومات التبرع
 • !إعدادات: إعداداتك وإعدادات القروب

{}
المزيد من الخيارات متاحة!
""".format(
    dispatcher.bot.first_name,
    "\nجميع الأوامر تعمل بـ ! أو /\n" if not ALLOW_EXCL else "",
)

SAITAMA_IMG = "https://telegra.ph/file/46e6d9dfcb3eb9eae95d9.jpg"

DONATE_STRING = """شكراً على رغبتك في التبرع!
يمكنك دعم المشروع عبر [Paypal](ko-fi.com/sawada)
الدعم لا يكون مادياً فقط، بل يمكنك المساهمة في تطوير البوت!"""

IMPORTED = {}
MIGRATEABLE = []
HELPABLE = {}
STATS = []
USER_INFO = []
DATA_IMPORT = []
DATA_EXPORT = []
CHAT_SETTINGS = {}
USER_SETTINGS = {}

for module_name in ALL_MODULES:
    imported_module = importlib.import_module("SaitamaRobot.modules." + module_name)
    if not hasattr(imported_module, "__mod_name__"):
        imported_module.__mod_name__ = imported_module.__name__

    if imported_module.__mod_name__.lower() not in IMPORTED:
        IMPORTED[imported_module.__mod_name__.lower()] = imported_module
    else:
        raise Exception("لا يمكن أن يكون هناك قسمان بنفس الاسم!")

    if hasattr(imported_module, "__help__") and imported_module.__help__:
        HELPABLE[imported_module.__mod_name__.lower()] = imported_module

    if hasattr(imported_module, "__migrate__"):
        MIGRATEABLE.append(imported_module)

    if hasattr(imported_module, "__stats__"):
        STATS.append(imported_module)

    if hasattr(imported_module, "__user_info__"):
        USER_INFO.append(imported_module)

    if hasattr(imported_module, "__import_data__"):
        DATA_IMPORT.append(imported_module)

    if hasattr(imported_module, "__export_data__"):
        DATA_EXPORT.append(imported_module)

    if hasattr(imported_module, "__chat_settings__"):
        CHAT_SETTINGS[imported_module.__mod_name__.lower()] = imported_module

    if hasattr(imported_module, "__user_settings__"):
        USER_SETTINGS[imported_module.__mod_name__.lower()] = imported_module


def send_help(chat_id, text, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "مساعدة"))
    dispatcher.bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
        reply_markup=keyboard,
    )


@run_async
def start(update: Update, context: CallbackContext):
    args = context.args
    uptime = get_readable_time((time.time() - StartTime))
    if update.effective_chat.type == "private":
        if len(args) >= 1:
            if args[0].lower() == "مساعدة":
                send_help(update.effective_chat.id, HELP_STRINGS)
            elif args[0].lower().startswith("مساعدة_"):
                mod = args[0].lower().split("_", 1)[1]
                if not HELPABLE.get(mod, False):
                    return
                send_help(
                    update.effective_chat.id,
                    HELPABLE[mod].__help__,
                    InlineKeyboardMarkup(
                        [[InlineKeyboardButton(text="رجوع", callback_data="رجوع_مساعدة")]],
                    ),
                )
        else:
            first_name = update.effective_user.first_name
            update.effective_message.reply_photo(
                SAITAMA_IMG,
                PM_START_TEXT.format(
                    escape_markdown(first_name), escape_markdown(context.bot.first_name),
                ),
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="☑️ أضفني",
                                url="t.me/{}?startgroup=true".format(
                                    context.bot.username,
                                ),
                            ),
                        ],
                        [
                            InlineKeyboardButton(
                                text="🚑 الدعم",
                                url=f"https://t.me/{SUPPORT_CHAT}",
                            ),
                            InlineKeyboardButton(
                                text="🔔 التحديثات",
                                url="https://t.me/OnePunchUpdates",
                            ),
                        ],
                        [
                            InlineKeyboardButton(
                                text="🗄 الكود المصدري",
                                url="https://github.com/AnimeKaizoku/SaitamaRobot",
                            ),
                        ],
                    ],
                ),
            )
    else:
        update.effective_message.reply_text(
            "أنا مستيقظ! ✨\n<b>مدة التشغيل:</b> <code>{}</code>".format(uptime),
            parse_mode=ParseMode.HTML,
        )


def error_callback(update: Update, context: CallbackContext):
    error = context.error
    try:
        raise error
    except Unauthorized:
        LOGGER.error("خطأ في المصادقة")
    except BadRequest:
        LOGGER.error("طلب خاطئ: %s", str(error))
    except TimedOut:
        LOGGER.error("انتهت مهلة الانتظار")
    except NetworkError:
        LOGGER.error("خطأ في الاتصال")
    except ChatMigrated as err:
        LOGGER.error("تم الهجرة: %s", str(err))
    except TelegramError:
        LOGGER.error("خطأ تيليجرام: %s", str(error))


@run_async
def help_button(update, context):
    query = update.callback_query
    mod_match = re.match(r"مساعدة_وحدة\((.+?)\)", query.data)
    back_match = re.match(r"رجوع_مساعدة", query.data)

    try:
        if mod_match:
            module = mod_match.group(1)
            text = "هذه هي المساعدة لـ *{}*:\n".format(
                HELPABLE[module].__mod_name__,
            ) + HELPABLE[module].__help__
            query.message.edit_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="رجوع", callback_data="رجوع_مساعدة")]],
                ),
            )
        elif back_match:
            query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, HELPABLE, "مساعدة"),
                ),
            )

        context.bot.answer_callback_query(query.id)

    except BadRequest:
        pass


@run_async
def get_help(update: Update, context: CallbackContext):
    chat = update.effective_chat
    args = update.effective_message.text.split(None, 1)

    if chat.type != chat.PRIVATE:
        if len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
            module = args[1].lower()
            update.effective_message.reply_text(
                f"اكتب !مساعدة بالخاص للمزيد عن {module}",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="المساعدة",
                                url="t.me/{}?start=مساعدة_{}".format(
                                    context.bot.username, module,
                                ),
                            ),
                        ],
                    ],
                ),
            )
            return
        update.effective_message.reply_text(
            "اكتب !مساعدة بالخاص للحصول على المزيد",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="المساعدة",
                            url="t.me/{}?start=مساعدة".format(context.bot.username),
                        ),
                    ],
                ],
            ),
        )
        return

    elif len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
        module = args[1].lower()
        text = "المساعدة لـ *{}*:\n".format(
            HELPABLE[module].__mod_name__,
        ) + HELPABLE[module].__help__
        send_help(
            chat.id,
            text,
            InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="رجوع", callback_data="رجوع_مساعدة")]],
            ),
        )
    else:
        send_help(chat.id, HELP_STRINGS)


@run_async
def donate(update: Update, context: CallbackContext):
    chat = update.effective_chat
    if chat.type == "private":
        update.effective_message.reply_text(
            DONATE_STRING, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True,
        )
    else:
        update.effective_message.reply_text(
            "شكراً على اهتمامك! 💝",
        )


def migrate_chats(update: Update, context: CallbackContext):
    msg = update.effective_message
    if msg.migrate_to_chat_id:
        old_chat = update.effective_chat.id
        new_chat = msg.migrate_to_chat_id
    elif msg.migrate_from_chat_id:
        old_chat = msg.migrate_from_chat_id
        new_chat = update.effective_chat.id
    else:
        return

    LOGGER.info("الانتقال من %s إلى %s", str(old_chat), str(new_chat))
    for mod in MIGRATEABLE:
        mod.__migrate__(old_chat, new_chat)

    LOGGER.info("تم الانتقال بنجاح!")
    raise DispatcherHandlerStop


def main():

    if SUPPORT_CHAT is not None and isinstance(SUPPORT_CHAT, str):
        try:
            dispatcher.bot.sendMessage(f"@{SUPPORT_CHAT}", "البوت متصل الآن! ✨")
        except Unauthorized:
            LOGGER.warning("البوت لا يستطيع إرسال رسالة لقروب الدعم!")
        except BadRequest as e:
            LOGGER.warning(e.message)

    start_handler = CommandHandler(["ابدأ", "start"], start)
    help_handler = CommandHandler(["مساعدة", "help"], get_help)
    help_callback_handler = CallbackQueryHandler(help_button, pattern=r"مساعدة.*")
    donate_handler = CommandHandler(["تبرع", "donate"], donate)
    migrate_handler = MessageHandler(Filters.status_update.migrate, migrate_chats)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(donate_handler)
    dispatcher.add_handler(help_callback_handler)
    dispatcher.add_handler(migrate_handler)
    dispatcher.add_error_handler(error_callback)

    if WEBHOOK:
        LOGGER.info("يتم استخدام webhooks")
        updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
        if CERT_PATH:
            updater.bot.set_webhook(url=URL + TOKEN, certificate=open(CERT_PATH, "rb"))
        else:
            updater.bot.set_webhook(url=URL + TOKEN)
    else:
        LOGGER.info("يتم استخدام long polling")
        updater.start_polling(timeout=15, read_latency=4, clean=True)

    if len(argv) not in (1, 3, 4):
        telethn.disconnect()
    else:
        telethn.run_until_disconnected()

    updater.idle()


if __name__ == "__main__":
    LOGGER.info("تم تحميل الأقسام بنجاح: " + str(ALL_MODULES))
    telethn.start(bot_token=TOKEN)
    main()
