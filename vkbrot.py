#!/usr/bin/python
# -*- coding: utf-8 -*-
# scripted by itjunky

from requests import get
from json import loads, dumps
from pprint import pprint
from random import choice
import vk

app_id, app_secret = '3697615', 'AlVXZFMUqyrnABp8ncuU' # habr
phone = "1234567"
passwd = "1234567"
user_id = "1"
scope = "friends,messages,offline"
api = ""
debug = 1

class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def get_token():
    global app_id, phone, passwd, api, scope
    auth_session = vk.AuthSession(app_id=app_id, user_login=phone, user_password=passwd, scope=scope)
    access_token, _ = auth_session.get_access_token()
    session = vk.Session(access_token=access_token)
    api = vk.API(session, lang='ru')
    return

def chek_permission():
    global api, user_id
    r = api.users.isAppUser(user_id=user_id)
    if debug: print 'User install app ', colors.OKGREEN, r, colors.ENDC
    r = api.account.getAppPermissions(user_id=user_id)
    if debug: print 'Permission is ', colors.OKGREEN, r, colors.ENDC

def get_poll_serv():
    r = api.messages.getLongPollServer()
    if debug: print 'Poll Server is ', colors.OKGREEN, r, colors.ENDC
    return r['server'], r['key'], r['ts']

def get_new_messages():
    print "Start grabbing messages"
    global api
    server, key, ts = get_poll_serv()

    while True:
        # wait for new action from Long Poll server
        r = get("http://%s?act=a_check&key=%s&ts=%s&wait=25&mode=2" % (server, key, ts)) 
	try:
            ts = r.json()["ts"] # need change after each connect
	except KeyError:
	    pass
        parsed_string = loads(r.content,encoding="utf-8")
        #print r.content # debug
        updates = parsed_string["updates"]
        for i in updates: # check every updates
            if i[0] == 4: # If new message
                try: # try to print
                    room_id, room_title = last_messages()
                    if not i[7]['from'] in ignored_users:
                        print colors.HEADER, room_id, colors.OKGREEN, room_title, colors.HEADER, i[7], colors.OKBLUE, i[6], colors.ENDC
                        #continue # skip analize messages from blacklisted users
                except TypeError:
                    print colors.FAIL, i[7], i[6], colors.ENDC
                    continue
                except KeyError: # print private message
                    print colors.HEADER, i[7], colors.OKBLUE, i[6], colors.ENDC
                    continue

                st_greet=(u'Привет', u'привет')
                st_bot=(u'бот', u'Бот')
                st_mat=(u'хуй', u'Хуй', u'бля', u'Бля', u'Пизд', u'пизд' u'ебу', u'ебa', u'сук', u'Сук')
                st_drugs=(u'трав', u'Трав', u'табл', u'Табл', u'люся', u'Люся', u'сибир', u'Сибир', u'нюха', u'гаш', u'Гаш', u'нарк')
                st_smile=(u':)', u'')

                if any(s in i[6] for s in st_greet): # select greet message
                    message = [u'Привет',            
                        u'Привеееет',                    
                        u'И вам добре',
                        u'Здаров',                           
                        u'Ооо, с возвращением =)',
                        u'Хай']         
                    random = choice(message)
                    response = api.messages.send(chat_id=room_id, message=random)
                    #response = get("%s.send?chat_id=%s&message=%s&v=5.37&access_token=%s" % (vkapiurl, room_id, random, token))
		    print colors.WARNING, "ОТВЕЧАЮ ПРИВЕТ", colors.ENDC, random

                if any(s in i[6] for s in st_bot): 
                    message = [u'Жованый крот',            
                        u'Да ты чо?..',                    
                        u'Нууу... И где этот ваш абармот?',
                        u'Где?',                           
                        u'Сноуден не 6от, вы чо!']         
                    random = choice(message)
                    response = api.messages.send(chat_id=room_id, message=random)
                    #response = get("%s.send?chat_id=%s&message=%s&v=5.37&access_token=%s" % (vkapiurl, room_id, random, token))
                    print colors.WARNING, "ОТВЕЧАЮ БОТ", colors.ENDC, random
                    #print response.content

                if u'Нет' in i[6]:
                    random = [u'Драндулет',
                        u'Дурака ответ']
                    response = api.messages.send(chat_id=room_id, message=random)
                    #response = get("%s.send?chat_id=%s&message=%s&v=5.37&access_token=%s" % (vkapiurl, room_id, message, token))
                    print colors.WARNING, "ОТВЕЧАЮ 42", colors.ENDC 
                    #print response.content

                if any(s in i[6] for s in st_mat):
                    message = [u'Жованый крот',                             
                        u'А Вы случаем не из посёлка Матюки?',              
                        u'Вроде и прилично выглядишь, а как сапожник...',   
                        u'Мааат перемат',                                   
                        u'И чего, с детьми, то же так будешь "беседовать"?',
                        u'Уххх.... Горелая перемычка',                      
                        u'Да как два байта переслать',                      
                        u'Вот прям настока?',                               
                        u'Да не при детях жеж!!!',                          
                        u'Ну ты тока полюбуйся на этого штриха']
                    random = choice(message)
                    response = api.messages.send(chat_id=room_id, message=random)
                    #response = get("%s.send?chat_id=%s&message=%s&v=5.37&access_token=%s" % (vkapiurl, room_id, random, token))
                    print colors.WARNING, "ОТВЕЧАЮ НА МАТ", colors.ENDC, random
                    #print response.content

                if any(s in i[6] for s in st_drugs):
                    message = [u'Жованый крот',
                        u'Опять шмыгают носом... и без меня...',
                        u'И мы то же ржали, аж зубы сохли =)',
                        u'Ты это пробовал?',
                        u'С ума сойти, с таких марафонов можно',
                        u'А я как-то сотку шрумов зохавал']
                    random = choice(message)
                    response = api.messages.send(chat_id=room_id, message=random)
                    #response = get("%s.send?chat_id=%s&message=%s&v=5.37&access_token=%s" % (vkapiurl, room_id, random, token))
                    print colors.WARNING, "ОТВЕЧАЮ ПРО ДРАГСЫ", colors.ENDC, random

def last_messages():
    response = api.messages.get(count=1)
    #get("https://api.vk.com/method/messages.get?count=1&v=5.37&access_token=%s" % token)
    #parsed_json = response.json()
#    print colors.HEADER, parsed_json['response']
    try:
       #print parsed_json['response']['items'][0]['user_id']
       #print parsed_json['response']['items'][0]['chat_id']
       #print parsed_json['response']['items'][0]['title']
       #print parsed_json['response']['items'][0]['body']
       #print colors.ENDC
       #return parsed_json['response']['items'][0]['chat_id'], parsed_json['response']['items'][0]['title']
       return response['items'][0]['chat_id'], response['items'][0]['title']
    except KeyError:
        pass

get("https://api.vk.com/method/stats.trackVisitor") # stat https://vk.com/stats?aid=1234567
get_token()
chek_permission()
get_new_messages()
