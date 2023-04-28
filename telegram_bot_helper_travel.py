#utf-8
import telebot
from telebot import types
import requests
import datetime
import json
import os.path
import re
token_bot=your_token_bot_of_BotFather

path_data_base = place_keeping

url_get_coords_by_city="http://api.openweathermap.org/geo/1.0/direct"
url_get_city_by_coords="http://api.openweathermap.org/geo/1.0/reverse"
url_get_weather_by_coords="https://api.openweathermap.org/data/2.5/forecast"
token_openweather=str(your_token_openweather.org)

displayed_words={
    'help':[
        'help','Help','/help','помощь','Помощь'
        ],
    'stop':[
        ['stop','/stop'],
        'Заполнение формы отменено.'
        ],
    'commands':['Я хочу задать новую поездку.',
                'Я хочу поехать ...',
                'Куда я могу поехать ...',
                'Показать все мои поездки.',
                'Показать все мои поездки и их условия.',
                'Удалить поездку',
                'Stop'
                ],
    'description_cmd':['Эта команда создает новую поездку,впоследствии по которой вы сможете производить поиск',
                       'После этой команды пишется  название поездки также, как и до этого вы писали,команда возращяет ближайшее время, когда вы сможете поехать',
                       'После этой команды пишется дата,когда вы хотите поехать. Команда вернет вам время и название поездки куда вы можете поехать. Формат даты:\'год-месяц-день\'(Возможно до 5 дней вперед)',
                       'Эта команда показывает все зарегистрированные ранее поездки',
                       'Эта команда показыввает все зарегистрированные ранее поездки и условия погоды,которые для них требуются',
                       'Эта команда удаляет вашу поездку по названию.',
                       'Эта команда прекращает выполнение команды, удаляя все данные введенные в эту команду'
                       ],
    'unknown_answer':'Я тебя, к сожалению, не понял.\nПроверь введенный тобой текст.\nДля более подробной информации напиши:\n\'Помощь\'',

    'command_1':{
        'answer':['Напишите название места,которое вы хотите задать.',
                'Напишите рядом с каким городом находится данное место или его координаты:\nШирота,Долгота',
                'Далее выберите один вариант из предложенных.',
                'Какая температура вам больше всего подходит для вашего занятия?',
                'Какой ветер вам больше всего подходит для вашего занятия?',
                'Какие осадки вам больше всего подходят для вашего занятия?'
                  ],
        'temperatyre' :[
                'Очень жарко >30 градусов',
                'Жарко от 20 до 30 градусов',
                'Тепло от 10 до 20 градусов',
                'Прохладно от 0 до 10 градусов',
                'Холодно от -15 до 0 градусов',
                'Очень холодно <-15 градусов',
                'Все равно'
                  ],
        'wind':[
                'Очень сильный >20 м/с',
                'Сильный от 15 до 20 м/с',
                'Нормальный от 10 до 15 м/с',
                'Слабый от 5 до 10 м/с',
                'Очень слабый от 0 до 5 м/с',
                'Все равно'
                ],
        'rain':[
            'Есть дождь',
            'Нет дождя',
            'Все равно'
                ],
        'end':'Ваши данные были успешны сохранены'
                  },

    'command_2':{
        'answer':[
            'Напишите название поездки в таком же виде, как вводили ранее',
            'Такой поездки нет среди ранее записанных',
            'Вот что нашлось по вашему запросу:'
            ]
                },
    'command_3':['Вот все ваши поездки:\n\t','У вас нет поездок'],
    'command_4':['Вот все ваши поездки и все их условия:\n\t','У вас нет поездок'],
    'command_5':['Введите дату,на которую вы хотите просмотреть все возможные поездки(\'день.месяц.год\'-формат даты,каждый параметр задается в числовом виде,год-в полном виде )'],
    'True':'Да',
    'False':'Нет'
    
    }


def read_data_base():
    global data_base
    if not(os.path.exists(path_data_base)):
        with open(path_data_base,'w') as read_file:
            data_base={}
        del read_file
    else:
        with open(path_data_base,'r') as read_file:
            try:
                data_base=json.load(read_file)
            except:
                data_base={}
        del read_file
def rewrite_data_base():
    global data_base
    with open(path_data_base,'w') as rewrite_file:
        try:
            rewrite_file.write(json.dumps(data_base))
        except:
            print('Error write file')
    del rewrite_file

def get_weather():
    params_get_weather_by_coords = {
    "appid": token_openweather,
    "lat": None,
    "lon": None,
    "units": "metric",
    "lang": "ru",
    "cnt":None
    }
    params_get_city_by_coords={
        "appid":token_openweather,
        "lat":None,
        "lon":None,
        "limit":1
    }
    params_get_coords_by_city= {
    "appid": token_openweather,
    "q": None
    }
    def inner(item,param,cnt=1):
        nonlocal params_get_weather_by_coords
        nonlocal params_get_coords_by_city

        def get_city_by_coords(lat:float,lon:float):
            params_get_city_by_coords["lat"],params_get_city_by_coords["lon"]=lat,lon
            city_name=requests.get(url=url_get_city_by_coords,params=params_get_city_by_coords).json()[0]
            ans={}
            try:
                ans['city_name']=city_name['local_names']['ru']
            except:
                ans['city_name'] = None
            try:
                ans['country']=city_name['country']
            except:
                ans['country']=None
            try:
                ans['state']=city_name['state']
            except:
                ans['state']=None
            return ans
        
        def get_coords_by_city(city_name:str):
            params_get_coords_by_city['q']=city_name
            coords = requests.get(url=url_get_coords_by_city, params=params_get_coords_by_city).json()
            return coords[0]['lat'],coords[0]['lon']
        def get_weather_by_coords(lat:float,lon:float):
            params_get_weather_by_coords["lat"], params_get_weather_by_coords["lon"] = lat, lon
            weather = requests.get(url = url_get_weather_by_coords, params = params_get_weather_by_coords).json()
            return list(map(lambda x:{'time':datetime.datetime.strptime(x['dt_txt'],'%Y-%m-%d %H:%M:%S')+datetime.timedelta(hours=3),
                                      'temperatyre':x['main']['temp'],
                                      'wind':x['wind']['speed'],
                                      'rain':x['weather'][0]['main']=='Rain'
                                      },weather['list']))

        
        if item=='get_city_by_coords':
            return get_city_by_coords(*param)
        elif item=='get_coords_by_city':
            return get_coords_by_city(param)
        elif item=='get_weather_by_coords':
            return get_weather_by_coords(*param)
        else:
            print('Error in func: get_weather. No understand params\(item\)=\'',item,'\'')
        
    return inner
def work_bot():
    def stop():
        nonlocal step
        nonlocal inputting
        nonlocal number_cmd
        step=0
        inputting=[]
        number_cmd=None
        keyboard=types.ReplyKeyboardMarkup()
        keyboard.add(*displayed_words['commands'])
        return keyboard
    def helper():
        nonlocal inputting
        inputting=[]
        ans='Вот некоторые из основных команд:\n'
        for i in range(len(displayed_words['commands'])):
            ans+='\t\t\''+displayed_words['commands'][i]+'\' -- '+displayed_words['description_cmd'][i]+'\n'
        return ans    
    def sender_ms(text,reply_markup=types.ReplyKeyboardRemove()):
        bot.send_message(chat_id,text,reply_markup=reply_markup)

    
    bot=telebot.TeleBot(token_bot)
    number_cmd=None #счет начинется с 1
    step=0
    inputting=[]
    chat_id=0
    @bot.message_handler(commands = ['start'])
    def start(message):
        nonlocal chat_id
        chat_id=message.chat.id
        keyboard = types.ReplyKeyboardMarkup()
        keyboard.add(*displayed_words['commands'])
        sender_ms('Привет!\n' + helper(), keyboard)
    @bot.message_handler(content_types=['text'])
    def get_messages(message):
        nonlocal step
        nonlocal number_cmd
        nonlocal inputting
        global data_base
        mess=message.text.strip()
        if mess.lower() in displayed_words['help']:
            sender_ms(helper())
        elif mess.lower() in displayed_words['stop'][0]:
            sender_ms(displayed_words['stop'][1],stop())
        elif step==0 and mess in displayed_words['commands']:
            number_cmd=displayed_words['commands'].index(mess)+1
        elif step!=0:
            inputting.append(mess)
        else:
            sender_ms(displayed_words['unknown_answer'],stop())


         #выполнение команд   
        
        
        if number_cmd==1:#'Я хочу задать новую поездку.'
            if step==0:
                sender_ms(displayed_words['command_1']['answer'][0])
                step+=1
            elif step==1:
                sender_ms(displayed_words['command_1']['answer'][1])
                inputting.append(inputting.pop().capitalize())#название поездки
                step+=1
            elif step==2:#ввод координат или города
                keyboard=types.ReplyKeyboardMarkup()
                keyboard.add(*displayed_words['command_1']['temperatyre'])
                text=inputting.pop().replace(' ','').split(',')
                if len(text)==1:#city
                    if text[0].isalpha():
                        keyboard=types.ReplyKeyboardMarkup()
                        keyboard.add(displayed_words['True'],displayed_words['False'])
                        coords_new_element_datebase=get_weather('get_coords_by_city',text[0])
                        city_name_new_element_database=get_weather('get_city_by_coords',coords_new_element_datebase)
                        if coords_new_element_datebase!=None:
                            inputting.append(city_name_new_element_database)
                            inputting.append(coords_new_element_datebase)
                            sender_ms('Вы хотели задать этот город:\nНазвание города-'+\
                                          str(city_name_new_element_database['city_name'])+\
                                          '\nГосударство-'+\
                                          str(city_name_new_element_database['state'])+\
                                          '\nСтрана-'+\
                                          str(city_name_new_element_database['country'])+\
                                          '\nКоординаты(широта,долгота)-'+\
                                          str(coords_new_element_datebase[0])+\
                                            str(coords_new_element_datebase[1])+'?',
                                          keyboard)
                            step+=1
                        else:
                            sender_ms('Заданный вами город не найден.Введите еще раз.')     #{'shown':{'city':'','state':'','country','wind','temperatyre','rain'},'hidden':{'rain':lambda x:1,temperatyre:lambda,'wind'}}
                        
                    else:
                        sender_ms(displayed_words['unknown_answer'])
                elif len(text)==2:#coords
                    if  re.fullmatch(r'-{0,1}\d+\.{0,1}\d*',text[0]) and \
                        re.fullmatch(r'-{0,1}\d+\.{0,1}\d*',text[1]) and -90<=float(text[0])<=90 and -180<=float(text[1])<=180:
                        
                            keyboard=types.ReplyKeyboardMarkup()
                            keyboard.add(displayed_words['True'],displayed_words['False'])
                            coords_new_element_datebase=tuple(map(float,text))
                            city_name_new_element_database=get_weather('get_city_by_coords',text)
                            inputting.append(city_name_new_element_database)
                            inputting.append(coords_new_element_datebase)
                            sender_ms('Вы хотели задать этот город:\nНазвание города-'+\
                                          str(city_name_new_element_database['city_name'])+\
                                          '\nОбласть-'+\
                                          str(city_name_new_element_database['state'])+\
                                          '\nСтрана-'+\
                                          str(city_name_new_element_database['country'])+\
                                          '\nКоординаты(широта,долгота)-'+\
                                          str(coords_new_element_datebase[0])+', ' +\
                                          str(coords_new_element_datebase[1])+'?',
                                          keyboard)
                            step+=1
                        
                    else:
                        sender_ms(displayed_words['unknown_answer'])
                else:
                    sender_ms(displayed_words['unknown_answer'])
            elif step==3:
                text=inputting.pop()
                if text==displayed_words['True']:
                    keyboard=types.ReplyKeyboardMarkup()
                    keyboard.add(*displayed_words['command_1']['temperatyre'])
                    sender_ms(displayed_words['command_1']['answer'][2])
                    sender_ms(displayed_words['command_1']['answer'][3],keyboard)
                    step+=1
                elif text==displayed_words['False']:
                    inputting.pop()
                    inputting.pop()#удаление координат и города
                    step-=1
                    sender_ms('Введите местоположение поездки еще раз')
                else:
                    keyboard=types.ReplyKeyboardMarkup()
                    keyboard.add(displayed_words['True'],displayed_words['False'])
                    sender_ms(displayed_words['unknown_answer'],keyboard)
            elif step==4:
                if inputting[-1] in displayed_words['command_1']['temperatyre']:
                    if inputting[-1]==displayed_words['command_1']['temperatyre'][0] :   #'Очень жарко >30 градусов':
                        inputting.append([inputting.pop(),lambda x:x>=30])
                    elif inputting[-1]==displayed_words['command_1']['temperatyre'][1] :   #'Жарко от 20 до 30 градусов'
                        inputting.append([inputting.pop(),lambda x:20<=x<30])
                    elif inputting[-1]==displayed_words['command_1']['temperatyre'][2] :   #'Тепло от 10 до 20 градусов'
                        inputting.append([inputting.pop(),lambda x:10<=x<20])
                    elif inputting[-1]==displayed_words['command_1']['temperatyre'][3] :   #'Тепло от 10 до 20 градусов'
                        inputting.append([inputting.pop(),lambda x:0<=x<10])
                    elif inputting[-1]==displayed_words['command_1']['temperatyre'][4] :   #'Тепло от 10 до 20 градусов'
                        inputting.append([inputting.pop(),lambda x:-15<=x<0])
                    elif inputting[-1]==displayed_words['command_1']['temperatyre'][5] :   #'Тепло от 10 до 20 градусов'
                        inputting.append([inputting.pop(),lambda x:x<-15])
                    else:
                        inputting.append([inputting.pop(),lambda x:True])#Все равно


                    keyboard=types.ReplyKeyboardMarkup()
                    keyboard.add(*displayed_words['command_1']['wind'])
                    sender_ms(displayed_words['command_1']['answer'][4],keyboard)
                    step+=1
                else:
                    inputting.pop()
                    sender_ms(displayed_words['unknown_answer'])
            elif step==5:
                if inputting[-1] in displayed_words['command_1']['wind']:
                    if inputting[-1]==displayed_words['command_1']['wind'][0] :
                            inputting.append([inputting.pop(),lambda x:20<=x])
                    elif inputting[-1]==displayed_words['command_1']['wind'][1] :
                            inputting.append([inputting.pop(),lambda x:15<=x<20])
                    elif inputting[-1]==displayed_words['command_1']['wind'][2] :
                            inputting.append([inputting.pop(),lambda x:10<=x<15])
                    elif inputting[-1]==displayed_words['command_1']['wind'][3] :
                            inputting.append([inputting.pop(),lambda x:5<=x<10])
                    elif inputting[-1]==displayed_words['command_1']['wind'][4] :
                            inputting.append([inputting.pop(),lambda x:0<=x<5])
                    else:
                        inputting.append([inputting.pop(),lambda x:True])
                        
                    keyboard=types.ReplyKeyboardMarkup()
                    keyboard.add(*displayed_words['command_1']['rain'])
                    sender_ms(displayed_words['command_1']['answer'][5],keyboard)
                    step+=1
                else:
                    inputting.pop()
                    sender_ms(displayed_words['unknown_answer'])
            elif step==6:                     #step-1==len(displayed_words['command_1']['answer'])-1#последний ход комманды
                if inputting[-1] in displayed_words['command_1']['rain']:
                    if inputting[-1]==displayed_words['command_1']['rain'][0]:#'Есть дождь',
                        inputting.append([inputting.pop(),lambda x:bool(x)])
                    elif inputting[-1]==displayed_words['command_1']['rain'][1]:#'Нет дождя',
                        inputting.append([inputting.pop(),lambda x:not(bool(x))])
                    else:inputting.append([inputting.pop(),lambda x:True])
                    data_base[inputting[0]]={
                    'shown':{
                        'city_name':inputting[1]['city_name'],
                        'country':inputting[1]['country'],
                        'state':inputting[1]['state'],
                        'lat':inputting[2][0],
                        'lon':inputting[2][1],
                        'temperatyre':inputting[3][0],
                        'wind':inputting[4][0],
                        'rain':inputting[5][0]
                              },
                    'hidden':{
                        'temperatyre':inputting[3][1],
                        'wind':inputting[4][1],
                        'rain':inputting[5][1]
                             }
                    }
                    rewrite_data_base()  
                    sender_ms(displayed_words['command_1']['end'],stop())
                else:
                    inputting.pop()
                    sender_ms(displayed_words['unknown_answer'])
        elif number_cmd==2:#'Я хочу поехать ...'
            if step==0:
                if list(data_base.keys())==[]:
                    sender_ms('Список ваших поездок пуст.',stop())
                else:
                    keyboard=types.ReplyKeyboardMarkup()
                    keyboard.add(*list(data_base.keys()))
                    sender_ms(displayed_words['command_2']['answer'][0],keyboard)
                    inputting=[]
                    step+=1
            elif step==1:
                if len(inputting)!=0 and inputting[-1] in list(data_base.keys()):
                    list_date=[]
                    element_datebase=data_base[inputting[-1]]
                    weather_for_this_element_datebase=get_weather('get_weather_by_coords',[
                                                                   element_datebase['shown']['lat'],
                                                                   element_datebase['shown']['lon']])
                    ans='Когда вы можете поехать:\n\t'
                    for element_weather in weather_for_this_element_datebase:
                        if  element_datebase['hidden']['temperatyre'](element_weather['temperatyre']) and \
                            element_datebase['hidden']['wind'](element_weather['wind']) and \
                            element_datebase['hidden']['rain'](element_weather['rain']):
                            list_date.append(element_weather['time'].strftime('%Y-%m-%d %H:%M:%S'))                            
                                          #'Все равно'
                        
                    if list_date==[]:
                        sender_ms('Вы,к сожалению, никуда не сможете поехать',stop())
                    else:
                        sender_ms(ans+'\n\t'.join(list_date),stop())
                        
                    del element_datebase
                    del element_weather
                    del ans
                    del list_date

                
                else:
                    inputting=[]
                    keyboard=types.ReplyKeyboardMarkup()
                    keyboard.add(data_base.keys())
                    sender_ms(displayed_words['command_2']['answer'][1],keyboard)
        elif number_cmd==3:#куда я могу поехать
            if step==0:
                sender_ms('Введите дату в формате год-месяц-день,например:\n\t'+(datetime.datetime.today()+datetime.timedelta(hours=3)).strftime('%Y-%m-%d'))
                inputting=[]
                step+=1
            elif step==1:
                try:
                    if [data_base.keys()]==[]:
                        sender_ms('У вас нет поездок.',stop())
                    else:
                        find_date=datetime.datetime.strptime(inputting[-1],'%Y-%m-%d')
                        base_answers={}
                        text_answer='Вы можете поехать в ' + find_date.strftime('%Y-%m-%d')+':'
                        for element_of_database in data_base.keys():
                            weather_element_database=get_weather('get_weather_by_coords',[data_base[element_of_database]['shown']['lat'],data_base[element_of_database]['shown']['lon']])
                            base_answers[element_of_database]=[]
                            for weather_one_day_element_database in weather_element_database:
                                if  weather_one_day_element_database['time'].year==find_date.year and \
                                    weather_one_day_element_database['time'].month==find_date.month and \
                                    weather_one_day_element_database['time'].day==find_date.day:
                                        if  data_base[element_of_database]['hidden']['temperatyre'](weather_one_day_element_database['temperatyre']) and\
                                            data_base[element_of_database]['hidden']['wind'](weather_one_day_element_database['wind']) and \
                                            data_base[element_of_database]['hidden']['rain'](weather_one_day_element_database['rain']) :
                                                base_answers[element_of_database].append(weather_one_day_element_database['time'].strftime('%H:%M:%S'))
                    adding_number=False
                    for element_of_text_answers in base_answers.keys():
                        if base_answers[element_of_text_answers]==[]:
                            pass
                        else:
                            adding_number=True
                            text_answer+='\n\t'+element_of_text_answers+':'+'\n\t\t'.join(base_answers[element_of_text_answers])
                    if adding_number:
                        sender_ms(text_answer,stop())
                    else:
                        sender_ms('Вы никуда не сможете поехать в '+ find_date.strftime('%Y-%m-%d')+'.',stop())
                except:
                    sender_ms('Вы ввели не коректную дату.Попробуйте ввести еще раз.')
                    inputting=[]
        elif number_cmd==4:#'Показать все мои поездки.'
            if list(data_base.keys())==[]:
                sender_ms(displayed_words['command_3'][1],stop())
            else:
                sender_ms(displayed_words['command_3'][0]+'\n\t\t'+','.join(data_base.keys()),stop())
        elif number_cmd==5:#'Показать все мои поездки и их условия.'
            if list(data_base.keys())==[]:
                sender_ms(displayed_words['command_4'][1],stop())
            else:
                ans=displayed_words['command_4'][0]
                for element_of_database in data_base.keys():
                    ans+=element_of_database+':\nГород: '+data_base[element_of_database]['shown']['city_name']+ \
                        ',Страна:'+data_base[element_of_database]['shown']['country']+',Область: '+data_base[element_of_database]['shown']['state']+ \
                        ',Координаты: ('+ str(data_base[element_of_database]['shown']['lat'])+str(data_base[element_of_database]['shown']['lon'])+ \
                        '),Температура: ' +  data_base[element_of_database]['shown']['temperatyre'] + \
                        ',Ветер:'+ data_base[element_of_database]['shown']['wind'] +\
                        ',Дождь:'+data_base[element_of_database]['shown']['rain']+'.'
                sender_ms(ans,stop())
        elif number_cmd==6:#'Я хочу удалить поездку
            if step==0:
                if list(data_base.keys())==[]:
                    sender_ms('У вас нет поездок',stop())
                else:
                    keyboard=types.ReplyKeyboardMarkup()
                    keyboard.add(*list(data_base.keys()))
                    sender_ms('Какую поездку вы хотите удалить?',keyboard)
                    step+=1
            elif step==1:
                if inputting[-1] in list(data_base.keys()):
                    data_base.pop(inputting[-1],0)
                    rewrite_data_base()
                    sender_ms('Удаление прошло успешно',stop())
                else:
                    keyboard=types.ReplyKeyboardMarkup()
                    keyboard.add(*list(data_base.keys()))
                    sender_ms('У вас нет такой поездки',keyboard)
                    inputting=[]
    @bot.message_handler(func=lambda message:True)
    def format_no_processed(message):
        sender_ms('Этот формат,к сожалению, я не могу обработать')
    bot.polling(none_stop=True,interval=0)

if __name__=='__main__':
        read_data_base()
        get_weather=get_weather()
        work_bot()

