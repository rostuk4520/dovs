from time import time
import vk_api
from threading import Thread
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType


class Bot(Thread):
    def __init__(self, acess_token, id, users):
        super(Bot, self).__init__()
        self.token = acess_token
        self.id = id
        self.users = users

    def run(self):
        vk_session = vk_api.VkApi(token=self.token)
        longpoll = VkBotLongPoll(vk_session, self.ID)
        vk = vk_session.get_api()

        def send_message(chat_id, message=None):
            vk.messages.send(
                random_id=get_random_id(),
                message=message,
                chat_id=chat_id
            )
        while True:
            try:
                time.sleep(0.1)
                for event in longpoll.listen():
                    if event.type == VkBotEventType.MESSAGE_NEW:
                        chat_id = event.chat_id
                        msg = event.message.get('text')
                        if (event.from_chat or event.from_user) and \
                                (event.message.get('from_id') in self.users):
                            if msg.lower().split()[0] == '+чс ':
                                text_msg = msg.lower().split()[1]
                                id_user = vk.users.get(
                                    user_ids=str(text_msg),
                                    fields='first_name,last_name')[0]['id']
                                vk.groups.ban(group_id=self.id,
                                              owner_id=id_user)
                                send_message(
                                    chat_id, f'[id{id_user}|Пользователь] забанен нахой.')
            except:
                pass


bot = Bot(
    acess_token='',
    # group token

    id=124,
    # group id

    users=[],
    # числовой ид тех кто может запускать бота

)

bot.start()
bot.join()
