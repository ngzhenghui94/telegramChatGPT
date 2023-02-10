import { ChatGPTAPI } from 'chatgpt'
import TelegramBot from "node-telegram-bot-api";
import dotenv from "dotenv";
import moment from "moment-timezone";
moment.tz.setDefault("Asia/Singapore");
dotenv.config()

const bot = new TelegramBot(process.env.TELEGRAMBOTAPIKEY, { polling: true });

const api = new ChatGPTAPI({
    apiKey: process.env.APIKEY,
    debug: true,
    temperature: 0.9,
    promptPrefix: "",
})

let idArray = []
let objArray = {}

// Listen for any kind of message. There are different kinds of messages
bot.on('message', async (msg) => {
    console.log(msg)
    if (idArray.includes(msg.chat.id)) {
        // send a follow-up
        console.log(objArray)
        console.log(idArray)
        let res = await api.sendMessage(msg.text, {
            conversationId: objArray[msg.chat.id][0],
            parentMessageId: objArray[msg.chat.id][1],
            lastSent: moment().format('YYYY-MM-DD HH:mm:ss')
        })
        console.log("Follow up convo" + res)
        bot.sendMessage(msg.chat.id, res.text);
        bot.sendMessage(process.env.myTelegramId, msg)
    } else {
        
        idArray.push(msg.chat.id)
        let res = await api.sendMessage(msg.text)
        objArray[msg.chat.id] = [res.conversationId, res.id]
        
        console.log("First Convo" + res)
        bot.sendMessage(msg.chat.id, res.text)
        bot.sendMessage(process.env.myTelegramId, msg)
    }    
});


