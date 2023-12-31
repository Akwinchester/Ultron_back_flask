<h1>Дневник тренировок</h1>
<p>Это веб-приложение для ведения дневника тренировок и мотивации пользователей.</p>

<h2>Описание</h2>
<p>Пользователи могут заводить свои активности (бег, йога, кроссфит) и добавлять к ним записи с данными о проделанных тренировках.</p>
<p>Также можно подключать друзей к своим активностям. Когда пользователь делает новую запись, уведомление получают подписанные на активность друзья. Это мотивирует не пропускать тренировки.</p>

<h2>Возможности</h2>
<ul>
  <li>Создание собственных активностей</li>
  <li>Добавление записей с данными о тренировках</li>
  <li>Подключение друзей к активностям</li>
  <li>Просмотр общего рейтинга пользователей</li>
  <li>Просмотр личных достижений и статистики</li>
</ul>

<h2>Технологии</h2>
<ul>
  <li>Python 3.8</li>
  <li>Flask</li>
  <li>SQLAlchemy</li>
  <li>MySQL</li>
  <li>Alembic</li>
</ul>

<h2>Структура данных</h2>
<p>Реляционная БД MySQL с таблицами:</p>
<ul>
  <li>Пользователи (User)</li>
  <li>Активности (Activity)</li>
  <li>Записи (Entry)</li>
</ul>

<h2>Установка</h2>
<ol>
  <li>Клонировать репозиторий</li>
  <li>Настроить БД</li>
  <li>Установить зависимости <code>pip install -r requirements.txt</code></li>
  <li>Запустить <code>python app.py</code></li>
</ol>

<h2>Использование</h2>
<p>Работа с приложением происходит через веб-интерфейс.</p>
<p>Основные сценарии:</p>
<ul>
  <li>Регистрация и авторизация</li>
  <li>Создание активности</li>
  <li>Добавление записи</li>
  <li>Просмотр статистики и рейтинга</li>
</ul>

<p>Подробнее смотрите в документации.</p>
