import telebot , sqlite3
import logging
logging.basicConfig(level=logging.INFO)

bot = telebot.TeleBot('2043076307:AAH19GvX90aZKBei5-hK0RkqRv48fKsJaC8')
tel = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
btn = telebot.types.KeyboardButton('Raqamni yuborish',request_contact=True)
tel.add(btn)
hay = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
hayo = telebot.types.KeyboardButton('Ha')
yoq = telebot.types.KeyboardButton('Yo\'q')
hay.add(hayo,yoq)
yon = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
web = telebot.types.KeyboardButton('Web Sayt')
dotnet = telebot.types.KeyboardButton('Telegram Bot')
onec = telebot.types.KeyboardButton('SMM')
android = telebot.types.KeyboardButton('Android Dastur')
ios = telebot.types.KeyboardButton('Grafik Dizayn')
yon.add(web)
yon.add(dotnet,onec)
yon.add(android,ios)
markup = telebot.types.ReplyKeyboardRemove(selective=False)
admin =  696007117
channel = -1001643672907
with sqlite3.connect('base.db') as sql:
	cur = sql.cursor()
	cur.execute('CREATE TABLE IF NOT EXISTS base(name TEXT,user_id TEXT,tel_nom TEXT,yonalish TEXT)')
	# sql.commit()

@bot.message_handler(commands=['start'])
def start(msg):
	a = bot.send_message(msg.chat.id,'Assalomu alaykum , ro\'yxatdan o\'tish boshlandi!\nIsmingiz nima?')
	bot.register_next_step_handler(a,yonalish)

def yonalish(msg):
	con = sqlite3.connect('base.db')
	cur = con.cursor()
	cur.execute('INSERT INTO base(name,user_id,tel_nom,yonalish) VALUES(?,?,?,?)',(msg.text,msg.chat.id,'None','None'))
	con.commit()
	a = bot.send_message(msg.chat.id,'Hizmat turini tanlang',reply_markup=yon)
	bot.register_next_step_handler(a,manzilll)
def manzilll(msg):
	con = sqlite3.connect('base.db')
	cur = con.cursor()
	cur.execute('UPDATE base SET yonalish = ? WHERE yonalish = ?',(msg.text,'None',))
	con.commit()
	a = bot.send_message(msg.chat.id,'Telefon raqamingizni yuboring.',reply_markup=tel)
	bot.register_next_step_handler(a,getnum)
def getnum(msg):
	con = sqlite3.connect('base.db')
	cur = con.cursor()
	cur.execute('UPDATE base SET tel_nom = ? WHERE tel_nom = ?',(msg.contact.phone_number,'None',))
	con.commit()
	cur.execute('SELECT * FROM base WHERE user_id = ?',(msg.chat.id,))
	a = cur.fetchone()
	mal = f'''Ism: {a[0]}
Telefon raqam: {a[2]}
Qanday xizmatdan foydalanmoqchi: {a[3]}
'''
	
	bot.send_message(msg.chat.id,f'Shu ma\'lumotlar to\'g\'rimi?\n{mal}',reply_markup=hay)

	
@bot.message_handler(content_types=['text'])
def text(msg):
	con = sqlite3.connect('base.db')
	cur = con.cursor()
	if msg.text=='Ha':		
		cur.execute('SELECT * FROM base WHERE user_id = ?',(msg.chat.id,))
		z = cur.fetchone()
		mal = f'''Ism: {z[0]}
Telefon raqam: {z[2]}
Qanday xizmatdan foydalanmoqchi: {z[3]}'''
		bot.send_message(msg.chat.id,'Adminga xabar berildi , tez orada siz bilan bog\'lanishadi!',reply_markup=markup)
		bot.send_message(channel,f'{mal}')
	elif msg.text=='Yo\'q':
		cur.execute('DELETE   FROM base WHERE user_id = ?',(msg.chat.id,))
		a = bot.send_message(msg.chat.id,"Qaytadan.")
		bot.register_next_step_handler(a,start)

bot.polling(none_stop=True)