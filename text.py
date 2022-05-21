text = {
    # Изменить падеж имён получаемых из VK
    # nom — именительный
    # gen — родительный
    # dat — дательный
    # acc — винительный
    # ins — творительный
    # abl — предложный
    'vk_users_get_name_case': 'gen',

    # Если кто-то захочет воспользоваться командами бота без необходимых прав
    # {ds_user_name} — отображает имя профиль в Discord
    'embed_error_missing_any_role_title': 'Не хватает прав!',
    'embed_error_missing_any_role_description': 'Извини, {ds_user_name}, но у тебя не хватает прав использовать '
                                                'мой функционал. Я помогаю только админам и кураторам NotADub. '
                                                'Если ты один из них, а использовать команды не получается – '
                                                'напиши об этом Лидеру проекта. Уверена, она сможет помочь!',
    'embed_error_missing_any_role_image':
        'https://i.gifer.com/embedded/download/Wc9y.gif',

    # Если кто-то захочет побеспокоить человека или группу лиц в отпуске
    # {ds_users_names} — отображает список имён профилей в Discord
    'vacation_error_embed_title': 'Не беспокоить!',
    'vacation_error_embed_description': '{ds_users_names} сейчас находится в отпуске, поэтому беспокоить его мы не станем.',
    'vacation_error_embed_image': 'https://i.postimg.cc/B6bzXC61/940906557-preview-J78-RHq7.gif',

    # Если кто-то что-то такое сделает, что я не предусмотрел
    # {error} — покажет класс и значение ошибки, если есть дочерняя ошибка, то и её класс и значение
    'unknown_error_embed_title': 'Ой-ёй! Кажется, что-то сломалось...',
    'unknown_error_embed_description': 'В ходе выполнения кода случилось непредвиденное.\n'
                                       'Но не переживайте, все остальные команды я исполню как надо!'
                                       'Просто в этот раз пошло что-то не так. '
                                       'Если хотите чтобы меня починили, напишите моему '
                                       '[создателю](https://t.me/IlyaClutcher). В сообщении постарайтесь как можно '
                                       'подробнее описать когда и при каких условиях я поломалась.\n'
                                       'А ещё по возможности прикрепите файл `discord.log` к сообщению.\n'
                                       'Постараюсь вывести ошибку:\n'
                                       '{error}',
    'unknown_error_embed_image': 'https://i.postimg.cc/DzTJvCxB/SttF.gif',

    # help
    # Описание команды, которое появляется при наборе команды help
    'help_description': 'Покажу, какие команды я знаю!',
    # При обычном выполнении команды help высветиться это
    # {ds_user_name} — отображает имя профиль в Discord
    'help_embed_title': 'Хэйо, {ds_user_name}! Вот что я могу:',
    'help_embed_description': '`/help` – показывает список команд, которые я знаю\n'
                              '`/add_vk` – связывает профили Discord и ВКонтакте\n'
                              '`/remove_vk` – удаляет связку профилей Discord и ВКонтакте\n'
                              '`/list_vk` – показывает список связанных профилей Discord и ВКонтакте\n'
                              '`/ping` – отправляет сообщение указанным участникам в рабочку и/или личные сообщения '
                              'с указанием названия ветки или канала, а ещё с заметкой\n '
                              '`/remind` – создаёт одноразовое или многоразовое напоминание для указанного участника '
                              'или роли через определённый промежуток времени\n'
                              '`/cancel_reminds` – отменяет определённое или все напоминания\n'
                              '`/list_reminds` – показывает список напоминаний\n'
                              '`/vac` – отправляет в отпуск участника или роль до указанной даты\n'
                              '`/cancel_vac` – досрочно отменяет отпуск у участника или роли\n'
                              '`/list_vac` – показывает всех участников в отпуске',
    'help_embed_image': 'https://i.postimg.cc/DZdq3SLp/b6b7a6e4d6254ece95075d77c3534f712ba1e6c5r1-540-304-hq.gif',

    # add_vk
    # Описание команды и её параметров, которые появляются при наборе команды add_vk
    'add_vk_description': 'Связать профили Discord и ВКонтакте',
    'add_vk_describe_ds_user': 'Введи логин участника в Discord',
    'add_vk_describe_vk_id': 'Введи ID странички участника ВКонтакте (то, что в ссылке после https://vk.com/)',

    # В каком падеже будут указаны имя и фамилия пользователя ВК
    'add_vk_users_get_name_case': 'gen',

    # При обычном выполнении команды add_vk высветиться это
    # {vk_user_name} — отображает имя в указанном падеже со страницы в ВК
    # {ds_user_name} — отображает имя профиль в Discord
    'add_vk_embed_title': 'Ура, профили успешно связаны!',
    'add_vk_embed_description': 'Профиль {vk_user_name} из ВКонтакте был успешно связан с профилем {ds_user_name} из '
                                'Discord. Теперь участник будет получать уведомления!',
    'add_vk_embed_image': 'https://i.postimg.cc/Fs0C1j8W/6712e821f2505f8377a9803c7c491c33d12df527r1-538-302-hq.gif',

    # Если при выполнении add_vk возникнет ошибка, что один из указанных ID фигурирует в базе данных
    'add_vk_embed_error_unique_violation_title': 'Хм... Кажется, мы уже знакомы.',
    'add_vk_embed_error_unique_violation_description': 'Один из введённых профилей уже фигурирует в базе данных.\n'
                                                       'Для того, чтобы проверить существующие записи, используй команду `/list_vk`.',
    'add_vk_embed_error_unique_violation_image':
        'https://i.postimg.cc/xCnypvhF/animation-avatar-anime-pixelbox-ru-34.gif',

    # Если при выполнении add_vk возникнет ошибка, что пользователь не будет найден по указанному VK ID
    # {vk_id} - будет отображать значение VK ID, которое было введено при вызове команды
    'add_vk_embed_error_index_error_title': 'Пользователь VK с ID = "{vk_id}" не найден.',
    'add_vk_embed_error_index_error_description': 'Если возникают сложности с получением правильного ID, '
                                                  'то можно использовать этот [сайт](https://regvk.com/id/).',
    'add_vk_embed_error_index_error_image': 'https://betterstudio.com/wp-content/uploads/2019/12/GIF-in-WordPress.gif',

    # Если при выполнении add_vk возникнет ошибка, что пользователь будет найден, но ему нельзя будет написать
    # {vk_user_name} — отображает имя в указанном падеже со страницы в ВК
    # {ds_user_name} — отображает имя профиль в Discord
    'add_vk_embed_error_VKAPIError_901_title': 'Профили связаны, но есть одно "но"...',
    'add_vk_embed_error_VKAPIError_901_description': 'Профиль {vk_user_name} из ВКонтакте был успешно связан с профилем '
                                                     '{ds_user_name} из Discord.\nНо паблик не может отправлять этому '
                                                     'участнику личные сообщения ВКонтакте, так как он не разрешил ему писать. '
                                                     'Попроси участника написать в сообщения паблика или разрешить сообщения от него. '
                                                     'Я бы очень хотела подружиться!',
    'add_vk_embed_error_VKAPIError_901_image': 'https://i.postimg.cc/sXCm5d3S/zsPkEF.gif',

    # remove_vk
    # list_vk

    # ping
    # Описание команды и её параметров, которые появляются при наборе команды ping
    'ping_description': 'Отправлю уведомление участнику или роли в рабочку или личные сообщения ВКонтакте.',
    'ping_describe_target': 'Отметь участника или роль, кому нужно отправить уведомление',
    'ping_describe_choice': 'Выбери, куда именно нужно отправить уведомление',
    'ping_describe_note': 'Напиши заметку (если нужно), которую нужно отправить вместе с уведомлением',

    # При обычном выполнении команды ping высветиться это
    # {ds_users_names}
    'ping_embed_title': 'Уведомление отправлено!',
    'ping_embed_description': 'В ближайшую минуту упомяну следующих участников:{ds_users_names}',
    'ping_embed_image': 'https://i.postimg.cc/3Jwq8v9v/8Lnq.gif',



    # Если при выполнении ping бот не сможет кому-то написать в личные сообщения кому-то, но в целом он выполнит
    # пинг, то высветится это
    'ping_embed_error_not_full_title': 'Уведомление отправлено! Но есть одно "но"...',
    'ping_embed_error_not_full_description': 'В ближайшую минуту отправлю уведомление, но упомянуты будут не все участники, '
                                             'поскольку не у всех из них связаны профили Discord и ВКонтакте. Вот кого я упомяну:{ds_users_names}',
                                             'ping_embed_error_not_full_image': 'https://i.postimg.cc/Gtt42KHN/anime-hug-14.gif',

    # Если при выполнении ping возникнет ошибка, что пользователи будут найдены, но им нельзя будет написать
    # {linked_accounts_names} — отображает имена связанных аккаунтов
    'ping_embed_error_VKAPIError_901_title': 'Не могу отправить уведомление!',
    'ping_embed_error_VKAPIError_901_description': 'Ну и ну... Кажется, указанные вами пользователи не хотят со мной дружить. '
                                                   'Я не могу отправить им уведомление, потому что мы никогда не общались или '
                                                   'они запретили паблику им писать. Ещё может быть, что профили Discord и ВКонтакте '
                                                   'для указанных участников не связаны. Скорее подружи нас!\n'
                                                   '{linked_accounts_names}',
    'ping_embed_error_VKAPIError_901_image': 'https://i.postimg.cc/Dz7jN4W0/223eed3b4be6395d204cae93a9814a803c7898b3-hq.gif',

    # Сообщение в VK, которое будет отправлено в беседу
    # {users_names} — список имён, которые были выбраны целью пинга
    # {channel} — имя канала и ветки, если вызов из неё, откуда происходит пинг
    # {note} — необязательная заметка к пингу (Лучше всего не трогать и оставлять в конце текста, так как он добавить
    # слово "Заметка:" с новой строки и ещё следом уже с другой строки саму заметку)
    'ping_vk_group_chat_message': 'Тук-тук! Пришло уведомление из Discord для {ds_users_names}\nУпоминание было оставлено в канале {channel}{note}',

    # Сообщение в VK, которое будет отправлено лично пользователю
    # {vk_user_name} — имя будет взято со страницы VK в именительном падеже, которой мы пишем
    # {channel} — имя канала и ветки, если вызов из неё, откуда происходит пинг
    # {note} — необязательная заметка к пингу (Лучше всего не трогать и оставлять в конце текста, так как он добавить
    # слово "Заметка:" с новой строки и ещё следом уже с другой строки саму заметку)
    'ping_vk_direct_message': 'Хэйо, {vk_user_name}! Куратор или админ упомянули тебя в Discord.\nОни ждут твоего ответа в канале {channel}{note}',

    # remove_vk
    # Описание команды и её параметров, которые появляются при наборе команды remove_vk
    'remove_vk_description': 'Удалить связь профилей Discord и ВКонтакте',
    'remove_vk_describe_target': 'Укажи логин пользователя в Discord, чью связь профилей необходимо разорвать',

    # При обычном выполнении команды remove_vk высветиться это
    'remove_vk_embed_title': 'Связь удалена.',
    'remove_vk_embed_description': 'Теперь Discord-профиль {ds_user_name} больше не связан с ВК-профилем {vk_user_name}.',
    'remove_vk_embed_image': 'https://i.postimg.cc/JhsbH8tr/RYA8.gif',

    'remove_vk_direct_message': 'Привет! Связь твоего Discord-профиля {ds_user_name} с профилем ВКонтакте разорвана.',

    # Если при попытке удаления, бот не найдёт связи
    'remove_vk_embed_error_nothing_to_delete_title': 'Не могу удалить!',
    'remove_vk_embed_error_nothing_to_delete_description': 'Discord-профиль {ds_user_name} не связан с '
                                                           'каким-либо ВК-профилем.',
    'remove_vk_embed_error_nothing_to_delete_image': 'https://i.postimg.cc/156Rtjyk/63e6701467f741323cb63bacb1b75615f760e327r1-500-281-hq.gif',

    # list_vk
    # Описание команды и её параметров, которые появляются при наборе команды list_vk
    'list_vk_description': 'Показать список связанных профилей',

    # При обычном выполнении команды list_vk высветиться это
    'list_vk_embed_title': 'Вот список моих друзей:',
    'list_vk_embed_description': '{links}',
    'list_vk_embed_image': 'https://i.postimg.cc/k52pJkm8/102151.gif',

    # Если не будет связанных аккаунтов
    'list_vk_embed_error_nothing_in_list_title': 'Со мной никто не дружит...',
    'list_vk_embed_error_nothing_in_list_description': 'Ещё ни один участник не подружился со мной. Пожалуйста, свяжи их профили Discord и ВКонтакте вместе!',
    'list_vk_embed_error_nothing_in_list_image': 'https://i.postimg.cc/26FFrwVh/1513639100-ezgif-com-gif-maker-2.gif',

    # vac
    # Описание команды и её параметров, которые появляются при наборе команды vac
    'vac_description': 'Отправить кого-то в отпуск',
    'vac_describe_target': 'Укажи пользователя, которого нужно отправить в отпуск',
    'vac_describe_date': 'Введи конечную дату отпуска в формате ДД.ММ.ГГГГ',
    'vac_describe_note': 'Напиши примечание, например, причину отпуска (больничный, отпуск и тд.)',

    # При обычном выполнении команды vac высветиться это
    'vac_embed_title': 'Наконец-то отдых!',
    'vac_embed_description': 'Я отправила {ds_users_names} в отпуск до {vacation_period}{note}',
    'vac_embed_image': 'https://i.postimg.cc/9f1Q2wcz/1640588339-anime-sleep-45.gif',

    # Если и так уже в отпуске
    'vac_embed_error_vac_already_title': 'Кто в отпуске, ещё больше отпускничать не может!',
    'vac_embed_vac_already_description': 'Вообще-то {ds_users_names} и так уже в отпуске. Куда уж больше отдыхать?',
    'vac_embed_vac_already_image': 'https://c.tenor.com/cJ6FH3ZxcVoAAAAC/nico-nico-yazawa.gif',

    # Если указана некорректная дата
    'vac_embed_error_vacation_period_title': 'Кажется, в дате есть ошибка...',
    'vac_embed_error_vacation_period_description': 'Посмотри, сейчас дата в неправильном формате: {vacation_period}\n'
                                                   'Используйте формат ДД.ММ.ГГГГ. К примеру:\n'
                                                   '10.12.2077\n'
                                                   '10.05.2078\n'
                                                   'Следующие варианты форматов дат не подходят:\n'
                                                   '32.06.2023\n'
                                                   '31.02.2024\n'
                                                   '18.12.23\n'
                                                   '18.12.1990',
    'vac_embed_error_vacation_period_image': 'https://c.tenor.com/0fnE4qq8hAYAAAAC/time-dance-anime.gif',

    # list_vac
    # Описание команды и её параметров, которые появляются при наборе команды list_vac
    'list_vac_description': 'Показать список участников, находящихся в отпуске',

    # При обычном выполнении команды list_vac высветиться это
    'list_vac_embed_title': 'Вот кто сейчас отдыхает:',
    'list_vac_embed_description': '{data}',
    'list_vac_embed_image': 'https://c.tenor.com/PK-VJhoxC8MAAAAC/party-time-anime.gif',

    # При обычном выполнении команды list_vac высветиться это
    'list_vac_embed_error_nobody_rest_title': 'Ничего себе, никого в отпуске нет!',
    'list_vac_embed_error_nobody_rest_description': 'Как приятно, когда все друзья заняты делами в команде.',
    'list_vac_embed_error_nobody_rest_image': 'https://i.postimg.cc/66hqLPkC/animesher-com-anime-girl-gif-cute-anime-gif-anime-gif-995337.gif',

    # cancel_vac
    # Описание команды и её параметров, которые появляются при наборе команды cancel_vac
    'cancel_vac_description': 'Вывести участника из отпуска досрочно',
    'cancel_vac_describe_target': 'Кому будем отменять отпуск?',

    # При обычном выполнении команды cancel_vac высветиться это
    'cancel_vac_embed_title': 'Пора за работу!',
    'cancel_vac_embed_description': 'Отпуск {ds_users_names} завершён досрочно.',
    'cancel_vac_embed_image': 'https://i.postimg.cc/BbbrFXWY/36224.gif',

    # Если человек или группа людей и так не отпуске.
    'cancel_vac_embed_error_no_vac_title': 'Кто работает, ещё больше работать не может!',
    'cancel_vac_embed_error_no_vac_description': '{ds_users_names} и так не в отпуске.',
    'cancel_vac_embed_error_no_vac_image': 'https://i.postimg.cc/8ck6mgwn/hmpf-anime.gif',

    # remind
    # Описание команды и её параметров, которые появляются при наборе команды remind
    'remind_description': 'Завести напоминалку',
    'remind_describe_target': 'Укажи участника или роль, для кого нужно поставить напоминалку',
    'remind_describe_repeat': 'Напоминалка будет разовой или повторяться?',
    'remind_describe_next_time': 'Через какой промежуток времени напомнить? Укажи в формате: 1н(еделя) 1д(ень) 1ч(ас) 1м(инута)',
    'remind_describe_note': 'Что указать в заметке к напоминалке?',

    # При обычном выполнении команды remind высветиться это
    'remind_embed_title': 'Напоминалку запомнила!',
    'remind_embed_description': 'Напомню {repeat} {ds_users_names} через {raw_time_delta}, то есть в следующий раз это '
                                'будет {next_time}, а к напоминанию напишу это:\n{note}',
    'remind_embed_title_image': 'https://i.postimg.cc/8Cw6Z2Sx/Disastrous-Weak-Fugu-size-restricted.gif',

    # Если будут введены неправильно данные, скорее всего время следующего напоминания
    'remind_embed_error_value_title': 'Что-то ты напутал...',
    'remind_embed_error_value_description': 'Скорее всего, неправильно введено время:\n{raw_time_delta}\n'
                                            'Формат ввода времени:\n'
                                            '1н 1д 1ч 1м\n'
                                            'Программа поймёт это как через одну неделю, через один, через один час и'
                                            'через одну минуту.',
    'remind_embed_error_value_title_image': 'https://i.postimg.cc/W3d3NpWV/9438a17709f43462c0749bbae32a4a2c.gif',

    # list_reminds
    # Описание команды и её параметров, которые появляются при наборе команды list_reminds
    'list_reminds_description': 'Показать список действующих напоминалок',

    # При обычном выполнении команды list_reminds будет это
    'list_reminds_embed_title': 'ID напоминания: {remind_id}',
    'list_reminds_embed_description': 'Кто поставил: {ds_user_name}\n'
                                      'Повторяется: {repeat}\n'
                                      'Куда отправляется: {channel_name}\n'
                                      'Через какой промежуток времени: {timedelta}\n'
                                      'Следующие напоминание будет: {next_time}\n'
                                      'Заметка:\n{note}',
    'list_reminds_embed_image': 'https://i.postimg.cc/DZL9dtms/original.gif',

    # Если нет уведомлений
    'list_reminds_embed_error_no_reminds_title': 'Как так? Нет ни одной напоминалки.',
    'list_reminds_embed_no_reminds_description': 'Давай поставим новые, а не то все всё забудут!',
    'list_reminds_embed_no_reminds_image': 'https://i.postimg.cc/Ssdrhrv3/adorable-boy-couple-eyes-blue-Favim-com-1744037.gif',

    # cancel_reminds
    # Описание команды и её параметров, которые появляются при наборе команды list_reminds
    'cancel_reminds_description': 'Удалить указанную напоминалку',
    'cancel_reminds_describe_remind_id': 'ID напоминалки, которую нужно удалить',

    # При обычном выполнении команды cancel_reminds будет это
    'cancel_reminds_embed_title': 'Напоминание удалено!',
    'cancel_reminds_embed_description': 'ID напоминалки: {remind_id}\n'
                                        'Кто поставил: {ds_user_name}\n'
                                        'Повторялось ли: {repeat}\n'
                                        'Куда отправлялось: {channel_name}\n'
                                        'Через какое время напомнило бы: {timedelta}\n'
                                        'Следующие напоминание было бы: {next_time}\n'
                                        'Заметка:\n{note}',
    'cancel_reminds_embed_image': 'https://i.postimg.cc/Px1qpVjV/orig.gif',

    # Если нет уведомления по указанному ID
    'cancel_reminds_embed_error_no_reminds_title': 'Такого напоминания не существует.',
    'cancel_reminds_reminds_embed_no_reminds_description': 'Напоминания с ID = {remind_id} нет, поэтому удалить его не выйдет.',
    'cancel_reminds_reminds_embed_no_reminds_image': 'https://i.postimg.cc/gjPH876x/8TJR.gif',

    # Когда заканчивается отпуск
    'vac_end_embed_title': 'Ура, отпуск закончился!',
    'vac_end_embed_description': 'Отпуск подошёл к концу. Надеюсь, удалось хорошенько отдохнуть!',
    'vac_end_embed_image': 'https://i.pinimg.com/originals/f2/d0/77/f2d077b444d836310f84d553830a7fd3.gif',

    # Когда пришло время одноразового напоминания
    'remind0_embed_title': 'Пришла напомнить кое-что!',
    'remind0_end_embed_description': '{note}',
    'remind0_end_embed_image': 'https://i.postimg.cc/Rhky6mc2/GIF-17.gif',

    # Когда пришло время повторяющегося напоминания
    'remind1_embed_title': 'Очередная напоминалка!',
    'remind1_end_embed_description': 'ID напоминалки: {remind_id}\n'
                                     'В следующий раз приду: {next_time}\n'
                                     'Заметка:\n{note}',
    'remind1_end_embed_image': 'https://i.postimg.cc/Rhky6mc2/GIF-17.gif',



    # ping
    'ping_embed_confirm_form_title': 'Не многовато ли людей?',
    'ping_embed_confirm_form_description': 'Я, конечно, не против позвать их всех сюда, но ты точно уверен, '
                                           'что нужно отправить уведомление такому количеству участников '
                                           '(целых {total}) {where}:'
                                           '\n{list_users}',
    'ping_embed_confirm_form_image': 'https://i.postimg.cc/gkpfWz26/cbb5d5a3ebd65f3d25f92bde9c4e5bb9.gif',

    # {ds_users_names}
    'ping_embed_error_no_targets_title': 'И кого тут пинговать?',
    'ping_embed_error_no_targets_description': 'Не смогла найти целей для пинга.',
    'ping_embed_error_no_targets_image': 'https://i.postimg.cc/XNt9GqCp/2c9d6b20b950d667a3b93d60207f8314.gif',
}
