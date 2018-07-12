import slackbot.bot
from xml.etree.ElementTree import ElementTree
from urllib import request

import json 
import requests

@slackbot.bot.respond_to('hello')
def resp_hello(message):
    message.reply('こんにちは!q')

def fizzbuzz(num):
    '''fissbuzz 判定

    Args:

        num (int): 判定する数字

    Returns:
        str: num が 3の倍数: 'Fizz'
            num が 5の倍数: 'Buzz'
            num が 15の倍数: 'FizzBuzz'
            その他: 'Nothing'
    '''
    if num % 15 == 0:
        return 'FizzBuzz'
    elif num % 5 == 0:
        return 'Buzz'
    elif num % 3 == 0:
        return 'Fizz'

    return 'Nothing'

@slackbot.bot.respond_to(r'^fizzbuzz\s+(\d+)')
def resp_fizzbuzz(message, digitstr):
    '''fizzbuzz (数字) 形式への返答
    (数字) 部のfissbuzz判定を行い, 'fizzbuzz (数字) 判定' を返事する

    Args:

        message (slackbot.dispatcher.Message): slack message
        digtstr (str): 数値の文字列
    '''

    # fizzbuzz 判定
    fb = fizzbuzz(int(digitstr))

    # 返事する文字列を構成
    reply = 'fizzbuzz {0:s} {1:s}'.format(digitstr, fb)

    message.reply(reply)





