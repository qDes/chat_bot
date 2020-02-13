import argparse
import dialogflow_v2 as dialogflow
import json
import os
import uuid

from dotenv import load_dotenv

# [START dialogflow_detect_intent_text]
def detect_intent_texts(project_id, session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs.
    Using the same `session_id` between requests allows continuation
    of the conversation."""
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session))

    for text in texts:
        text_input = dialogflow.types.TextInput(text=text, language_code=language_code)

        query_input = dialogflow.types.QueryInput(text=text_input)

        response = session_client.detect_intent(
            session=session, query_input=query_input
        )

        print("=" * 20)
        print("Query text: {}".format(response.query_result.query_text))
        print(
            "Detected intent: {} (confidence: {})\n".format(
                response.query_result.intent.display_name,
                response.query_result.intent_detection_confidence,
            )
        )
        print("Fulfillment text: {}\n".format(response.query_result.fulfillment_text))


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
    for phrase in phrases.get('questions'):
        intent["training_phrases"].append({"parts":[{"text": phrase}]})
    return intent


def fetch_intents(project_id):
    intents_client = dialogflow.IntentsClient()
    parent = intents_client.project_agent_path(project_id)
    intents = intents_client.list_intents(parent)
    result = []
    for intent in intents:
        result.append(intent.display_name)
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


if __name__ == "__main__":
    load_dotenv()
    project_id = os.environ["GOOGLE_PROJECT_ID"]
    session_id = str(uuid.uuid4())
    texts = ["привет" ]
    language_code = "ru-RU"
    create_intents(project_id, "questions.json")