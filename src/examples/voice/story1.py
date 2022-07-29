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
    friendName = ''
    friendGender = ''
    friendPronom = ''
    villageName = ''
    animal = ''
    animalName = ''
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
                if 'non' in text and step == 0:
                    aiy.voice.tts.say("Très bien, revenez plus tard si vous changez d'avis.")
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
                        
                    aiy.voice.tts.say("Comment s'appelle l'ami du personnage principal ?")
                    break
                elif step == 3:
                    friendName = text
                    aiy.voice.tts.say("L'ami du personnage s'appelle"+friendName)
                    aiy.voice.tts.say("Est-ce un garçon ou une fille ?")
                    step += 1
                    break
                elif step == 4:
                    while friendGender != 'garçon' and friendGender != 'un garçon' and friendGender != 'fille' and friendGender != 'une fille':
                        friendGender = text
                        if friendGender == 'garçon' or friendGender == 'un garçon':
                            friendPronom = 'il'
                            aiy.voice.tts.say("L'ami est un garçon")
                            step += 1
                            break
                        elif friendGender == 'fille' or friendGender == 'une fille':
                            friendPronom = 'elle'
                            aiy.voice.tts.say("L'amie est une fille")
                            step += 1
                            break

                        aiy.voice.tts.say("Je n'ai pas compris, est-ce un garçon ou une fille ?")
                        break
                        
                    aiy.voice.tts.say("Comment s'appelle le village ?")
                    break
                elif step == 5:
                    villageName = text
                    aiy.voice.tts.say("Le village s'appelle "+villageName)
                    aiy.voice.tts.say("Le village se trouve vers un désert, un bois ou un lac ?")
                    step += 1
                    break
                elif step == 6:
                    
                    while biome != 'désert' and biome != 'un désert' and biome != 'bois' and biome != 'un bois' and biome != 'lac' and biome != 'un lac':
                        biome = text
                        if biome == 'désert' or biome == 'un désert':
                            biome = 'désert'
                            aiy.voice.tts.say("Le village se trouve vers un désert")
                            step += 1
                            break
                        elif biome == 'bois' or biome == 'un bois':
                            biome = 'bois'
                            aiy.voice.tts.say("Le village se trouve vers un bois")
                            step += 1
                            break
                        elif biome == 'lac' or biome == 'un lac':
                            biome = 'lac'
                            aiy.voice.tts.say("Le village se trouve vers un lac")
                            step += 1
                            break
                        aiy.voice.tts.say("Je n'ai pas compris, le village se trouve-t-il vers un désert, une forêt ou un lac ?")
                        break

                    aiy.voice.tts.say("Comment s'appelle l'ogre ?")
                    break
                elif step == 7:
                    ogreName = text
                    aiy.voice.tts.say("L'ogre s'appelle "+ogreName)
                    aiy.voice.tts.say("Donne moi un adjectif qui décrit l'ogre.")
                    step += 1
                    break
                elif step == 8:
                    ogreAdjective = text
                    aiy.voice.tts.say("L'ogre est "+ogreAdjective)
                    aiy.voice.tts.say("Donnez-moi un nom d'animal.")
                    step += 1
                    break
                elif step == 9:
                    animal = text
                    # PRobleme
                    aiy.voice.tts.say("L'animal est un "+animal)
                    aiy.voice.tts.say("Merci pour ces informations, je vais créer l'histoire.")
                    aiy.voice.tts.say("Voulez-vous l'entendre ?")
                    step += 1
                    break
                elif step == 10:
                    if 'oui' in text:
                        aiy.voice.tts.say("Très bien.")
                        aiy.voice.tts.say("Il était une fois "+characterName+", un enfant plein de vie. "+characterPronom+" habitait dans le village de "+villageName+" à côté d'un grand "+biome+". Chaque jour, "+characterPronom+" voyait le soleil apparaître derrière la colline et "+characterPronom+" demandait à sa mère : Maman, qu'y a-t-il derrière cette colline ?" +". Derrière la colline, il y un grand "+biome+", un endroit qui n'est pas fait pour les enfants. Seuls les adultes peuvent s'y aventurer car c'est un monde dangereux pour qui ne connaît pas ses secrets. Un jour, tu pourras toi aussi aller au-delà de la colline. Mais avant, il te faut grandir et écouter les anciens : ils ont beaucoup de choses à t'apprendre.")
                        aiy.voice.tts.say("Mais "+characterName+" n’écoutait jamais personne. "+characterPronom+" préférait jouer avec ses amis et n’en faire qu’à sa tête. Un jour, "+characterPronom+" s’aventura en dehors du village mais sa mère rattrapa son enfant et le ramena fermement par le bras en lui disant : Ne t’éloigne jamais plus, c’est beaucoup trop dangereux. Je vais te dire ce qu’il y a derrière la colline : il y a "+ogreName+", l’ogre "+ogreAdjective+" qui dévore les enfants perdus.")
                        aiy.voice.tts.say("Malgré les avertissements de sa mère, "+characterName+" voulait à tout prix aller derrière la colline. "+characterPronom+" proposa à son ami "+friendName+" de tenter l’aventure. Son ami se montra peu enthousiaste à son idée. Nous sommes encore trop jeunes, dit "+friendName+", nous ne saurons pas nous débrouiller seules dans vers "+biome+". Et puis il y a "+ogreName+". Il est "+ogreAdjective+" et a déjà mangé des enfants tous crus. Vous n'êtes que des froussards dans ce village, se moqua "+characterName+". L'ogre "+ogreName+" ? Ce n'est qu'une histoire pour faire peur aux enfants ! Puisque c'est comme ça, j'irai seul")
                        aiy.voice.tts.say("L’occasion se présenta quelques jours plus tard. Toutes les femmes du village étaient parties ramasser des oignons sauvages et les hommes étaient occupés à dresser des chevaux. "+characterName+" en profita pour se mettre en marche. Où vas-tu de si bon matin ? lui demanda un ancien, qui était assis sous un arbre. A la crique ! mentit "+characterName+". Ne va pas plus loin ! lui cria le vieil homme. "+characterName+" avait maintenant dépassé la crique et se trouvait face à la colline. Une énorme joie envahit son coeur : ça y est, se dit-"+characterPronom+" fièrement, je serai en haut de cette colline, et je verrai enfin ce qu’il y a derrière. Et "+characterPronom+" s’élança, d'un pas léger, à l’assaut du mont.")
                        aiy.voice.tts.say("Et ce qu’"+characterPronom+" découvrit alors l’émerveilla : un horizon sans fin où se détachaient, ici et là, la silhouette d’un arbre ou un tapis de fleurs rouges. "+characterPronom+" s’assit et regarda longtemps ce paysage extraordinaire. Le silence fut soudain interrompu par un bruit étrange qui venait du ventre de "+characterName+". "+characterPronom+" sourit : « J’ai faim et je n’ai pas pensé à emporter de la nourriture. Mais ce n’est pas grave ! En descendant de l’autre côté, je trouverai bien de quoi manger ! » "+characterPronom+" dévala la pente et, arrivée dans le buATTENsh, "+characterPronom+" se mit à la recherche de bananes et de tomates sauvages. Mais de ce côté de la colline, aucun arbre fruitier ne poussait. Le soleil était maintenant à son zénith. "+characterName+", exténuée par la faim et la soif, décida de se reposer à l’ombre d’un acacia.")
                        aiy.voice.tts.say("Bonjour petit enfant, lui dit un animal qui se trouvait à côté de l'arbre. Que fais-tu ici ? Je suis "+characterName+" et je suis venue découvrir ce qu’il y a derrière la colline. Et toi, qui es-tu ? Je suis Nyii-Nyii, le "+animal+" zébré, et j’habite dans cet arbre. Nyii-Nyii, sais-tu où je pourrais trouver à boire et à manger ? Mais ici même ! J’ai souvent vu les femmes de ton village écraser les graines de mon arbre pour obtenir de la farine avec laquelle elles faisaient des galettes. Hélas ! soupira "+characterName+". Je ne sais pas faire cela. Je n’ai pas encore appris. "+characterName+" se mit en route, mais très vite "+characterPronom+" dut se rendre à l’évidence : "+characterPronom+" était bien perdu, et la nuit commençait à tomber.")
                        aiy.voice.tts.say(characterPronom+" se réfugia sous un arbre et "+characterPronom+" essaya de faire un feu en frottant un morceau de bois sur une écorce, mais n’y réussit pas. Alors "+characterPronom+" comprit qu’"+characterPronom+" allait passer la nuit sans lumière ni chaleur. « "+characterName+" ! "+characterName+" ! "+characterName+" ! » semblait dire le vent. « Quelqu’un m’appelle ! J’y vais. » s’exclama "+characterName+", reprenant espoir. Des lumières apparurent à l’horizon. Mais alors, les paroles de Mima lui revinrent à l’esprit : « La ruse favorite de l’ogre "+ogreName+" est de faire de grands feux pour attirer les enfants. » Terrorisée, "+characterName+" n’osa plus bouger. "+characterPronom+" se blottit contre l’arbre et tenta de rester éveillée pour ne pas être emportée par l’ogre. Mais au petit matin, épuisée, "+characterName+" finit par s’endormir.")
                        aiy.voice.tts.say("Dans son sommeil, "+characterName+" entendit une voix qui disait : "+characterPronom+" est ici ! Venez vite ! On aurait dit celle de son père. "+characterPronom+" ouvrit doucement les yeux. Sa mère était penchée vers son enfant. Maman ! Maman ! C’est vraiment toi ?  Comment m’avez-vous retrouvée ? L'ancien t’avait vu aller vers la crique et de là, ton père a suivi tes traces. Nous avons allumé de grands feux dans l’espoir qu’ils te guident vers nous. Nous avons crié ton nom dans le vent, mais tu n’as pas répondu. "+characterName+" se blottit contre sa mère tendrement. Installé entre ses parents, "+characterName+" promit de ne plus jamais aller seul au-delà de la colline. "+characterPronom+" attendrait d’avoir appris tout ce que les Anciens avaient à lui enseigner.")

                        aiy.voice.tts.say(" J'espère que l'histoire vous a plus. J'envoie l'histoire sur l'application comme ça vous pourrez l'écouter plus tard. Voulez-vous recommencer ?")
                        step = 0
                        check = -1
                        break
                    elif 'non' in text:
                        aiy.voice.tts.say("Je vais créer l'histoire pour vous et vous pourrez l'écouter plus tard. Voulez-vous recommencer ?")
                        step = 0
                        break
                    break
                # elif step == 11:
                #     aiy.voice.tts.say(" J'espère que l'histoire vous a plus. J'envoie l'histoire sur l'application comme ça vous pourrez l'écouter plus tard. Voulez-vous recommencer ?")
                #     step = 0
                #     break

                
                

            check+=1

if __name__ == '__main__':
    main()
