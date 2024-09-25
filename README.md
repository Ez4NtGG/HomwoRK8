# goit_python_web_hw_08
GoIT, Python WEB, Homework number 08. NoSQL. MongoDB.


### Перша частина
#### Вихідні дані

У нас є json файл з авторами та їх властивостями: дата та місце народження, короткий опис біографії.
Також ми маємо наступний json файл із цитатами від цих авторів.

#### Порядок виконання

  Створіть хмарну базу даних Atlas MongoDB
  За допомогою ODM Mongoengine створіть моделі для зберігання даних із цих файлів у колекціях authors та quotes.
  Під час зберігання цитат (quotes), поле автора в документі повинно бути не рядковим значенням, а [Reference fields](http://docs.mongoengine.org/guide/defining-documents.html?highlight=ReferenceField#reference -fields) полем, де зберігається ObjectID з колекції authors.
  - Напишіть скрипти для завантаження json файлів у хмарну базу даних.
  - Реалізуйте скрипт для пошуку цитат за тегом, за ім'ям автора або набором тегів. Скрипт виконується в нескінченному циклі і за допомогою звичайного оператора input приймає команди у наступному форматі команда: значення. Приклад:

    - name: Steve Martin — знайти та повернути список всіх цитат автора Steve Martin;
    - tag:life — знайти та повернути список цитат для тега life;
    - tags:life,live — знайти та повернути список цитат, де є теги life або live (примітка: без пробілів між тегами life, live);
    - exit — завершити виконання скрипту;

    Виведення результатів пошуку лише у форматі utf-8;

#### Додаткове завдання

Подумайте та реалізуйте для команд name:Steve Martin та tag:life можливість скороченого запису значень для пошуку, як name:st та tag:li відповідно;
Виконайте кешування результату виконання команд name: та tag: за допомогою Redis, щоб при повторному запиті результат пошуку брався не з MongoDB бази даних, а з кешу;

##### Підказка

    Для команд name:st та tag:li використовуйте регулярні вирази в String queries


### Друга частина

Напишіть два скрипти: consumer.py та producer.py. Використовуючи RabbitMQ, організуйте за допомогою черг імітацію розсилки email контактам.

Використовуючи ODM Mongoengine, створіть модель для контакту. Модель обов'язково повинна включати поля: повне ім'я, email та логічне поле, яке має значення False за замовчуванням. Воно означає, що повідомлення контакту не надіслано і має стати True, коли буде відправлено. Інші поля для інформаційного навантаження можете придумати самі.

Під час запуску скрипта producer.py він генерує певну кількість фейкових контактів та записує їх у базу даних. Потім поміщає у чергу RabbitMQ повідомлення, яке містить ObjectID створеного контакту, і так для всіх згенерованих контактів.

Скрипт consumer.py отримує з черги RabbitMQ повідомлення, обробляє його та імітує функцією-заглушкою надсилання повідомлення по email. Після надсилання повідомлення необхідно логічне поле для контакту встановити в True. Скрипт працює постійно в очікуванні повідомлень з RabbitMQ.

Заглушка може імітувати поведінку існуючого коду (наприклад, процедури на віддаленому комп'ютері) або бути тимчасовою заміною ще не створеного коду. Наприклад, замість функції, що виконує складні обчислення, можна тимчасово (доки не буде написана сама функція) поставити заглушку, що завжди повертає 1, і налагоджувати інші функції, що залежать від неї.

#### Додаткове завдання
Введіть у моделі додаткове поле телефонний номер. Також додайте поле, що відповідає за кращий спосіб надсилання повідомлень — SMS по телефону або email. Нехай producer.py відправляє у різні черги контакти для SMS та email. Створіть два скрипти consumer_sms.py та consumer_email.py, кожен з яких отримує свої контакти та обробляє їх.


### RESULT

#### SEED
```
src/main.py"
connect_db - ok
added authors id: 652425416f6a5cc787f5fbe0 (Albert Einstein)
added authors id: 652425416f6a5cc787f5fbe1 (Steve Martin)
added quotes id: 652425416f6a5cc787f5fbe2
added quote of quote.author Albert Einstein, author id [652425416f6a5cc787f5fbe0] = (Albert Einstein) 
added quotes id: 652425416f6a5cc787f5fbe3
added quote of quote.author Albert Einstein, author id [652425416f6a5cc787f5fbe0] = (Albert Einstein) 
added quotes id: 652425416f6a5cc787f5fbe4
added quote of quote.author Albert Einstein, author id [652425416f6a5cc787f5fbe0] = (Albert Einstein) 
added quotes id: 652425416f6a5cc787f5fbe5
added quote of quote.author Steve Martin, author id [652425416f6a5cc787f5fbe1] = (Steve Martin) 
```

#### SEARCH
```
/src/main.py"
connect_db - ok
Add authors...
100%|████████████████████████████████████████████████████████████████████████████████████████| 2/2 [00:00<00:00,  8.47it/s]
Add quotes...
100%|████████████████████████████████████████████████████████████████████████████████████████| 4/4 [00:00<00:00, 10.96it/s]
Add contacts: 100 ...
100%|████████████████████████████████████████████████████████████████████████████████████| 100/100 [00:03<00:00, 25.61it/s]
>>>help
List of commands: ('name', 'tag', 'help', 'exit'),  please to use ':' as argument separator
>>>name bert
command 'name bert' - unknown, can use 'help' for list of commands
>>>name:bert 
command 'name' - args: bert
[ 1 ] ----------------------------------------------------------------------------------------------------
{'author': 'Albert Einstein',
 'quote': '“The world as we have created it is a process of our thinking. It '
          'cannot be changed without changing our thinking.”',
 'tags': ['change', 'deep-thoughts', 'thinking', 'world']}
[ 2 ] ----------------------------------------------------------------------------------------------------
{'author': 'Albert Einstein',
 'quote': '“There are only two ways to live your life. One is as though '
          'nothing is a miracle. The other is as though everything is a '
          'miracle.”',
 'tags': ['inspirational', 'life', 'live', 'miracle', 'miracles']}
[ 3 ] ----------------------------------------------------------------------------------------------------
{'author': 'Albert Einstein',
 'quote': '“Try not to become a man of success. Rather become a man of value.”',
 'tags': ['adulthood', 'success', 'value']}
>>>name: mart
command 'name' - args: mart 
[ 1 ] ----------------------------------------------------------------------------------------------------
{'author': 'Steve Martin',
 'quote': '“A day without sunshine is like, you know, night.”',
 'tags': ['humor', 'obvious', 'simile']}
>>>tag: liv
command 'tag' - args: liv 
[ 1 ] ----------------------------------------------------------------------------------------------------
{'author': 'Albert Einstein',
 'quote': '“There are only two ways to live your life. One is as though '
          'nothing is a miracle. The other is as though everything is a '
          'miracle.”',
 'tags': ['inspirational', 'life', 'live', 'miracle', 'miracles']}
>>>tag: succ
command 'tag' - args: succ
[ 1 ] ----------------------------------------------------------------------------------------------------
{'author': 'Albert Einstein',
 'quote': '“Try not to become a man of success. Rather become a man of value.”',
 'tags': ['adulthood', 'success', 'value']}
>>>tag:     
for command 'tag' arguments is empty
>>>tag: ""
command 'tag' - args: ""
Not Found
>>>tag: xxxxx
command 'tag' - args: xxxxx
Not Found
>>>name: wwwwww
command 'name' - args: wwwwww
Not Found
>>>exit
command 'exit'
```

#### MULTIPLE not full TAGS
```
>>>tag:li,suc 
command 'tag' - args: li,suc 
[ 1 ] ----------------------------------------------------------------------------------------------------
{'author': 'Albert Einstein',
 'quote': '“There are only two ways to live your life. One is as though '
          'nothing is a miracle. The other is as though everything is a '
          'miracle.”',
 'tags': ['inspirational', 'life', 'live', 'miracle', 'miracles']}
[ 2 ] ----------------------------------------------------------------------------------------------------
{'author': 'Albert Einstein',
 'quote': '“Try not to become a man of success. Rather become a man of value.”',
 'tags': ['adulthood', 'success', 'value']}
```


#### UTF-8
```
>>>tag: live,марія                                                                                                          
command 'tag' - args: live,марія 
[ 1 ] ----------------------------------------------------------------------------------------------------
{'author': 'Albert Einstein',
 'quote': '“There are only two ways to live your life. One is as though '
          'nothing is a miracle. The other is as though everything is a '
          'miracle.”',
 'tags': ['inspirational', 'life', 'live', 'miracle', 'miracles']}
[ 2 ] ----------------------------------------------------------------------------------------------------
{'author': 'Steve Martin',
 'quote': '“A day without sunshine is like, you know, night.”',
 'tags': ['humor', 'obvious', 'simile', 'марія']}
>>>
```
#### REDIS CACHE

##### RUN REDIS DOCKER
scripts\docker_run_redis.cmd

```
command 'name' - args: albert
[ 1 ] ----------------------------------------------------------------------------------------------------
{'author': 'Albert Einstein',
 'quote': '“The world as we have created it is a process of our thinking. It '
          'cannot be changed without changing our thinking.”',
 'tags': ['change', 'deep-thoughts', 'thinking', 'world']}
[ 2 ] ----------------------------------------------------------------------------------------------------
{'author': 'Albert Einstein',
 'quote': '“There are only two ways to live your life. One is as though '
          'nothing is a miracle. The other is as though everything is a '
          'miracle.”',
 'tags': ['inspirational', 'life', 'live', 'miracle', 'miracles']}
[ 3 ] ----------------------------------------------------------------------------------------------------
{'author': 'Albert Einstein',
 'quote': '“Try not to become a man of success. Rather become a man of value.”',
 'tags': ['adulthood', 'success', 'value']}
Time execution: 0.02808839999488555
>>>name: albert
command 'name' - args: albert
[ 1 ] ----------------------------------------------------------------------------------------------------
{'author': 'Albert Einstein',
 'quote': '“The world as we have created it is a process of our thinking. It '
          'cannot be changed without changing our thinking.”',
 'tags': ['change', 'deep-thoughts', 'thinking', 'world']}
[ 2 ] ----------------------------------------------------------------------------------------------------
{'author': 'Albert Einstein',
 'quote': '“There are only two ways to live your life. One is as though '
          'nothing is a miracle. The other is as though everything is a '
          'miracle.”',
 'tags': ['inspirational', 'life', 'live', 'miracle', 'miracles']}
[ 3 ] ----------------------------------------------------------------------------------------------------
{'author': 'Albert Einstein',
 'quote': '“Try not to become a man of success. Rather become a man of value.”',
 'tags': ['adulthood', 'success', 'value']}
Time execution: 0.009065599966561422
>>>

```



### Частина 2

#### RabbitMQ

##### RUN RabbitMQ DOCKER
scripts\docker_run_rabbitmq.cmd

##### RUN task creater - producer
```
python tasks/producer.py
connect_db - ok
Add contacts: 100 ...
100%|████████████████████████████████████████████████████████████████████████████████████| 100/100 [00:04<00:00, 22.64it/s]
Sending '100' contacts ...
100%|██████████████████████████████████████████████████████████████████████████████████| 100/100 [00:00<00:00, 2941.10it/s] 
Sending '100' contacts ...
100%|██████████████████████████████████████████████████████████████████████████████████| 100/100 [00:00<00:00, 4831.20it/s]
```

##### RUN email sender - consumer #1

```
tasks/consumer.py

connect_db - ok
 [*] Waiting for messages. To exit press CTRL+C
 [x] Received id: 1
Name: Валерій Іваничук 
Sending email to: smyklarysa@example.com
 [x] Received id: 3
Name: Лілія Швачко 
Sending email to: varvara41@example.org
 [x] Received id: 5
Name: Тарас Царенко 
Sending email to: iukhym96@example.org
 [x] Received id: 7
Name: Веніямин Козак 
Sending email to: vadym17@example.com
 [x] Received id: 9
Name: Левко Копитко 
Sending email to: klavdiia81@example.net
....
 [x] Received id: 1
Task already done
 [x] Received id: 2
Task already done
 [x] Received id: 3
Task already done
 [x] Received id: 4
Task already done
 [x] Received id: 5


```

##### RUN email sender - consumer #2

```
tasks/consumer.py

connect_db - ok
 [*] Waiting for messages. To exit press CTRL+C
 [x] Received id: 2
Name: Ярина Наливайко 
Sending email to: zhuravelzynovii@example.com
 [x] Received id: 4
Name: Мілена Воблий 
Sending email to: zarudnyilukian@example.net
 [x] Received id: 6
Name: Аліна Шовкопляс 
Sending email to: vlokhklyment@example.org
 [x] Received id: 8
Name: Єлисавета Андрієвич 
Sending email to: liubovverhun@example.net
 [x] Received id: 10
Name: Омелян Бабариченко 
Sending email to: kostiantyn04@example.org
 [x] Received id: 12
Name: Трохим Юхименко 
Sending email to: romanetsoleksa@example.org
 [x] Received id: 14
Name: Едуард Пʼятаченко 
Sending email to: avreliibarannyk@example.org
 [x] Received id: 16
Name: Юстим Твердохліб 
Sending email to: ustym82@example.com
 [x] Received id: 18
Name: Єлисавета Харченко 
Sending email to: shvaikaoleksandr@example.net
....
 [x] Received id: 7
Task already done
 [x] Received id: 9
Task already done
 [x] Received id: 11
Task already done
 [x] Received id: 13
Task already done
 [x] Received id: 15
Task already done
 [x] Received id: 17
Task already done
 [x] Received id: 19
Task already done
 [x] Received id: 21
Task already done
 [x] Received id: 23
Task already done
 [x] Received id: 25
Task already done
 [x] Received id: 27
Task already done
 [x] Received id: 29
Task already done
 [x] Received id: 31
Task already done
```

#### RabbitMQ Monitor 
![RabbitMQ Monitor](doc/rabitmq_02.png) 


#### MongoDB records 
done = true
![MongoDB records](doc/mongo_01.png) 



### Додаткове
src\hw08\tasks\producer_sms.py
```
connect_db - ok
Add contacts: 5 ...
100%|█████████████████████████████████████████████████████████████████████████████████████████████| 5/5 [00:00<00:00, 17.79it/s]
Sending '5' contacts ...
100%|████████████████████████████████████████████████████████████████████████████████████████████| 5/5 [00:00<00:00, 324.81it/s] 
Sending '5' contacts ...
100%|█████████████████████████████████████████████████████████████████████████████████████████████████████| 5/5 [00:00<?, ?it/s] 
```
src\hw08\tasks\consumer_sms.py
```
connect_db - ok
 [*] Waiting for messages. To exit press CTRL+C
 [x] Received id: 1
prefer_type='type_sms'
Name: Устим Чекалюк 
Sending SMS to: 056 57 66
 [x] Received id: 2
prefer_type='type_sms'
Name: Соломон Мірошниченко 
Sending SMS to: +380 88 125 16 47
 [x] Received id: 3
prefer_type='type_sms'
Name: Станіслав Гоголь-Яновський 
Sending SMS to: 718-59-05
 [x] Received id: 4
prefer_type='type_sms'
Name: Тереза Дзюба 
Sending SMS to: +380 06 669 06 94
 [x] Received id: 5
prefer_type='type_sms'
Name: Христина Забарний 
Sending SMS to: 053 619 81 88
 [x] Received id: 1
prefer_type='type_sms'
Task already done
 [x] Received id: 2
prefer_type='type_sms'
Task already done
 [x] Received id: 3
prefer_type='type_sms'
Task already done
 [x] Received id: 4
prefer_type='type_sms'
Task already done
 [x] Received id: 5
prefer_type='type_sms'
Task already done

```

src\hw08\tasks\producer_email.py
```
connect_db - ok
Add contacts: 5 ...
100%|█████████████████████████████████████████████████████████████████████████████████████████████| 5/5 [00:00<00:00, 17.43it/s]
Sending '5' contacts ...
100%|████████████████████████████████████████████████████████████████████████████████████████████| 5/5 [00:00<00:00, 392.13it/s] 
Sending '5' contacts ...
100%|███████████████████████████████████████████████████████████████████████████████████████████| 5/5 [00:00<00:00, 2507.06it/s]
```

src\hw08\tasks\consumer_email.py
```
connect_db - ok
 [*] Waiting for messages. To exit press CTRL+C
 [x] Received id: 1
prefer_type='type_email'
Name: Тарас Шовкопляс 
Sending email to: olesmalyshko@example.org
 [x] Received id: 2
prefer_type='type_email'
Name: Юстим Андрієнко 
Sending email to: iaroslav38@example.org
 [x] Received id: 3
prefer_type='type_email'
Name: Віктор Ярема 
Sending email to: levko82@example.org
 [x] Received id: 4
prefer_type='type_email'
Name: Олекса Фартушняк 
Sending email to: irenakhrystenko@example.org
 [x] Received id: 5
prefer_type='type_email'
Name: Аркадій Каденюк 
Sending email to: khomashutko@example.com
 [x] Received id: 1
prefer_type='type_email'
Task already done
 [x] Received id: 2
prefer_type='type_email'
Task already done
 [x] Received id: 3
prefer_type='type_email'
Task already done
 [x] Received id: 4
prefer_type='type_email'
Task already done
 [x] Received id: 5
prefer_type='type_email'
Task already done

```

#### RabbitMQ Monitor SMS/EMAIL
![RabbitMQ Monitor sms/email](doc/rabitmq_03.png) 


#### DOCKER COMPOSE
![ DOCKER COMPOSE 1](doc/docker_01.png) 
![ DOCKER COMPOSE 2](doc/docker_02.png) 