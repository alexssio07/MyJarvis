import datetime
import wikipedia
from pygame import mixer
import speech_recognition as sr
import time
import datetime
import pyjokes
import pywhatkit
import weathercom
import json
from pywhatkit.remotekit import start_server
from flask import Flask, request
from gtts import gTTS

listener = sr.Recognizer()
mixer.init()


def talk(text):
    tts = gTTS(text=text, lang='it')
    tts.save('tts_output_audio.mp3')
    mixer.music.load('G:\\Progetti Python\\MyJarvis\\tts_output_audio.mp3')
    mixer.music.play()
    while mixer.music.get_busy():  # wait for music to finish playing
        time.sleep(1)
        stop_action()
    mixer.music.unload()


def take_command():
    print('In ascolto..')
    try:
        with sr.Microphone() as source:
            audio = listener.listen(source)
            text = listener.recognize_google(audio, language="it")
            text = text.lower()
            print('Sto elaborando...')
            print(text)
            if 'jarvis' in text:
                text = text.replace('jarvis', '')
                if 'riproduci' in text:
                    song = text.replace('riproduci', '')
                    play_song_on_youtube(song)
                elif 'metti' in text:
                    text = text.replace('metti', '')
                    play_song_on_youtube(text)
                elif 'che ore sono' in text:
                    tell_me_time()
                elif 'che ora è' in text:
                    tell_me_time()
                elif 'chi era' in text:
                    text = text.replace('chi era', '')
                    tell_me_from_wikipedia(text)
                elif 'chi è' in text:
                    text = text.replace('chi è', '')
                    tell_me_from_wikipedia(text)
                elif 'chi sono' in text:
                    text = text.replace('chi sono', '')
                    tell_me_from_wikipedia(text)
                elif 'chi erano' in text:
                    text = text.replace('chi erano', '')
                    tell_me_from_wikipedia(text)
                elif 'che cosa è' in text:
                    text = text.replace('che cosa è', '')
                    tell_me_from_wikipedia(text)
                elif 'che cos' + 'e' in text:
                    text = text.replace('che cos' + 'e', '')
                    tell_me_from_wikipedia(text)
                elif 'dimmi una freddura' in text:
                    tell_me_joke()
                elif "che tempo fa a" in text:
                    text = text.replace("che tempo fa a", '')
                    print(text)
                    humidity, temp, phrase = tell_me_weather(text)
                    print(str(temp))
                elif "dimmi il meteo a" in text:
                    text = text.replace("dimmi il meteo a", '')
                    tell_me_weather(text)
    except:
        pass
    return text


def tell_me_time():
    time = datetime.datetime.now().strftime('%I:%M')
    print(time)
    talk('Sono le ore : ' + time)


def play_song_on_youtube(song):
    talk('Riproduco ' + song)
    pywhatkit.playonyt(song)
    print(song)


def tell_me_from_wikipedia(keyword):
    wikipedia.set_lang("it")
    info = wikipedia.summary(keyword, 3)
    print(info)
    talk(info)


def stop_action():
    try:
        with sr.Microphone() as source:
            audio = listener.listen(source)
            text = listener.recognize_google(audio, language="it")
            text = text.lower()
            if 'jarvis' in text:
                text = text.replace('jarvis', '')
                if 'stop' or 'basta' or 'fermati' in text:
                    mixer.stop()
                    mixer.music.unload()
    except:
        pass


def tell_me_weather(city):
    weather = weathercom.getCityWeatherDetails(city)
    humidity = json.load(weather)["vt1observation"]["humidity"]
    temp = json.loads(weather)["vt1observation"]["temperature"]
    phrase = json.loads(weather)["vt1observation"]["phrase"]
    print(city)
    return humidity, temp, phrase


def tell_me_joke():
    talk(pyjokes.get_joke('it'))



"""take_command()"""