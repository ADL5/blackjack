import tkinter as tk
from random import choice
from json import load,dump
from time import sleep
import sys
from os import path

root = tk.Tk()
root.title("blackjack")
root.geometry("400x500+950+100")
root['bg'] = 'gray20'

if sys.platform == 'win32':
    name_file = '\\data player.json'
elif sys.platform == 'linux':
    name_file = '/data player.json'
total_path = path.abspath(path.dirname(sys.argv[0])) + name_file

if not(path.isfile(total_path)):
	with open(total_path,'w',encoding='utf-8') as file:
		dump({"status_user": False,"last login": ""},file,indent=4)

with open(total_path,'r',encoding='utf-8') as file:
	data = load(file)

money = 0
bid = 0
enemy_score = 0
player_score = 0

def run_game():
	global money, bid, data, enemy_score, player_score

	money = data[data['last login']]['money']
	names_enemy = ["МАФИОЗИЙ", "Жулик", 'Глава Банды', 'Диллер']
	nick_enemy = choice(names_enemy)
	nick_player = data['last login']
	cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 10, 10, 10]

	def frame_bid():
		global bid, money

		def check_bid():
			global bid, money
			try:
				bid = int(entry_bid.get())
			except:
				pass
			if bid > money * 0.99999999 or bid > 999999999:
				label_error_bid['text'] = 'ставка слишком высока'
				label_error_bid['fg'] = '#660000'
			elif bid < money * 0.1:
				label_error_bid['text'] = 'ставка слишком мала'
				label_error_bid['fg'] = '#660000'
			else:
				money -= bid
				label_balance['text'] = f'баланс: {money}$'
				label_balance_game['text'] = f'баланс: {money}$'
				label_error_bid['fg'] = 'gray60'
				label_balance_game['fg'] = 'gray78'
				label_look_at_bid_game['text'] = f'ставка: {bid}$'
				label_look_at_bid_game['fg'] = 'gray60'
				frame_bid.destroy()
				frame_game.place(relheight=1, relwidth=1)
				give_cards()

		frame_bid = tk.Frame(frame_default, bg='#073300')
		label_error_bid = tk.Label(frame_bid, text='Ставка слишком высока', bg='#073300', fg='#073300',font=('times new roman', 18))
		label_error_bid.place(relwidth=1, relheight=0.17, relx=0.0, rely=0.05)
		entry_bid = tk.Entry(frame_bid, bg='#073300',fg='gray80',border=0, font=('times new roman', 20), justify='center')
		entry_bid.place(relwidth=0.6, relheight=0.18, relx=0.2, rely=0.38)
		entry_bid.insert(0, bid)
		btn_put_bid = tk.Button(frame_bid, text='Поставить', command=check_bid, bg='gray30',activebackground='gray28',font=('times new roman',16))
		btn_put_bid.place(relwidth=0.67, relheight=0.17, relx=0.165, rely=0.73)
		frame_bid.place(relheight=0.4, relwidth=0.7, relx=0.15, rely=0.3)

	frame_default = tk.Frame(root, bg='#073300')
	btn_bid = tk.Button(frame_default, text='Ставка', bg='gray30',activebackground='gray28', font=('times new roman', 14), command=frame_bid)
	btn_bid.place(relwidth=0.4, relheight=0.1, relx=0.3, rely=0.553)
	label_balance = tk.Label(frame_default, text=f'баланс: {money}$', bg='#073300', fg='gray50',font=('times new roman', 15))
	label_balance.pack(anchor='ne')
	frame_default.place(relwidth=1, relheight=1)

	def winner():
		global bid,money,player_score,enemy_score,data
		label_enemy["fg"] = '#660000'
		label_player['fg'] = '#106b01'
		label_enemy.update()
		label_player.update()
		sleep(1)
		money += int(bid*2)
		player_score = 0
		enemy_score = 0
		label_balance_game['text'] = f'баланс: {money}$'
		label_balance['text'] = f'баланс: {money}'
		label_player_score['text'] = player_score
		label_enemy_score['text'] = enemy_score
		label_enemy["fg"] = 'gray39'
		label_player['fg'] = 'gray39'
		data[data['last login']]['money'] = money
		data[data['last login']]['money_win'] += bid
		btn_hit.place_forget()
		btn_stand.place_forget()
		frame_game.place_forget()
		with open(total_path, 'w', encoding='utf-8') as file:
			dump(data,file,indent=4)

	def loser():
		global bid, money, player_score, enemy_score, data
		label_enemy["fg"] = '#106b01'
		label_player['fg'] = '#660000'
		label_enemy.update()
		label_player.update()
		sleep(1)
		player_score = 0
		enemy_score = 0
		label_balance_game['text'] = f'баланс: {money}$'
		label_balance['text'] = f'баланс: {money}'
		label_player_score['text'] = player_score
		label_enemy_score['text'] = enemy_score
		label_enemy["fg"] = 'gray39'
		label_player['fg'] = 'gray39'
		data[data['last login']]['money'] = money
		data[data['last login']]['money_win'] -= bid
		btn_hit.place_forget()
		btn_stand.place_forget()
		frame_game.place_forget()

		if money<1001:

			frame_gameover = tk.Frame(frame_default,bg='#660000')
			label_gameover = tk.Label(frame_gameover,text='Конец,\nТы проиграл.\nИнформация об аккаунте:\nВыиграл денег: {0}'.format(data[data['last login']]['money_win']),bg='#660000',font=('Times new roman',20))
			label_gameover.pack(pady=70)
			btn_leave = tk.Button(frame_gameover,text='Выйти',command=lambda: root.destroy(),width=14,height=1,font=('Times new roman',13),bg='gray35',activebackground='gray30',fg='gray5',activeforeground='gray2')
			btn_leave.pack(pady=30)
			del data[data['last login']]
			data['last login'] = ''
			data['status_user'] = False
			with open(total_path, 'w', encoding='utf-8') as file:
				dump(data, file, indent=4)
			frame_gameover.place(relheight=1,relwidth=1)

		with open(total_path, 'w', encoding='utf-8') as file:
			dump(data, file, indent=4)

	def give_cards():
		global enemy_score, player_score,money,bid
		for i in range(3):
			label_enemy_score.update()
			label_player_score.update()
			sleep(1)
			if i % 2 != 0:
				enemy_score += choice(cards)
				label_enemy_score['text'] = f'{enemy_score}'
			else:
				player_score += choice(cards)
				label_player_score['text'] = f'{player_score}'
		if player_score == 21:
			label_player_score.update()
			sleep(1)
			winner()
		elif player_score>21:
			label_player_score.update()
			sleep(1)
			loser()
		else:
			btn_hit.place(relwidth=0.238, relheight=0.23, relx=0.09, rely=0.683)
			btn_stand.place(relwidth=0.238, relheight=0.23, relx=0.6755, rely=0.683)

	def hit():
		global enemy_score,player_score
		player_score+=choice(cards)
		label_player_score['text'] = player_score
		if player_score>21:
			btn_hit.place_forget()
			btn_stand.place_forget()
			label_player_score.update()
			sleep(0.7)
			loser()
		elif player_score==21:
			btn_hit.place_forget()
			btn_stand.place_forget()
			label_player_score.update()
			sleep(0.7)
			winner()

	def stand():
		global enemy_score,player_score
		btn_hit.place_forget()
		btn_stand.place_forget()
		enemy_score+=choice(cards)
		label_enemy_score['text'] = enemy_score
		while enemy_score<17:
			enemy_score+=choice(cards)
			label_enemy_score.update()
			sleep(1)
			label_enemy_score['text'] = enemy_score
		if enemy_score == 21:
			label_enemy_score.update()
			sleep(1)
			loser()
		elif enemy_score>21:
			label_enemy_score.update()
			sleep(1)
			winner()
		elif 21 - player_score <= 21 - enemy_score:
			label_player_score.update()
			label_enemy_score.update()
			sleep(1)
			winner()
		else:
			label_player_score.update()
			label_enemy_score.update()
			sleep(1)
			loser()

	frame_game = tk.Frame(root,bg='#073300')
	btn_hit = tk.Button(frame_game,text='HIT',bg='gray45',fg='gray5',activebackground='gray37',activeforeground='gray2',font=('times new roman', 15),command=hit)
	btn_stand = tk.Button(frame_game,text='STAND',bg='gray45',fg='gray5',activebackground='gray37',activeforeground='gray2',font=('times new roman', 15),command=stand)
	label_enemy = tk.Label(frame_game,text=nick_enemy, bg='#073300', fg='gray39',font=('times new roman', 18))
	label_enemy.place(relwidth=0.51,relheight=0.06,relx=0.24,rely=0.12)
	label_enemy_score = tk.Label(frame_game, text=f'{enemy_score}',bg='#073300', fg='gray39',font=('times new roman', 25))
	label_enemy_score.place(relwidth=0.1,relheight=0.07,relx=0.45,rely=0.2025)
	label_player = tk.Label(frame_game, text=nick_player, bg='#073300', fg='gray39', font=('times new roman', 20))
	label_player.place(relwidth=0.48, relheight=0.06, relx=0.26, rely=0.42)
	label_player_score = tk.Label(frame_game, text=f'{player_score}', bg='#073300', fg='gray39',font=('times new roman', 25))
	label_player_score.place(relwidth=0.1, relheight=0.07, relx=0.45, rely=0.5025)
	label_balance_game = tk.Label(frame_game, text=f'баланс: {money}$', bg='#073300', fg='gray25',font=('times new roman', 15))
	label_balance_game.pack(anchor='ne')
	label_look_at_bid_game = tk.Label(frame_game, text=f'Ставка: {str(bid)}$', bg='#073300',font=('times new roman', 15))
	label_look_at_bid_game.pack(anchor='ne')

if not(data['status_user']):
	def append_new_user():

		def go_back():
			frame_registr.destroy()

		def swap_flag():
			global data
			if enabled.get() == 1:
				data['status_user'] = True
			else:
				data['status_user'] = False

		def is_valid():
			global data
			flag = [False, False]
			login = login_entry.get()
			password = password_entry.get()
			if len(password) < 5:
				password_label_error['fg'] = '#660000'
				flag[0] = False
			else:
				password_label_error['fg'] = 'gray30'
				flag[0] = True
			if login in data or login == '':
				login_label_error['fg'] = '#660000'
				flag[1] = False
			else:
				login_label_error['fg'] = 'gray30'
				flag[1] = True
			return flag

		def append_user():
			global data
			login = login_entry.get()
			password = password_entry.get()
			flag = is_valid()
			if all(flag):
				swap_flag()
				data[f'{login}'] = {'password': f'{password}', 'money':0}
				data['last login'] = login
				data[login]['money'] = 5000
				data[login]['money_win'] = 0
				with open(total_path, 'w', encoding='utf-8') as file:
					dump(data,file,indent=4)
				flag = False
				frame_registr.destroy()
				frame_new_user.destroy()
				run_game()

		frame_registr = tk.Frame(root, bg='gray30')
		login_label = tk.Label(frame_registr, text='Логин', font=('times new roman', 20), bg='gray30').place(relwidth=0.3, relheight=0.1, relx=0.2, rely=0.1)
		login_entry = tk.Entry(frame_registr, bg='gray20', fg='gray70', font=('times new roman', 20))
		login_entry.place(relheight=0.07, relwidth=0.5, relx=0.25, rely=0.2)
		login_label_error = tk.Label(frame_registr, text='Занят', font=('times new roman', 20), bg='gray30',fg='gray30')
		login_label_error.place(relwidth=0.3, relheight=0.08, relx=0.46, rely=0.109)
		password_label = tk.Label(frame_registr, text='Пароль', font=('times new roman', 20), bg='gray30').place(relwidth=0.3, relheight=0.1, relx=0.2, rely=0.353)
		password_entry = tk.Entry(frame_registr, bg='gray20', fg='gray70', font=('times new roman', 20))
		password_entry.place(relheight=0.07, relwidth=0.5, relx=0.25, rely=0.45)
		password_label_error = tk.Label(frame_registr, text='Короткий', font=('times new roman', 20), bg='gray30',fg='gray30')
		password_label_error.place(relwidth=0.3, relheight=0.08, relx=0.46, rely=0.362)
		enabled = tk.IntVar()
		btn_remember_me = tk.Checkbutton(frame_registr, text='Запомнить меня', variable=enabled, bg='gray30',fg='gray5', activeforeground='gray5', activebackground='gray30',command=swap_flag).place(relwidth=0.3, relheight=0.05, relx=0.7, rely=0.95, )
		btn_enter_data = tk.Button(frame_registr,text='Продолжить',command=append_user,font=('times new roman', 20), bg='gray30',activebackground='gray28').place(relwidth=0.5, relheight=0.1, relx=0.25, rely=0.65)
		btn_goback = tk.Button(frame_registr,text='Назад',command=go_back,font=('times new roman', 20), bg='gray30',activebackground='gray28').place(relwidth=0.4,relheight=0.08,relx=0.007,rely=0.913)
		frame_registr.place(relwidth=1, relheight=1)

	def enter_new_user():

		def go_back():
			frame_enter.destroy()

		def swap_flag():
			global data
			if enabled.get() == 1:
				data['status_user'] = True
			else:
				data['status_user'] = False

		def is_valid():
			global data
			flag = [False, False]
			login = login_entry.get()
			password = password_entry.get()
			if login not in data.keys() or login=='':
				login_label_error['fg'] = '#660000'
				flag[0] = False
			else:
				login_label_error['fg'] = 'gray30'
				flag[0] = True
			if password != data[login]['password']:
				password_label_error['fg'] = '#660000'
				flag[1] = False
			else:
				password_label_error['fg'] = 'gray30'
				flag[1] = True
			return flag

		def enter_user():
			global data
			try:
				login = login_entry.get()
				flag = is_valid()
				data['last login'] = login
				if all(flag):
					with open(total_path, 'w', encoding='utf-8') as file:
						dump(data,file,indent=4)
					frame_enter.destroy()
					frame_new_user.destroy()
					run_game()
			except:
				pass
		frame_enter = tk.Frame(root,bg='gray30')
		login_label = tk.Label(frame_enter, text='Логин', font=('times new roman', 20), bg='gray30').place(relwidth=0.3, relheight=0.1, relx=0.2, rely=0.1)
		login_entry = tk.Entry(frame_enter, bg='gray20', fg='gray70', font=('times new roman', 20))
		login_entry.place(relheight=0.07, relwidth=0.5, relx=0.25, rely=0.2)
		login_label_error = tk.Label(frame_enter, text='Неверный', font=('times new roman', 20), bg='gray30',fg='gray30')
		login_label_error.place(relwidth=0.3, relheight=0.08, relx=0.46, rely=0.109)
		password_label = tk.Label(frame_enter, text='Пароль', font=('times new roman', 20), bg='gray30').place(relwidth=0.3, relheight=0.1, relx=0.2, rely=0.353)
		password_entry = tk.Entry(frame_enter, bg='gray20', fg='gray70', font=('times new roman', 20))
		password_entry.place(relheight=0.07, relwidth=0.5, relx=0.25, rely=0.45)
		password_label_error = tk.Label(frame_enter, text='Неверный', font=('times new roman', 20), bg='gray30',fg='gray30')
		password_label_error.place(relwidth=0.3, relheight=0.08, relx=0.46, rely=0.362)
		enabled = tk.IntVar()
		btn_remember_me = tk.Checkbutton(frame_enter, text='Запомнить меня', variable=enabled, bg='gray30',fg='gray5', activeforeground='gray5', activebackground='gray30',command=swap_flag).place(relwidth=0.3, relheight=0.05, relx=0.7, rely=0.95, )
		btn_enter_data = tk.Button(frame_enter, text='Продолжить', command=enter_user, font=('times new roman', 20),bg='gray30',activebackground='gray28').place(relwidth=0.5, relheight=0.1, relx=0.25, rely=0.65)
		btn_goback = tk.Button(frame_enter, text='Назад', command=go_back, font=('times new roman', 20),bg='gray30',activebackground='gray28').place(relwidth=0.4,relheight=0.08,relx=0.007,rely=0.913)
		frame_enter.place(relwidth=1,relheight=1)

	frame_new_user = tk.Frame(root, bg='gray30')
	welcome_label = tk.Label(frame_new_user, text='Приветствую тебя в Blackjack!', font=('times new roman', 16),bg='gray30').place(relwidth=0.7, relheight=0.2, relx=0.1501, rely=0.15)
	btn_registr = tk.Button(frame_new_user, text='создать аккаунт', command=append_new_user, bg='gray30',activebackground='gray28',font=('Times new roman',15)).place(relwidth=0.41,relheight=0.17,relx=0.535, rely=0.5)
	btn_login = tk.Button(frame_new_user, text='войти', command=enter_new_user, bg='gray30', activebackground='gray28',font=('Times new roman',15)).place(relwidth=0.4,relheight=0.17,relx=0.06, rely=0.5)
	frame_new_user.place(relheight=1, relwidth=1)

else:
	run_game()

root.mainloop()




