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

from aiy.board import Board, Led
from aiy.cloudspeech import CloudSpeechClient


def get_hints(language_code):
    if language_code.startswith('fr_'):
        return ('allume',
                'éteins',
                'clignote',
		'répète après moi',
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

    logging.info('Initializing for language %s...', args.language)
    hints = get_hints(args.language)
    client = CloudSpeechClient()

    aiy.voice.tts.say('Bonjour, je raconte des histoires, voulez-vous en entendre une ?')

    with Board() as board:
        while True:
            if hints:
                logging.info('Say something, e.g. %s.' % ', '.join(hints))
            else:
                logging.info('Say something.')
            text = client.recognize(language_code=args.language,
                                    hint_phrases=hints)
            if text is None:
                logging.info('You said nothing.')
                continue

            logging.info('You said: "%s"' % text)
            text = text.lower()
            if 'allume' in text:
                board.led.state = Led.ON
            elif 'éteins' in text:
                board.led.state = Led.OFF
            elif 'clignote' in text:
                board.led.state = Led.BLINK
            elif 'répète après moi' in text:
                # Remove "repeat after me" from the text to be repeated
                to_repeat = text.replace('répète après moi', '', 1)
                aiy.voice.tts.say(to_repeat)
            elif 'oui' in text:
                board.led.state = Led.BLINK
                aiy.voice.tts.say('Il était une fois dans un royaume lointain...')
                board.led.state = Led.OFF
            elif 'au revoir' in text:
                aiy.voice.tts.say('au revoir')
                break

if __name__ == '__main__':
    main()
