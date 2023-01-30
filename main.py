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
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
    )
    print(response.choices[0].text)
    return response.choices[0].text

def imagineOpenAI(msg):
    response = openai.Image.create(
        prompt=str(msg),
        n=1,
        size="256x256"
    )
    print(response)
    return response['data'][0]['url']

telegram_conversations = {}



async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    value = telegram_conversations.get(update.effective_chat.id, None)
    print(value)
    # print(telegram_conversations[update.effective_chat.id])
    if value is not None:
        telegram_conversations[update.effective_chat.id] += "Human: " + update.message.text + "\n"
    else:
        telegram_conversations[update.effective_chat.id] = "Human: " + update.message.text + "\n"
    getReply = queryOpenAi(telegram_conversations[update.effective_chat.id])
    telegram_conversations[update.effective_chat.id] += "AI: " + getReply + "\n"
    print(telegram_conversations)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=getReply)
    await context.bot.send_message(chat_id=myTelegramId, text=update)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hello, I am @danielninetyfour's Bot. I use OpenAI's, text-davinci-003 model.")

async def imagine(update: Update, context: ContextTypes.DEFAULT_TYPE):
    imageURL = imagineOpenAI(update.message.text)
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=imageURL)


if __name__ == '__main__':
    application = ApplicationBuilder().token(telegramBotApiKey).build()
    
    start_handler = CommandHandler('start', start)
    imagine_handler = CommandHandler('imagine', imagine)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    
    application.add_handler(start_handler)
    application.add_handler(imagine_handler)
    application.add_handler(echo_handler)

    application.run_polling()

