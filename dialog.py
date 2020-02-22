import argparse
import dialogflow_v2 as dialogflow
import json
import os

from dotenv import load_dotenv


def fetch_dialogflow_answer(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.types.TextInput(text=text,
                                            language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = session_client.detect_intent(session=session,
                                            query_input=query_input)
    response_text = response.query_result.fulfillment_text
    is_fallback = response.query_result.intent.is_fallback
    return response_text, is_fallback


def read_training_set(filename):
    with open(filename, "r") as f:
        intent = json.loads(f.read())
    return intent


def make_intent(name, phrases):
    intent = {
        "display_name": name,
        "messages": [{"text": {"text": [phrases.get('answer')]}}],
        "training_phrases": [],
    }
    intent["training_pharses"] = [{"parts": [{"text": phrase}]} for
                                  phrase in phrases.get('guestions')]
    return intent


def fetch_intents(project_id):
    intents_client = dialogflow.IntentsClient()
    parent = intents_client.project_agent_path(project_id)
    intents = intents_client.list_intents(parent)
    result = [intent.display_name for intent in intents]
    return result


def create_intents(project_id, filename):
    client = dialogflow.IntentsClient()
    parent = client.project_agent_path(project_id)
    training_set = read_training_set(filename)
    intents = fetch_intents(project_id)
    for key, value in training_set.items():
        if key in intents:
            continue
        intent = make_intent(key, value)
        response = client.create_intent(parent, intent)
        print(response)


def get_args():
    parser = argparse.ArgumentParser(description="dialogflow learner")
    parser.add_argument('-f', help='filename')
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    filename = args.f
    load_dotenv()
    project_id = os.environ["GOOGLE_PROJECT_ID"]
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google-credentials.json"
    texts = ["Как устроиться на работу"]
    language_code = "ru-RU"
    create_intents(project_id, filename)
