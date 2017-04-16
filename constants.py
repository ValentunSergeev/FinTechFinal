from emoji import emojize

labels = {1: 'Акции', 2: 'Блокировка карты', 3: 'Вам звонили', 4: 'Вклад', 5: 'Действующий кредит',
          6: 'Денежные переводы', 7: 'Задолженность', 8: 'Интернет банк', 9: 'Карты', 10: 'Кредит',
          11: 'Кредитные карты', 12: 'Курс доллара', 13: 'Курс евро', 14: 'Курсы валют', 15: 'Мобильный банк',
          16: 'Не работает банкомат', 17: 'Обслуживание вкладов', 18: 'Обслуживание карт',
          19: 'Обслуживание кредитных карт',
          20: 'Открыте вклада', 21: 'Перевод на оператора', 22: 'Платежное поручение', 23: 'Получение карты',
          24: 'Получения кредита', 25: 'Пос терминал', 26: 'Претензии', 27: 'Приветствие', 28: 'Продажа кредитных карт',
          29: 'Процентные ставки', 30: 'Расчетно кассовое обслуживание', 31: 'Расчетный счет', 32: 'Реквизиты банка',
          33: 'Физические лица', 34: 'Эквайринг', 35: 'Юридические лица', 0: 'Адреса офисов и банкоматов'}
common_requests = {12: "Ткущий курс долара: 65 рублей. ", 13: "Текущий курс евро: 70 рублей. ",
                   "курс доллара": "Текущий курс долара: 65 рублей. ", "курс евро": "Текущий курс евро: 70 рублей. "}

non_fin_words = ['нет', 'да', 'хорошо', "ну это"]
cake = emojize(":cake:", use_aliases=True)

right_ans = ['да', "конечно", "ага", "угадал", "точно", "верно"]
wrong_ans = ['нет', 'никакая из этих тем не подходит', "неа", "не", "ошибаешься", "ошибка"]

# TODO CHANGE TIMES TO NORMAL
remind_time = 15
off_time = 30
