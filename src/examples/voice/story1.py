#!/usr/bin/env python3
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A demo of the Google CloudSpeech recognizer."""
import argparse
import locale
import logging
import aiy.voice.tts
import time

from aiy.board import Board, Led
from aiy.cloudspeech import CloudSpeechClient


def get_hints(language_code):
    if language_code.startswith('fr_'):
        return ('allume',
                'éteins',
                'clignote',
		'répète après moi',
                'alouette',
                'au revoir')
    return None

def locale_language():
    language, _ = locale.getdefaultlocale()
    return language

def main():
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser(description='Assistant service example.')
    parser.add_argument('--language', default=locale_language())
    args = parser.parse_args()
    step = 0
    check = 0
    characterName = ''
    characterGender = ''
    characterPronom = ''
    villageName = ''
    locality = ''
    biome = ''
    ogreName = ''
    ogreAdjective = ''



    logging.info('Initializing for language %s...', args.language)
    hints = get_hints(args.language)
    client = CloudSpeechClient()

    aiy.voice.tts.say('Bonjour, je raconte des histoires, voulez-vous en entendre une ?')


    with Board() as board:
        while True:
            board.led.state = Led.ON
            board.button.wait_for_press()
            board.led.state = Led.BLINK
            text = client.recognize(language_code=args.language,
                                    hint_phrases=hints)
            # time.sleep(2)
            
            board.led.state = Led.OFF

            if text is None:
                aiy.voice.tts.say("Je n'ai pas compris, veuillez recommencer.")
                continue

            while step == check:
                
                text = text.lower()
                if 'oui' in text and step == 0:
                    aiy.voice.tts.say("Nous allons créer l'histoire ensemble.")
                    aiy.voice.tts.say("Pour commencer, comment se nomme le personnage principal ?")
                    step += 1
                    break
                elif step == 1:
                    characterName = text
                    aiy.voice.tts.say("Le personnage s'appelle"+characterName)
                    aiy.voice.tts.say("Est-ce un garçon ou une fille ?")
                    step += 1
                    break
                elif step == 2:
                    while characterGender != 'garçon' and characterGender != 'un garçon' and characterGender != 'fille' and characterGender != 'une fille':
                        characterGender = text
                        if characterGender == 'garçon' or characterGender == 'un garçon':
                            characterPronom = 'il'
                            aiy.voice.tts.say("Le personnage est un garçon")
                            step += 1
                            break
                        elif characterGender == 'fille' or characterGender == 'une fille':
                            characterPronom = 'elle'
                            aiy.voice.tts.say("Le personnage est une fille")
                            step += 1
                            break

                        aiy.voice.tts.say("Je n'ai pas compris, est-ce un garçon ou une fille ?")
                        break
                        
                    aiy.voice.tts.say("Comment s'appelle le village ?")
                    step += 1
                    break
                elif step == 3:
                    villageName = text
                    aiy.voice.tts.say("Le village s'appelle "+villageName)
                    aiy.voice.tts.say("Le village se trouve vers un désert, une forêt ou un lac ?")
                    step += 1
                    break
                elif step == 4:
                    biome = text
                    while biome != 'desert' and biome != 'un desert' and biome != 'forêt' and biome != 'une forêt' and biome != 'lac' and biome != 'un lac':
                        biome = text
                        if biome == 'desert' or biome == 'un desert':
                            aiy.voice.tts.say("Le village se trouve dans un désert")
                            step += 1
                            break
                        elif biome == 'forêt' or biome == 'une forêt':
                            aiy.voice.tts.say("Le village se trouve dans une forêt")
                            step += 1
                            break
                        elif biome == 'lac' or biome == 'un lac':
                            aiy.voice.tts.say("Le village se trouve dans un lac")
                            step += 1
                            break

                        aiy.voice.tts.say("Je n'ai pas compris, le village se trouve-t-il vers un desert, une forêt ou un lac ?")
                        break

                    aiy.voice.tts.say("Comment s'appelle l'ogre ?")
                    step += 1
                    break
                elif step == 5:
                    ogreName = text
                    aiy.voice.tts.say("L'ogre s'appelle "+ogreName)
                    aiy.voice.tts.say("Donne moi un adjectif qui décrit l'ogre.")
                    step += 1
                    break
                elif step == 6:
                    ogreAdjective = text
                    aiy.voice.tts.say("L'ogre est "+ogreAdjective)
                    aiy.voice.tts.say("Comment s'appelle le pays ou se déroule l'histoire ?")
                    step += 1
                    break
                elif step == 7:
                    locality = text
                    aiy.voice.tts.say("Le pays s'appelle "+locality)
                    aiy.voice.tts.say("Merci pour ces informations, je vais créer l'histoire.")
                    aiy.voice.tts.say("Voulez-vous l'entendre ?")
                    step += 1
                    break
                elif step == 8:
                    if 'oui' in text:
                        aiy.voice.tts.say("Très bien.")
                        aiy.voice.tts.say("Il était une fois "+characterName)
                        if characterGender == 'garçon':
                            aiy.voice.tts.say("un petit "+characterGender+" plein de vie" )
                        elif characterGender == 'fille':
                            aiy.voice.tts.say("une petite "+characterGender+" pleine de vie.")
                        aiy.voice.tts.say(" "+characterPronom+" habitait dans le village de "+villageName+" dans le biome "+biome+" en "+locality+". Chaque jour, "+characterPronom+" voyait le soleil apparaître derrière la colline et "+characterPronom+" demandait à sa mère : Maman, qu'y a-t-il derrière cette colline ?" +". Derrière la colline, il y un biome "+biome+", un endroit qui n'est pas fait pour les enfants. Seuls les adultes peuvent s'y aventurer car c'est un monde dangereux pouur qui ne connaît pas ses secrets. Un jour, tu pourras toi aussi aller au-delà de la colline. Mais avant, il te faut grandir et écouter les anciens : ils ont beaucoup de choses à t'apprendre.")
                        aiy.voice.tts.say("Mais "+characterName+" n’écoutait jamais personne. "+characterPronom+" préférait jouer avec ses amis et n’en faire qu’à sa tête. Un jour, "+characterPronom+" s’aventura en dehors du village mais sa mère rattrapa son enfant et le ramena fermement par le bras en lui disant : Ne t’éloigne jamais plus, c’est beaucoup trop dangereux. Je vais te dire ce qu’il y a derrière la colline : il y a "+ogreName+", l’ogre "+ogreAdjective+" qui dévore les enfants perdus.")
                        
                    

                        step += 1
                        break
                    elif 'non' in text:
                        aiy.voice.tts.say("Je vais créer l'histoire pour vous et vous pourrez l'écouter plus tard.")
                        step = 0
                        break

                
                

            check+=1

if __name__ == '__main__':
    main()
