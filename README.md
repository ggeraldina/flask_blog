## 
1. Виртуальная среда Python `python -m venv venv`. Первым venv в команде является имя пакета виртуальной среды Python, а второе — имя виртуальной среды
2. Теперь вам нужно сообщить системе, что вы хотите ее использовать, активируя ее. Чтобы активировать новую виртуальную среду, используете следующую команду.   
В Windows: `venv\Scripts\activate`; (или `source venv/bin/activate`)
3. `pip install -r requirements.txt`

    > общепринятой практикой является создание файла `requirements.txt` в корневой папке проекта с перечислением всех зависимостей и их версий. Создание списка:
    >
    > `pip freeze > requirements.txt`
    >
    > Команда `pip freeze` создаст дамп всех пакетов, установленных в виртуальной среде, в формате, соответствующем файлу `requirements.txt`. 

4. Запуск `flask run` и переменная среды `FLASK_APP`

    * В терминале запустите приложение, введя `python -m flask run` (для Windows), который запускает сервер разработки Flask. Сервер разработки ищет `app.py` по умолчанию. 
    
    * Кроме того, если вы хотите запустить сервер разработки на другой IP-адрес или порт, используйте аргументы командной строки узла и порта, как `--host=0.0.0.0 --port=80`
    
    > Если вы хотите использовать другое имя `app.py` файла, например `program.py`, определите переменную среды с именем `FLASK_APP` и установите ее значение для выбранного файла. Затем сервер разработки Flask использует значение `FLASK_APP` вместо файла по умолчанию `app.py`
    >
    > В данном случае Flask можно сообщить:
    > В Windows: `set FLASK_APP=microblog.py`; (или `export FLASK_APP=microblog.py`)

    > Вы можете создать файл .env со всеми переменными среды, которые необходимы вашему приложению. Важно, чтобы вы не добавляли ваш .env-файл в систему управления версиями. Не стоит иметь файл, содержащий пароли и другую конфиденциальную информацию, включенный в репозиторий исходного кода.

    > .env-файл можно использовать для всех переменных временной конфигурации, но его нельзя использовать для переменных среды `FLASK_APP` и `FLASK_DEBUG`, так как они необходимы уже в процессе начальной загрузки приложения, до того, как экземпляр приложения и его объект конфигурации появится.

5. Сценарий flask хорош для запуска локального сервера разработки, но вам придется перезапускать его вручную после каждого изменения кода. Это не очень приятно, и фляжка может сделать лучше. Если вы включите поддержку отладки, сервер перезагрузится при изменении кода, а также предоставит вам полезный отладчик, если что-то пойдет не так. 

    Чтобы включить все функции разработки (включая режим отладки), можно экспортировать переменную среды `FLASK_ENV` и установить ее в значение development перед запуском сервера:

    В Windows: `set FLASK_ENV=development`

    Переменная среды `FLASK_ENV` имеет значение по умолчанию production
