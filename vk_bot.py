import os
import vk_api
import random
import uuid

from dotenv import load_dotenv
from dialog import fetch_dialogflow_answer
from vk_api.longpoll import VkLongPoll, VkEventType


def echo(event, vk_api, project_id,
         session_id, language_code):
    reply, fallback = fetch_dialogflow_answer(project_id, session_id,
                                              event.text,
                                              language_code)
    if not fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=reply,
            random_id=random.randint(1, 1000)
        )


if __name__ == "__main__":
    load_dotenv()
    google_project_id = os.environ["GOOGLE_PROJECT_ID"]
    google_session_id = str(uuid.uuid4())
    language_code = "ru-RU"

    vk_token = os.environ["VK_TOKEN"]
    vk_session = vk_api.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api, google_project_id,
                 google_session_id, language_code)
