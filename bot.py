from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Replace with your actual bot token
BOT_TOKEN = "8132860873:AAEWsZ5L5SrB17LUM-0JVjn9iNsB6ln__h0"

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Initialize a simple storage for user data
user_data = {}

# Create start menu
start_menu = ReplyKeyboardMarkup(resize_keyboard=True)
start_menu.add(KeyboardButton("Ввести параметры"), KeyboardButton("Ввести продукты"))

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я диетолог-бот. Я помогу создать диету на основе твоих параметров и продуктов.\nЧто ты хочешь сделать?", reply_markup=start_menu)

@dp.message_handler(lambda message: message.text == "Ввести параметры")
async def get_parameters(message: types.Message):
    user_data[message.from_user.id] = {}
    await message.reply("Введите ваши параметры в формате: \nВозраст, вес (в кг), рост (в см), цель (похудение/поддержание/набор)")

@dp.message_handler(lambda message: message.from_user.id in user_data and not user_data[message.from_user.id].get("parameters"))
async def save_parameters(message: types.Message):
    try:
        age, weight, height, goal = message.text.split(",")
        user_data[message.from_user.id]["parameters"] = {
            "age": int(age.strip()),
            "weight": float(weight.strip()),
            "height": float(height.strip()),
            "goal": goal.strip().lower()
        }
        await message.reply("Параметры сохранены! Теперь введите продукты.", reply_markup=start_menu)
    except Exception:
        await message.reply("Пожалуйста, введите параметры в правильном формате: \nВозраст, вес (в кг), рост (в см), цель (похудение/поддержание/набор)")

@dp.message_handler(lambda message: message.text == "Ввести продукты")
async def get_products(message: types.Message):
    await message.reply("Введите список продуктов через запятую. Например: курица, рис, брокколи.")

@dp.message_handler(lambda message: message.from_user.id in user_data and not user_data[message.from_user.id].get("products"))
async def save_products(message: types.Message):
    products = [product.strip().lower() for product in message.text.split(",")]
    user_data[message.from_user.id]["products"] = products
    await message.reply("Продукты сохранены! Теперь я могу предложить диету. Напишите 'Меню', чтобы получить рекомендации.")

@dp.message_handler(lambda message: message.text.lower() == "меню")
async def generate_menu(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_data or not user_data[user_id].get("parameters") or not user_data[user_id].get("products"):
        await message.reply("Сначала введите параметры и продукты.", reply_markup=start_menu)
        return

    params = user_data[user_id]["parameters"]
    products = user_data[user_id]["products"]

    # Simple diet suggestion logic (for demonstration purposes)
    calorie_goal = 2000  # Default calorie goal
    if params["goal"] == "похудение":
        calorie_goal = 1500
    elif params["goal"] == "набор":
        calorie_goal = 2500

    suggested_menu = f"Ваши параметры: {params}\nВаши продукты: {', '.join(products)}\n" \
                     f"Рекомендуемая калорийность: {calorie_goal} ккал.\n" \
                     f"Пример меню: \n- Завтрак: Овсянка с {products[0]}\n- Обед: {products[0]} с {products[1]}\n- Ужин: {products[1]} с {products[2]}"

    await message.reply(suggested_menu)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
