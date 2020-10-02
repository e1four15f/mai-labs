from typing import Sequence

import networkx as nx
import vk
from tqdm import tqdm
from vk.exceptions import VkAPIError


class VKApi:
    def __init__(self, token: str):
        self._session = vk.Session(access_token=token)  # Авторизация
        self._api = vk.API(self._session)

    def load_friend_as_graph(self, user_ids: Sequence[int]) -> nx.Graph:
        graph = nx.Graph()

        for g_id in tqdm(user_ids):
            try:
                friends = self._api.friends.get(user_id=g_id, fields='domain', v=5.85)
                member = self._api.users.get(user_id=g_id, fields='domain', v='5.85')
                graph.add_node(
                    member['domain'],
                    label='{} {}'.format(member['first_name'], member['last_name']),
                )
            except VkAPIError:
                # закрытый профиль не добавляем чтобы не портил картинку
                continue

            # каждого друга добавляем в граф
            for friend in tqdm(friends['items']):
                graph.add_node(
                    friend['domain'],
                    label='{} {}'.format(friend['first_name'], friend['last_name']),
                )

                # проверяем список друзей каждого друга
                try:
                    # получаем список друзей друзей
                    fs_of_f = self._api.friends.get(
                        user_id=friend['id'], fields='domain', v=5.85
                    )

                    for f_of_f in fs_of_f['items']:
                        # если друг есть в графе - добавить связь
                        if graph.has_node(f_of_f['domain']):
                            graph.add_edge(friend['domain'], f_of_f['domain'])
                except VkAPIError:
                    pass
        return graph
