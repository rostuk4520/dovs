import time
import vk_api
from threading import Thread
from vk_api.utils import get_random_id
from vk_api.longpoll import VkLongPoll, VkEventType


class Bot(Thread):
    def __init__(self, acess_token, id):
        super(Bot, self).__init__()
        self.token = acess_token
        self.id = id

    def run(self):
        self.vk_session = vk_api.VkApi(token=self.token)
        self.longpoll = VkLongPoll(self.vk_session)
        vk = self.vk_session.get_api()

        def send_message(chat_id, message=None):
            vk.messages.send(
                random_id=get_random_id(),
                message=message,
                peer_id=chat_id
            )

        def find_user_id(message):
            if 'reply_message' in vk.messages.getHistory(
                    count=1,
                    peer_id=event.peer_id,
                    rev=0)['items'][0]:
                user_id = vk.messages.getHistory(count=1,
                                                 peer_id=event.peer_id,
                                                 rev=0)['items'][0][
                    'reply_message'][
                    'from_id']
            elif message.find('https://vk.com/') != -1:
                user_id = message.split('https://vk.com/')[1]
            elif message.find('@') != -1:
                user_id = message.split('[id')[1].split('|')[0]
            elif message.find('[id') != -1:
                user_id = message.split('[id')[1].split('|')[0]
            else:
                user_id = 0
            user_id = vk.users.get(
                user_ids=str(user_id),
                fields='first_name,last_name')[0]['id']
            return int(user_id)
        
        while True:
            try:
                time.sleep(0.1)
                for event in self.longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW and event.from_me:
                        if event.message.lower().split()[0] == '+чс':
                            id_user = find_user_id(event.message.lower().split()[1])
                            print(id_user)
                            vk.groups.ban(group_id=self.id,
                                            owner_id=id_user)
                            print('забанен')
                            send_message(
                                event.peer_id, f'[id{id_user}|Пользователь] забанен нахой.')
            except Exception as e:
                print(e)


bot = Bot(
    acess_token='',
    # user token

    id=,
    # group id

)

bot.start()
bot.join()
