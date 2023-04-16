import speech_recognition as sr
from nltk import word_tokenize, corpus
import json
from scrapper import searchOnWiki
import os
from text_to_speech import save
from pydub import AudioSegment
from pydub.playback import play
import shutil

LANGUAGE_CORPUS = "portuguese"
SPEAKING_LANGUAGE = "pt-BR"
CONFIG_PATH = "config.json"


def clear():
    print("\n" * os.get_terminal_size().lines)

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

        # print("Tokens", tokens)

        if len(tokens) >= 3:
            if assistant_name == tokens[0].lower():
                if(len(tokens) > 3):
                    object_strings = []
                    for token in tokens:
                        object_strings.append(token.lower())
                    action = object_strings[1]
                    object = ' '.join(object_strings[2::])
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


def execute_command(action, object, exec_audio):
    searchType = 'page'
    section = None
    
    if 'autores' in object:
        object = 'literatura grega'
        searchType = 'section'
        section = 'Principais Autores'

    title, result = searchOnWiki(object,section,searchType)

    if title and result:
        print('*' * len(title) * 3)
        print(' ' * len(title) + '\033[;1m' + title + '\033[0;0m')
        print('*' * len(title) * 3)
        print('\n')

        try:
            print(result)
            if exec_audio:
                print('\033[1;36mcarregando áudio\033[0;0m')
                save(str(result), 'pt', file='./__temp/{}.mp3'.format(title.lower()))
                audio = AudioSegment.from_mp3('./__temp/{}.mp3'.format(title.lower()))
                play(audio)
                shutil.rmtree('./__temp')
                os.mkdir('./__temp')
        except:
            print('\033[1;31mNão foi possível gerar o áudio!\033[0;0m')
            print(result)

        exit()
    
    print('\033[1;31mNão conseguimos completar a sua pesquisa, por favor tente novamente!\033[0;0m')


if __name__ == '__main__':
    start()

    repeat = True
    while repeat:
        try:
            command = listen_command()
            clear()
            print(f"\033[1;36mprocessando o comando:\033[0;0m {command}\n")

            if command:
                action, object = tokenize_command(command)
                valid = validate_command(action, object)
                if valid:
                    execute_command(action, object, True)
                else:
                    print("\033[1;31mNão entendi o comando. Repita, por favor!\033[0;0m")
        except KeyboardInterrupt:
            print("Tchau!")

            repeat = False
