import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import json
from config import Conf
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        with open('resources/names.json', 'r', encoding='utf-8') as f:
            self.strings = json.load(f)
        self.setup_handlers()
    
    def main_menu_keyboard(self):
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        options = self.strings['options']
        markup.row(
            KeyboardButton(options['mali']),
            KeyboardButton(options['human_resources']),
            KeyboardButton(options['legal'])
        )
        markup.row(
            KeyboardButton(options['franchise_development']),
            KeyboardButton(options['ict']),
            KeyboardButton(options['inspection'])
        )
        markup.row(
            KeyboardButton(options['commerce']),
            KeyboardButton(options['marketing']),
            KeyboardButton(options['organizational_sales'])
        )
        markup.row(
            KeyboardButton(options['warehouse_distribution']),
            KeyboardButton(options['launch']),
            KeyboardButton(options['equipment'])
        )
        markup.row(
            KeyboardButton(options['back']),
            KeyboardButton(options['supply_chain_planning'])
        )
        return markup
    
    def setup_handlers(self):
        @self.bot.message_handler(commands=['start'])
        def send_welcome(message):
            self.bot.send_message(message.chat.id, 
                                  self.strings['welcome_message'],
                                  reply_markup=self.main_menu_keyboard())
        
        @self.bot.message_handler(func=lambda message: True)
        def handle_menu(message):
            if message.chat.type in ['group', 'supergroup']:
                # Ensure the bot is mentioned in group chats
                bot_username = f'@{self.bot.get_me().username}'
                if message.text.startswith(bot_username):
                    # Strip the bot username mention and any leading/trailing whitespace
                    text = message.text[len(bot_username):].strip()
                else:
                    return
            else:
                # For non-group chats, use the message text as is
                text = message.text

            options = self.strings['options']
            command_func = self.get_command_function(text)
            if command_func:
                command_func(message)
            else:
                self.bot.send_message(message.chat.id, 
                                      self.strings['invalid_option'], 
                                      reply_markup=self.main_menu_keyboard())

    def get_command_function(self, text):
        options = self.strings['options']
        commands = {
            options['mali']: self.mali,
            options['human_resources']: self.human_resources,
            options['legal']: self.legal,
            options['franchise_development']: self.franchise_development,
            options['ict']: self.ict,
            options['inspection']: self.inspection,
            options['commerce']: self.commerce,
            options['marketing']: self.marketing,
            options['organizational_sales']: self.organizational_sales,
            options['warehouse_distribution']: self.warehouse_distribution,
            options['launch']: self.launch,
            options['equipment']: self.equipment,
            options['supply_chain_planning']: self.supply_chain_planning,
            options['back']: self.go_back
        }
        return commands.get(text)
    
    def mali(self, message):
        self.send_selection_message(message, 'mali')

    def human_resources(self, message):
        self.send_selection_message(message, 'human_resources')

    def legal(self, message):
        self.send_selection_message(message, 'legal')

    def franchise_development(self, message):
        self.send_selection_message(message, 'franchise_development')

    def ict(self, message):
        self.send_selection_message(message, 'ict')

    def inspection(self, message):
        self.send_selection_message(message, 'inspection')

    def commerce(self, message):
        self.send_selection_message(message, 'commerce')

    def marketing(self, message):
        self.send_selection_message(message, 'marketing')

    def organizational_sales(self, message):
        self.send_selection_message(message, 'organizational_sales')

    def warehouse_distribution(self, message):
        self.send_selection_message(message, 'warehouse_distribution')

    def launch(self, message):
        self.send_selection_message(message, 'launch')

    def equipment(self, message):
        self.send_selection_message(message, 'equipment')

    def supply_chain_planning(self, message):
        self.send_selection_message(message, 'supply_chain_planning')

    def go_back(self, message):
        self.bot.send_message(message.chat.id, self.strings['back_message'], reply_markup=self.main_menu_keyboard())

    def send_selection_message(self, message, option_key):
        option = self.strings['options'][option_key]
        self.bot.send_message(message.chat.id, self.strings['selection_message'].format(option=option))

    def run(self):
        logger.info("Bot is polling...")
        self.bot.polling(none_stop=True)

if __name__ == '__main__':
    bot = TelegramBot(Conf.telegram_bot_api)
    bot.run()
