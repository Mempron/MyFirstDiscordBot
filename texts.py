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
                                                'команды этого бота. Только кураторы и лидеры отделов могут '
                                                'использовать этого бота для своих задач.',
    'embed_error_missing_any_role_image':
        'https://i.pinimg.com/originals/04/0d/ba/040dba1669a82ba41bf87383cbe8d3b8.gif',

    # Если кто-то захочет побеспокоить человека или группу лиц в отпуске
    # {ds_users_names} — отображает список имён профилей в Discord
    'vacation_error_embed_title': 'Не беспокоить!',
    'vacation_error_embed_description': 'Не стоит беспокоить {ds_users_names}, всем нам хоть иногда да надо отдыхать.',
    'vacation_error_embed_image': 'https://i.imgur.com/KVAFGdh.gif',

    # Если кто-то что-то такое сделает, что я не предусмотрел
    # {error} — покажет класс и значение ошибки, если есть дочерняя ошибка, то и её класс и значение
    'unknown_error_embed_title': 'Поздравляю, вы меня сломали.',
    'unknown_error_embed_description': 'В ходе выполнения кода случилось непредвиденное.\n'
                                       'Произошла ошибка, которую мой создатель не предвидел. '
                                       'Если хотите, чтобы меня починили, то напишите моему '
                                       '[создателю](https://t.me/IlyaClutcher).'
                                       'Но не переживайте, бот должен и дальше работать без проблем.'
                                       'Просто в этот раз пошло что-то не так. В сообщении постарайтесь как можно '
                                       'подробнее описать когда и при каких условиях это произошло.\n'
                                       'А ещё если можете, то прикрепить файл `discord.log` к сообщению.\n'
                                       'Постараюсь вывести ошибку:\n'
                                       '{error}',
    'unknown_error_embed_image': 'https://c.tenor.com/NFlo735HwGsAAAAC/kaneki.gif',

    # help
    # Описание команды, которое появляется при наборе команды help
    'help_description': 'Показывает что может этот бот',
    # При обычном выполнении команды help высветиться это
    # {ds_user_name} — отображает имя профиль в Discord
    'help_embed_title': 'Привет, {ds_user_name}! Вот что я могу:',
    'help_embed_description': '`/help` — показывает это сообщение\n'
                              '`/add_vk` — связать Discord и VK\n'
                              '`/remove_vk` — удалить связь Discord и VK\n'
                              '`/list_vk` — показать все связанные аккаунты Discord и VK\n'
                              '`/ping` — отправляет сообщение всем адресатам в беседу и личные сообщения '
                              '(если подключено) с указанием ветки или канала и заметкой\n '
                              '`/remind` — создаёт одноразовое или многоразовое напоминание для указанного участника '
                              'или роли через определённый промежуток времени\n'
                              '`/cancel_reminds` — отменяет какое-то определенно упоминание или все напоминания\n'
                              '`/list_reminds` — показывает список напоминаний\n'
                              '`/vac` — отправляет в отпуск указанного участника или роль до определенного дня\n'
                              '`/unvac` — отменяет отпуск у указанного участника или роли\n'
                              '`/list_vacs` — показывает всех участников в отпуске',
    'help_embed_image': 'http://pa1.narvii.com/7465/5971590fdfc35200ad481434689dffb4aa9110fer1-360-240_00.gif',
    'help_embed_url': 'https://www.youtube.com/c/NotADub',

    # add_vk
    # Описание команды и её параметров, которые появляются при наборе команды add_vk
    'add_vk_description': 'Связать аккаунт из Discord и VK',
    'add_vk_describe_ds_user': 'Аккаунт из Discord',
    'add_vk_describe_vk_id': 'ID VK (либо цифровой ID, либо то, что после / в ссылке)',

    # При обычном выполнении команды add_vk высветиться это
    # {vk_user_name} — отображает имя в указанном падеже со страницы в ВК
    # {ds_user_name} — отображает имя профиль в Discord
    'add_vk_embed_title': 'Всё супер! И даже нюансов нет!',
    'add_vk_embed_description': 'Профиль {vk_user_name} из VK был успешно связан с профилем {ds_user_name} из '
                                'Discord.',
    'add_vk_embed_image': 'https://pa1.narvii.com/6610/23abdb3aa713c424d4bf7d08e240e1b501934ae6_hq.gif',

    # Если при выполнении add_vk возникнет ошибка, что один из указанных ID фигурирует в базе данных
    'add_vk_embed_error_unique_violation_title': 'Ошибка! Запись о таком пользователе уже есть в базе данных.',
    'add_vk_embed_error_unique_violation_description': 'Один из введённых вами ID уже фигурирует в базе данных.\n'
                                                       'Чтобы посмотреть связанные аккаунты используйте `/list_vk`.',
    'add_vk_embed_error_unique_violation_image':
        'http://pa1.narvii.com/6743/a26443300851ca079d40adb26b03ddb0f4e72484_00.gif',

    # Если при выполнении add_vk возникнет ошибка, что пользователь не будет найден по указанному VK ID
    # {vk_id} - будет отображать значение VK ID, которое было введено при вызове команды
    'add_vk_embed_error_index_error_title': 'Пользователь VK с ID = "{vk_id}" не найден.',
    'add_vk_embed_error_index_error_description': 'Если возникают сложности с получением правильного ID, '
                                                  'то можно использовать этот [сайт](https://regvk.com/id/).',
    'add_vk_embed_error_index_error_image': 'https://betterstudio.com/wp-content/uploads/2019/12/GIF-in-WordPress.gif',

    # Если при выполнении add_vk возникнет ошибка, что пользователь будет найден, но ему нельзя будет написать
    # {vk_user_name} — отображает имя в указанном падеже со страницы в ВК
    # {ds_user_name} — отображает имя профиль в Discord
    'add_vk_embed_error_VKAPIError_901_title': 'Всё супер! Но есть один нюанс...',
    'add_vk_embed_error_VKAPIError_901_description': 'Теперь VK аккаунт {vk_user_name} связан с Discord аккаунтом '
                                                     '{ds_user_name}.\nНо сообщество не может отправлять сообщения '
                                                     'этому пользователю в VK, так как он ему либо ни разу не писал, '
                                                     'либо заблокировал его.\nНаписать сообществу можно по этой '
                                                     '[ссылке](https://vk.com/im?sel=-168930791).',
    'add_vk_embed_error_VKAPIError_901_image': 'https://i.imgur.com/1dEA5bZ.gif',

    # remove_vk
    # list_vk

    # ping
    # Описание команды и её параметров, которые появляются при наборе команды ping
    'ping_description': 'Отправляет пинги в ВК, в беседу и личные сообщения',
    'ping_describe_target': 'Цель для пинга,её могут быть участник или роль',
    'ping_describe_note': 'Заметка к пингу по желанию',

    # При обычном выполнении команды ping высветиться это
    # {ds_users_names}
    'ping_embed_title': 'Пинги отправлены!',
    'ping_embed_description': 'В ближайшую минуту пинг будет отправлен в беседу, в котором будут упомянуты '
                              '{ds_users_names}. И если у них привязан VK к Discord, то и в личные сообщения.',
    'ping_embed_image': 'https://www.icegif.com/wp-content/uploads/icegif-2013.gif',

    # Если при выполнении ping бот не сможет кому-то написать в личные сообщения кому-то, но в целом он выполнит
    # пинг, то высветится это
    'ping_embed_error_not_full_title': 'Пинги отправлены! Но есть нюанс...',
    'ping_embed_error_not_full_description': 'В ближайшую минуту пинг будет отправлен в беседу, в котором будут '
                                             'упомянуты {ds_users_names}. И если у них привязан VK к Discord, то и в '
                                             'личные сообщения. Но кому-то написать из списка не удастся, так как'
                                             'он не дал разрешения сообществу на отправку ему сообщений.',
    'ping_embed_error_not_full_image': 'https://www.icegif.com/wp-content/uploads/icegif-2013.gif',

    # Если при выполнении ping возникнет ошибка, что пользователи будут найдены, но им нельзя будет написать
    # {linked_accounts_names} — отображает имена связанных аккаунтов
    'ping_embed_error_VKAPIError_901_title': 'Не могу отправить пинг!',
    'ping_embed_error_VKAPIError_901_description': 'Ниже представлен список аккаунтов, которым сообщество не может '
                                                   'писать, так как нет разрешения. Люди из этого списка должны '
                                                   'написать сообществу, это можно сделать по этой '
                                                   '[ссылке](https://vk.com/im?sel=-168930791).'
                                                   '{linked_accounts_names}',
    'ping_embed_error_VKAPIError_901_image': 'https://c.tenor.com/rnhV3fu39f8AAAAC/eating-anime.gif',

    # Сообщение в VK, которое будет отправлено в беседу
    # {users_names} — список имён, которые были выбраны целью пинга
    # {channel} — имя канала и ветки, если вызов из неё, откуда происходит пинг
    # {note} — необязательная заметка к пингу (Лучше всего не трогать и оставлять в конце текста, так как он добавить
    # слово "Заметка:" с новой строки и ещё следом уже с другой строки саму заметку)
    'ping_vk_group_chat_message': 'Внимание, {ds_users_names}! Новое уведомление!\nОткуда: {channel}{note}',

    # Сообщение в VK, которое будет отправлено лично пользователю
    # {vk_user_name} — имя будет взято со страницы VK в именительном падеже, которой мы пишем
    # {channel} — имя канала и ветки, если вызов из неё, откуда происходит пинг
    # {note} — необязательная заметка к пингу (Лучше всего не трогать и оставлять в конце текста, так как он добавить
    # слово "Заметка:" с новой строки и ещё следом уже с другой строки саму заметку)
    'ping_vk_direct_message': 'Привет, {vk_user_name}! Новое уведомление!\nОткуда: {channel}{note}',

    # remove_vk
    # Описание команды и её параметров, которые появляются при наборе команды remove_vk
    'remove_vk_description': 'Удалить связь Discord и VK',
    'remove_vk_describe_target': 'Discord аккаунт для которого хотите удалить связь',

    # При обычном выполнении команды ping высветиться это
    'remove_vk_embed_title': 'Связь удалена.',
    'remove_vk_embed_description': 'Теперь Discord аккаунт {ds_user_name} больше не связан с аккаунтом {vk_user_name}.',
    'remove_vk_embed_image': 'https://c.tenor.com/gMU9WdWa4YIAAAAM/d4dj-d4dj-meme.gif',

    'remove_vk_direct_message': 'Привет. Мы отвязали Discord аккаунт {ds_user_name} от твоего профиля.',

    # Если при попытке удаления, бот не найдёт связи
    'remove_vk_embed_error_nothing_to_delete_title': 'Не могу удалить!',
    'remove_vk_embed_error_nothing_to_delete_description': 'У пользователя {ds_user_name} нет связи с '
                                                           'каким-либо аккаунтом в VK',
    'remove_vk_embed_error_nothing_to_delete_image': 'https://img.wattpad.com/'
                                                     'b993b8d34ea984ada23a0ed90c0070e7178ca65b/68747470733a2f2f73332e61'
                                                     '6d617a6f6e6177732e636f6d2f776174747061642d6d656469612d73657276696'
                                                     '3652f53746f7279496d6167652f6753524c46505f71637552634f673d3d2d3431'
                                                     '373734303031342e3134643539653232366239393963313939353035303431353'
                                                     '53030352e676966',

    # list_vk
    # Описание команды и её параметров, которые появляются при наборе команды list_vk
    'list_vk_description': 'Покажет все связанные аккаунты',

    # При обычном выполнении команды list_vk высветиться это
    'list_vk_embed_title': 'Вот список:',
    'list_vk_embed_description': '{links}',
    'list_vk_embed_image': 'https://c.tenor.com/KkSu1C4AW-oAAAAd/anime-loli.gif',

    # Если не будет связанных аккаунтов
    'list_vk_embed_error_nothing_in_list_title': 'Пусто',
    'list_vk_embed_error_nothing_in_list_description': 'Нет связанных аккаунтов. Пора бы что-то связать...',
    'list_vk_embed_error_nothing_in_list_image': 'https://c.tenor.com/CX9MHjS4uZkAAAAC/kanna-kamui-eat.gif',

    # vac
    # Описание команды и её параметров, которые появляются при наборе команды vac
    'vac_description': 'Отправить кого-то в отпуск',
    'vac_describe_target': 'Роль или пользователь, кого хотите отправить в отпуск',
    'vac_describe_date': 'Отпуск до дд.мм.год',
    'vac_describe_note': 'Причина (необязательно указывать)',

    # При обычном выполнении команды vac высветиться это
    'vac_embed_title': 'Теперь можно и отдохнуть!',
    'vac_embed_description': 'Теперь {ds_users_names} в отпуске до {vacation_period}{note}',
    'vac_embed_image': 'https://i.pinimg.com/originals/e4/98/96/e4989643374e2dfae38c643f3fb941a3.gif',

    # Если и так уже в отпуске
    'vac_embed_error_vac_already_title': 'И так уже в отпуске!',
    'vac_embed_vac_already_description': '{ds_users_names} и так уже в отпуске.',
    'vac_embed_vac_already_image': 'https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/'
                                   'abd95b4f-a41c-464a-98b6-cfddf0ebedb1/d5h0uwn-e6cf6ea9-ba51-449a-8426-8ae43dc681a1'
                                   '.gif?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODI'
                                   'yNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MT'
                                   'VlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcL2FiZDk1YjRmLWE0MWMtNDY0YS05OGI2LWNmZGRmM'
                                   'GViZWRiMVwvZDVoMHV3bi1lNmNmNmVhOS1iYTUxLTQ0OWEtODQyNi04YWU0M2RjNjgxYTEuZ2lmIn1dXSwi'
                                   'YXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.l9-2SmStZWII8k16bOrlsKyht6EV2CxtQYf'
                                   '9sufetyM',

    # Если указана некорректная дата
    'vac_embed_error_vacation_period_title': 'Ошибка с датой',
    'vac_embed_error_vacation_period_description': 'Некорректно указна дата: {vacation_period}\n'
                                                   'Используйте формат день.месяц.год. К примеру:\n'
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
    'list_vac_description': 'Показать список отдыхающих',

    # При обычном выполнении команды list_vac высветиться это
    'list_vac_embed_title': 'Список отдыхающих:',
    'list_vac_embed_description': '{data}',
    'list_vac_embed_image': 'https://c.tenor.com/PK-VJhoxC8MAAAAC/party-time-anime.gif',

    # При обычном выполнении команды list_vac высветиться это
    'list_vac_embed_error_nobody_rest_title': 'Пусто!',
    'list_vac_embed_error_nobody_rest_description': 'Все пчёлки работают.',
    'list_vac_embed_error_nobody_rest_image': 'https://c.tenor.com/cJ6FH3ZxcVoAAAAC/nico-nico-yazawa.gif',



    # cancel_vac
    # Описание команды и её параметров, которые появляются при наборе команды cancel_vac
    'cancel_vac_description': 'Отменить отпуск',
    'cancel_vac_describe_target': 'Кому будем отменять отпуск?',

    # При обычном выполнении команды cancel_vac высветиться это
    'cancel_vac_embed_title': 'Пора за работу!',
    'cancel_vac_embed_description': 'Отпуск {ds_users_names} отменён',
    'cancel_vac_embed_image': 'https://i.pinimg.com/originals/34/17/f4/3417f49a547682eb7b18c17ef8476f09.gif',

    # Если человек или группа людей и так не отпуске.
    'cancel_vac_embed_error_no_vac_title': 'Вы, наверное, ошиблись.',
    'cancel_vac_embed_error_no_vac_description': '{ds_users_names} и так не в отпуске.',
    'cancel_vac_embed_error_no_vac_image': 'https://giffiles.alphacoders.com/192/192980.gif',



    # remind
    # Описание команды и её параметров, которые появляются при наборе команды remind
    'remind_description': 'Напомнить кому-то что-то',
    'remind_describe_target': 'Кому будем что-то напоминать?',
    'remind_describe_repeat': 'Будем повторять напоминание или нет?',
    'remind_describe_next_time': 'Через какой промежуток времени напомнить? 1н(еделя) 1д(ень) 1ч(ас) 1м(инута)',
    'remind_describe_note': 'Что будем напоминать?',

    # При обычном выполнении команды remind высветиться это
    'remind_embed_title': 'Обязательно напомню!',
    'remind_embed_description': 'Напомню {repeat} {ds_users_names} через {raw_time_delta}, то есть в следующий раз это '
                                'будет {next_time}, следующее:\n{note}',
    'remind_embed_title_image': 'https://64.media.tumblr.com/11e4f3f90499ed5bdc514188a7820c99/'
                                'tumblr_inline_mpb4vam8Xi1qz4rgp.gif',

    # Если будут введены неправильно данные, скорее всего время следующего напоминания
    'remind_embed_error_value_title': 'Неправильный ввод',
    'remind_embed_error_value_description': 'Скорее всего, вы ввели неправильно время:\n{raw_time_delta}\n'
                                            'Формат ввода времени:\n'
                                            '1н 1д 1ч 1м\n'
                                            'Программа поймёт это как через одну неделю, через один, через один час и'
                                            'через одну минуту.',
    'remind_embed_error_value_title_image': 'https://c.tenor.com/gqukl6zjCWgAAAAd/death-note-light.gif',



    # list_reminds
    # Описание команды и её параметров, которые появляются при наборе команды list_reminds
    'list_reminds_description': 'Вывести список напоминаний',

    # При обычном выполнении команды list_reminds будет это
    'list_reminds_embed_title': 'Напоминание: {remind_id}',
    'list_reminds_embed_description': 'Чьё: {ds_user_name}\n'
                                      'Повторяется: {repeat}\n'
                                      'Куда будет отправлено: {channel_name}\n'
                                      'Через какое время напомнить: {timedelta}\n'
                                      'Следующие напоминание будет: {next_time}\n'
                                      'Заметка:\n{note}',
    'list_reminds_embed_image': 'https://i.ibb.co/dcyjyry/invisible.png',

    # Если нет уведомлений
    'list_reminds_embed_error_no_reminds_title': 'Напоминаний нет',
    'list_reminds_embed_no_reminds_description': 'Думаю стоит создать новое новое напоминание.',
    'list_reminds_embed_no_reminds_image': 'https://c.tenor.com/xQT14ucuqUEAAAAC/broken-in-rain-anime.gif',


    # cancel_reminds
    # Описание команды и её параметров, которые появляются при наборе команды list_reminds
    'cancel_reminds_description': 'Вывести список напоминаний',

    # При обычном выполнении команды cancel_reminds будет это
    'cancel_reminds_embed_title': 'Напоминание удалено!',
    'cancel_reminds_embed_description': 'Под номер: {remind_id}\n'
                                        'Чьё: {ds_user_name}\n'
                                        'Повторяется: {repeat}\n'
                                        'Куда будет отправлено: {channel_name}\n'
                                        'Через какое время напомнить: {timedelta}\n'
                                        'Следующие напоминание было бы: {next_time}\n'
                                        'Заметка:\n{note}',
    'cancel_reminds_embed_image': 'https://i.pinimg.com/originals/17/42/19/174219c231fbefe8c60e575fd3e4ece4.gif',

    # Если нет уведомления по указанному ID
    'cancel_reminds_embed_error_no_reminds_title': 'Такого напоминания нет',
    'cancel_reminds_reminds_embed_no_reminds_description': 'Напоминания с ID = {remind_id} нет, чтобы его можно было'
                                                           'удалить.',
    'cancel_reminds_reminds_embed_no_reminds_image': 'https://cdn.myanimelist.net/s/common/uploaded_files/'
                                                     '1449622120-505abb25b264ed361f4dc11b149bf349.gif',



    # Когда заканчивается отпуск
    'vac_end_embed_title': 'Поздравляю, отпуск кончился!',
    'vac_end_embed_description': 'Отпуск подошёл к концу, надеюсь вы хорошо отдохнули!',
    'vac_end_embed_image': 'https://i.pinimg.com/originals/f2/d0/77/f2d077b444d836310f84d553830a7fd3.gif',


    # Когда пришло время одноразового напоминания
    'remind0_embed_title': 'Напоминаю!',
    'remind0_end_embed_description': '{note}',
    'remind0_end_embed_image': 'https://c.tenor.com/jlhIudCvVGMAAAAC/kawaii-attack-on-titan.gif',

    # Когда пришло время одноразового напоминания
    'remind1_embed_title': 'Напоминаю!',
    'remind1_end_embed_description': 'Напоминание под номером: {remind_id}\n'
                                     'Следующее будет: {next_time}\n'
                                     'Заметка:\n{note}',
    'remind1_end_embed_image': 'https://pa1.narvii.com/5988/a5055a09577f9f1f84ff0f5267a287ec25ad7b51_hq.gif',
}
