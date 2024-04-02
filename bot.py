import telebot
import requests
import json
from telebot import types
from config import TOKEN, USERID, SLASH_TOKEN

bot = telebot.TeleBot(TOKEN)


class IsAdmin(telebot.custom_filters.SimpleCustomFilter):
    key = 'is_admin'

    @staticmethod
    def check(message: telebot.types.Message):
        return bot.get_chat_member(message.chat.id, message.from_user.id).user.id == USERID


class Link():
    def __init__(self, id, url, name, title, visibility, tags):
        self.id = id
        self.url = url
        self.name = name
        self.title = title
        self.visibility = visibility if visibility is not None else 'PRIVATE'
        self.tags = tags


@bot.message_handler(is_admin=True, commands=['admin'])
def admin_rep(message):
    bot.send_message(message.chat.id, 'Admin')


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    help = "Hello! I am a bot that can help you with your daily tasks. Here are some commands you can use:\n\n"
    help += "/start - Start the bot\n"
    help += "/help - Get help\n"
    help += "[website] [name] #tags - Save a link with a name\n"
    # help += "/clear - Delete all saved messages\n"
    bot.reply_to(message, help)


@bot.callback_query_handler(func=lambda call: True)
def handle_button_click(call):
    message = call.message
    # print(message)
    if call.data == 'PUBLIC':
        link_name = message.text.split()[6]
        link_id = message.text.split()[8]
        edit_link_visibility(link_id, 'PUBLIC')
        bot.edit_message_text(text="Link saved as %s with name %s, id %s" %
                              ('PUBLIC', link_name, link_id), chat_id=message.chat.id, message_id=message.message_id, reply_markup=message.reply_markup)
    elif call.data == 'PRIVATE':
        link_name = message.text.split()[6]
        link_id = message.text.split()[8]
        edit_link_visibility(link_id, 'PRIVATE')
        bot.edit_message_text(text="Link saved as %s with name %s, id %s" %
                              ('PRIVATE', link_name, link_id), chat_id=message.chat.id, message_id=message.message_id, reply_markup=message.reply_markup)
    elif call.data == 'PROTECTED':
        link_name = message.text.split()[6]
        link_id = message.text.split()[8]
        edit_link_visibility(link_id, 'PROTECTED')
        bot.edit_message_text(text="Link saved as %s with name %s, id %s" %
                              ('PROTECTED', link_name, link_id), chat_id=message.chat.id, message_id=message.message_id, reply_markup=message.reply_markup)


@bot.message_handler(is_admin=True, regexp='https?://[\\w.-]+[/\\w+]?')
# @bot.message_handler(func=lambda message: True)
def save_url(message):
    # print(message.text)
    key_words = message.text.split()
    url = key_words[0]
    if len(key_words) == 1:
        bot.reply_to(message, "Please provide a name for the link")
        return
    name = key_words[1]
    # Determine if the message has tags
    if message.text.find('#') == -1:
        tags = None
    else:
        tags = message.text.split('#')[1:]
        tags = [tag.strip() for tag in tags]
    # Default visibility is PRIVATE
    link = Link(None, url, name, None, None, tags)
    # Print link all the details
    link_id = push_url_to_slash(link)
    if link_id.find('err') != -1:
        bot.reply_to(message, link_id)
        return
    link.id = link_id

    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton(
        text='PUBLIC', callback_data='PUBLIC')
    itembtn2 = types.InlineKeyboardButton(
        text='PRIVATE', callback_data='PRIVATE')
    itembtm3 = types.InlineKeyboardButton(
        text='PROTECTED', callback_data='PROTECTED')
    markup.add(itembtn1, itembtn2, itembtm3)

    bot.reply_to(message, "Link saved as %s with name %s, id %s" %
                     (link.visibility, link.name, link.id), reply_markup=markup)


def push_url_to_slash(link: Link) -> str:
    url = "https://slash.fooo.in/api/v1/shortcuts"

    if link.url is None or link.url == '':
        return 'err: URL is required'
    if link.name is None or link.name == '':
        return 'err: name is required'
    # print(link.tags)
    payload = json.dumps({
        "link": link.url,
        "name": link.name,
        "tags": link.tags if link.tags is not None else [],
        "title": link.title if link.title is not None else "",
        "visibility": link.visibility if link.visibility is not None else "PRIVATE"
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer' + SLASH_TOKEN
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    # print(response.json())
    if response.status_code != 200:
        return 'err:' + response.json()['message']
    return str(response.json()['shortcut']['id'])


def edit_link_visibility(link_id, visibility):
    url = "https://slash.fooo.in/api/v1/shortcuts/%s?updateMask=visibility" % link_id

    payload = json.dumps({
        "visibility": visibility
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer' + SLASH_TOKEN
    }

    response = requests.request("PUT", url, headers=headers, data=payload)

    if response.status_code != 200:
        return None
    return response.json()['shortcut']['visibility']


bot.add_custom_filter(IsAdmin())
bot.infinity_polling()
