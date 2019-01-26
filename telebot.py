import zipfile
import os
import time
import telepot
from telepot.loop import MessageLoop


def zipf(folders, zip_filename):
    zip = zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_LZMA)
    for folder in folders:
        for dirpath, dirnames, filenames in os.walk(folder):
            for filename in filenames:
                zip.write(
                    os.path.join(dirpath, filename),
                    os.path.relpath(os.path.join(dirpath, filename), os.path.join(folders[0], '../..')))
    zip.close()


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    if content_type == 'text':
        if msg['text'] == "/backup":
            bot.sendMessage(chat_id, "will generate a new backup, compression has started")
            folders = [
                "/home/klown/server/tf2/serverfiles/tf/addons",
                "/home/klown/server/tf2/serverfiles/tf/cfg",
                "/home/klown/server/tf2/lgsm/config-lgsm"
            ]
            zipf(folders, "/home/klown/bot/telegram/backup.zip")
            bot.sendMessage(chat_id, "compression successful, uploading")
            bot.sendDocument(chat_id, open("/home/klown/bot/telegram/backup.zip", 'rb'))
        elif msg['text'] == "/lastbackup":
            bot.sendMessage(chat_id, "uploading the last backup")
            bot.sendDocument(chat_id, open("/home/klown/bot/telegram/backup.zip", 'rb'))
        else:
            bot.sendMessage(chat_id, "commands: /backup, /lastbackup")


bot = telepot.Bot("api key here")
MessageLoop(bot, handle).run_as_thread()
print("listening")

while 1:
    time.sleep(10)
