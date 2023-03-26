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
    temperature: 1.4,
    promptPrefix: "",
})

let idArray = []
let objArray = {}

// Listen for any kind of message. There are different kinds of messages
bot.on('message', async (msg) => {
    console.log(msg)
    const textMsg = msg.text
    if (idArray.includes(msg.chat.id)) {


        // send a follow-up
        // console.log(objArray)
        // console.log(idArray)
        try {
            let res = await api.sendMessage(msg.text, {
                parentMessageId: objArray[msg.chat.id][0],
                // lastSent: moment().format('YYYY-MM-DD HH:mm:ss')
            })
            console.log(res)
            if (res.detail.usage.total_tokens >= 1000) {
                console.log("reseting convo")
                objArray[msg.chat.id] = [0]
            } else {
                console.log("convo within token")
                objArray[msg.chat.id] = [res.id]
            }

            // console.log("Follow up convo")
            // console.log(res)

            bot.sendMessage(msg.chat.id, res.text).then((msg) => {
                bot.sendMessage(1708060707, "<code>" + textMsg + JSON.stringify(msg) + "</code>", { parse_mode: "HTML" })
            })
        } catch (e) {
            bot.sendMessage(msg.chat.id, "Sorry there was an error. Please try again or use the /reset command." + e)
            bot.sendMessage(1708060707, JSON.stringify(e))
        }
    } else {
        try {
            idArray.push(msg.chat.id)
            let res = await api.sendMessage(msg.text)
            console.log(res)
            objArray[msg.chat.id] = [res.id]

            // console.log("First Convo" + res)

            bot.sendMessage(msg.chat.id, res.text).then((msg) => {
                bot.sendMessage(1708060707, "<code>" + textMsg + JSON.stringify(msg) + "</code>", { parse_mode: "HTML" })
                // console.log(msg)
            })
        } catch (e) {
            bot.sendMessage(msg.chat.id, "Sorry there was an error. Please try again or use the /reset command." + e)
            bot.sendMessage(1708060707, JSON.stringify(e))
        }

    }

});


bot.onText(/^\/reset$/i, async (msg) => {
    try {
        let res = await api.sendMessage("reset", {
            parentMessageId: objArray[msg.chat.id][0],
            // lastSent: moment().format('YYYY-MM-DD HH:mm:ss')
        })
        objArray[msg.chat.id] = [0]
        console.log(res)
        bot.sendMessage(msg.chat.id, "Convo reset.")
    } catch (e) {
        bot.sendMessage(msg.chat.id, "Sorry, there was an error. You may not have a convo to rest." + e)
        bot.sendMessage(1708060707, JSON.stringify(e))
    }
});
