import os
from os.path import join, dirname
from dotenv import load_dotenv
import openai
import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Load your API key from an environment variable or secret management service
openai.api_key = os.getenv("APIKEY")
myTelegramId = os.environ.get("myTelegramId")
telegramBotApiKey = os.environ.get("TELEGRAMBOTAPIKEY")

def queryOpenAi(msg):
    print(msg)
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=str(msg),
    temperature=0.9,
    max_tokens=4000,
    top_p=1,
    frequency_penalty=0.0,
    presence_penalty=0.6,
    )
    print(response.choices[0].text)
    return response.choices[0].text


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    getReply = queryOpenAi(update.message.text)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=getReply)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hello, I am @danielninetyfour's Bot. I use the ChatGPT, text-davinci-003 model.")

if __name__ == '__main__':
    application = ApplicationBuilder().token(telegramBotApiKey).build()
    
    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    
    application.add_handler(start_handler)
    application.add_handler(echo_handler)

    application.run_polling()

