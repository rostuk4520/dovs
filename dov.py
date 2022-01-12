import vk_api
from vk_api.utils import get_random_id
from vk_api.longpoll import VkLongPoll, VkEventType
from threading import Thread
import time


class Bot(Thread):
    def __init__(self, acess_token, prefix, dovs=[]):
        super(Bot, self).__init__()
        self.token = acess_token
        self.prefix = prefix
        self.dovs = dovs

    def run(self):
        self.vk_session = vk_api.VkApi(token=self.token)
        self.longpoll = VkLongPoll(self.vk_session)
        vk = self.vk_session.get_api()

        while True:
            time.sleep(0.1)
            try:
                for event in self.longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW \
                        and (event.from_user or event.from_chat) \
                            and (event.user_id in self.dovs):
                        if len(event.message.lower().split()) > 0 \
                                and event.message.lower().split()[0] == self.prefix:
                            text = event.message[len(self.prefix)+1:]
                            result = vk.messages.getHistory(
                                count=1,
                                peer_id=event.peer_id,
                                rev=0)['items'][0]
                            if 'reply_message' in result:
                                vk.messages.send(
                                    random_id=get_random_id(),
                                    peer_id=event.peer_id,
                                    message=text,
                                    reply_to=result['reply_message']['id'])
                            else:
                                vk.messages.send(
                                    random_id=get_random_id(),
                                    peer_id=event.peer_id,
                                    message=text)
            except:
                pass


me = Bot(acess_token='token',  # тут вставлять токен
         prefix='pref',        # префикс для довов
         dovs=[123, 321])      # довы через запятую

you = Bot(acess_token='token',   # тут вставлять токен
          prefix='pref',         # префикс для довов
          dovs=[123, 321])       # довы через запятую

USERS = [me, you, ]

for user in USERS:
    user.start()
