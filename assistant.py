import speech_recognition as sr
from nltk import word_tokenize, corpus
import json
from scrapper import searchOnWiki

LANGUAGE_CORPUS = "portuguese"
SPEAKING_LANGUAGE = "pt-BR"
CONFIG_PATH = "config.json"


def start():
    global recognizer
    global stop_words
    global assistant_name
    global actions

    recognizer = sr.Recognizer()
    stop_words = set(corpus.stopwords.words(LANGUAGE_CORPUS))

    with open(CONFIG_PATH, "r") as config_file:
        config = json.load(config_file)

        assistant_name = config["name"]
        actions = config["actions"]

        config_file.close()


def listen_command():
    global recognizer

    command = None

    with sr.Microphone() as audio_source:
        recognizer.adjust_for_ambient_noise(audio_source)

        print("Fale alguma coisa...")
        speech = recognizer.listen(audio_source, timeout=5, phrase_time_limit=5)
        try:
            command = recognizer.recognize_google(speech, language=SPEAKING_LANGUAGE)
        except sr.UnknownValueError:
            pass

    return command


def process_audio_command(command_audio):
    global recognizer

    command = None

    with sr.AudioFile(command_audio) as audio_source:
        speech = recognizer.listen(audio_source)
        try:
            command = recognizer.recognize_google(speech, language=SPEAKING_LANGUAGE)
        except sr.UnknownValueError:
            pass

    return command


def remove_stop_words(tokens):
    global stop_words

    filtered_tokens = []
    for token in tokens:
        if token not in stop_words:
            filtered_tokens.append(token)

    return filtered_tokens


def tokenize_command(command):
    global assistant_name

    action = None
    object = None

    tokens = word_tokenize(command, LANGUAGE_CORPUS)
    if tokens:
        tokens = remove_stop_words(tokens)

        if len(tokens) >= 3:
            if assistant_name == tokens[0].lower():
                if(len(tokens) > 3):
                    actions = []
                    for token in tokens:
                        actions.append(token.lower())
                    object = tokens[-1].lower()
                else:
                    action = tokens[1].lower()
                    object = tokens[2].lower()

    return action, object


def validate_command(action, object):
    global actions

    valid = False

    if action and object:
        for registeredAction in actions:
            if action == registeredAction["name"].lower():
                if object in registeredAction["objects"]:
                    valid = True

                break

    return valid


def execute_command(action, object):
    if(len(action) > 2):
        searchOnWiki(object)
    print("vou executar o comando:", action, object)


if __name__ == '__main__':
    start()

    continuar = True
    while continuar:
        try:
            command = listen_command()
            print(f"processando o comando: {command}")

            if command:
                action, object = tokenize_command(command)
                valid = validate_command(action, object)
                if valid:
                    execute_command(action, object)
                else:
                    print("Não entendi o comando. Repita, por favor!")
        except KeyboardInterrupt:
            print("Tchau!")

            continuar = False
