# MAIN SCRIPT

import datetime
import logging
from telegram.ext.filters import Filters
from telegram.ext import MessageHandler
from telegram.ext import CommandHandler
from telegram.ext import Updater
from yt_api import get_id, get_stats, get_vid_info, get_thumbnail, get_rating


fhand = open('token.txt')
secret_token = None
for i in fhand:
    secret_token = i
# print(secret_token)
url = None


updater = Updater(token=secret_token)
dispatcher = updater.dispatcher
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def start(update, context):
    cmdlist = 'This is Jesher\'s YT_Stat_bot'+"\n"+'The Bot understands the following commands:'+"\n"+'/clink - To get the stats of a YT channel' + \
        "\n"+'/vlink - To get the stats of a YT video'+"\n" + \
        '/tlink - To get the Thumbnail Url of the video'+"\n"
    context.bot.send_message(chat_id=update.effective_chat.id, text=cmdlist)


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


def get_channel_stats(update, context):
    link = ''.join(context.args)
    if link.startswith('https://www.youtube')or link.startswith('https://www.youtu.be')or link.startswith('https://youtube')or link.startswith('https://youtu.be'):
        stats = get_stats(get_id(link))
        c_name = 'Channel Name:\n'+stats[0]
        c_desc = 'Channel Description:\n'+stats[1]
        c_country = 'Channel Country:\n'+stats[2]
        c_sub = 'No.of Subscribers:\n'+str(stats[3])
        c_vidcount = 'No. of Videos:\n'+str(stats[4])
        outs = c_name+"\n\n"+c_desc+"\n\n"+c_country + \
            "\n\n"+c_sub+"\n\n"+c_vidcount+"\n\n"
        context.bot.send_message(chat_id=update.effective_chat.id, text=outs)
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text='Bad Link!!!')


ch_link_handler = CommandHandler('clink', get_channel_stats)
dispatcher.add_handler(ch_link_handler)


def get_video_stats(update, context):
    url = ''.join(context.args)
    if url.startswith('https://www.youtube/c')or url.startswith('https://www.youtu.be/c')or url.startswith('https://youtube')or url.startswith('https://youtu.be'):
        stats = get_vid_info(url)
        r = get_rating(url)
        vlen = str(stats[2])
        dateu = str(stats[4])
        nof = str(stats[3])
        nol = str(r[0])
        nodl = str(r[1])
        noc = str(r[2])
        outs = 'Author Name:\n'+stats[0]+"\n\n"+'Video Title:\n'+stats[1]+"\n\n"+'Video Length:\n'+vlen+"\n\n"+'Date Of Upload:\n'+dateu+"\n\n" + \
            'No.of Views:\n'+nof+"\n\n"+'-------RATINGS---------\n'+'No.of Likes:\n' + \
            nol+"\n\n"+'No.of Dislikes: \n'+nodl+"\n\n"+'No.of Comments: \n'+noc+"\n"
        context.bot.send_message(chat_id=update.effective_chat.id, text=outs)
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text='Bad Link!!')


v_link_handler = CommandHandler('vlink', get_video_stats)
dispatcher.add_handler(v_link_handler)


def get_thumbnail_url(update, context):
    url = ''.join(context.args)
    if url.startswith('https://www.youtube')or url.startswith('https://www.youtu.be')or url.startswith('https://youtube')or url.startswith('https://youtu.be'):
        turl = get_thumbnail(url)
        outs = 'ThumbNail Url:'+"\n"+turl
        context.bot.send_message(chat_id=update.effective_chat.id, text=outs)


th_handler = CommandHandler('tlink', get_thumbnail_url)
dispatcher.add_handler(th_handler)


def unknown(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text='Sorry! Invalid Commmand.')


unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)


updater.start_polling()
# updater.stop()
