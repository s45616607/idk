import telebot
from telebot.types import (
    Message,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    PreCheckoutQuery,
    LabeledPrice,
    )
from telebot.util import escape, user_link
from urllib.parse import quote, unquote
from configs import cfg
from database import *
from data import *


bot = telebot.TeleBot(cfg.BOT_TOKEN, parse_mode="HTML")


#
admin_id = cfg.admin_id

@bot.message_handler(commands=["start"], chat_types=["private"])
def start_main(message: Message):
    if already_ban(message.from_user.id):
        return bot.reply_to(message, lang_msg(message, "banned"))
    user_id = message.from_user.id
    bot.reply_to(message , text=lang_msg(message, "start_menu"), reply_markup=lang_buttons(message, "button_start"), disable_web_page_preview=True)
    is_new_user = not user_exists(user_id)
    args = message.text.strip().split(" ")
    referrer_id = int(args[1]) if len(args) == 2 and args[1].isdigit() else None
    if referrer_id and referrer_id != user_id and is_new_user:
        register_referral(user_id, str(referrer_id))
    if is_new_user:
        save_user(username=message.from_user.username, user_id=user_id)
        notify_text = (
            f"<b><blockquote>- مستخدم جديد في البوت :</blockquote>\n\n"
            f"- حسابه : {user_link(message.from_user)}\n"
            f"- ايديه : <code>{message.from_user.id}</code>\n"
            f"- يوزره : @{message.from_user.username}\n\n"
            f"عدد المستخدمين الكلي: {total_users()}</b>"
        )
        bot.send_message(admin_id, notify_text, parse_mode='HTML')
    delete(user_id, None, 'database/users.json')
    return




@bot.message_handler(commands=["help"], chat_types=["private"])
def help_main(message: Message):


    pass


@bot.message_handler(commands=["store"], chat_types=["private"])
def store_main(message: Message):

    pass


@bot.message_handler(commands=["store"], chat_types=["private"])
def myself_main(message: Message):

    pass


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call: CallbackQuery):
    data = call.data
    user_id = call.from_user.id

    pass



@bot.inline_handler(lambda query: True)
def inline_invoice(query):

    pass






if __name__ == "__main__":
    bot.infinity_polling(skip_pending=True)

