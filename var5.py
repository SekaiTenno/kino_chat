import telebot
import csv


# Создаем бота и указываем токен
bot = telebot.TeleBot('7091433663:AAFBpwtQAXksVnnzcymp7SVKYDJ2QAlSAeA')

# Загружаем данные из файла movies.csv
def load_movies():
    movies = {}
    with open("movies.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            title = row["Title"]
            movies[title] = {
                "Year": row["Year"],
                "Cast": row["Cast"],
                "Description": row["Description"]
            }
    return movies

# Глобальная переменная для хранения текущего состояния
user_state = {}

# Обработчик команды /start
@bot.message_handler(commands=["start"])
def handle_start(message):
    if user_state.get(message.chat.id) != "searching":
        user_state[message.chat.id] = "searching"
        bot.send_message(message.chat.id, "Напишите название фильма:")

# # Обработчик команды /stop
# @bot.message_handler(commands=["stop"])
# def handle_stop(message):
#     bot.send_message(message.chat.id, "Бот остановлен. Для перезапуска используйте команду /restart.")
#     return

# # Обработчик команды /restart
# @bot.message_handler(commands=["restart"])
# def handle_restart(message):
#     user_state[message.chat.id] = "searching"
#     bot.send_message(message.chat.id, "Бот перезапущен. Напишите название фильма:")

# Обработчик текстовых сообщений для поиска фильмов
@bot.message_handler(func=lambda message: user_state.get(message.chat.id) == "searching")
def handle_search(message):
    movies = load_movies()
    search_query = message.text.lower()
    found_movies = [title for title in movies if search_query in title.lower()]
    if found_movies:
        for title in found_movies:
            movie_info = movies[title]
            response = f"Название: {title}\nГод: {movie_info['Year']}\nАктеры: {movie_info['Cast']}\nОписание: {movie_info['Description']}"
            bot.send_message(message.chat.id, response)
        markup = telebot.types.ReplyKeyboardMarkup(row_width=1)
        markup.add("Продолжить поиск")
        bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Фильм не найден. Попробуйте еще раз:")
    

# # Запускаем бота
bot.polling(none_stop=True)
