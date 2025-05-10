#!/usr/bin/python

import random
import requests
from time import sleep
import os, signal, sys
from pyfiglet import figlet_format
from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich.text import Text
from rich.style import Style
from carparktool import CarParkTool

__CHANNEL_USERNAME__ = "GALGENTool"
__GROUP_USERNAME__   = "GALGENTool_chat"

def signal_handler(sig, frame):
    print("\n Bye Bye...")
    sys.exit(0)

def gradient_text(text, colors):
    lines = text.splitlines()
    height = len(lines)
    width = max(len(line) for line in lines)
    colorful_text = Text()
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char != ' ':
                color_index = int(((x / (width - 1 if width > 1 else 1)) + (y / (height - 1 if height > 1 else 1))) * 0.5 * (len(colors) - 1))
                color_index = min(max(color_index, 0), len(colors) - 1)  # Ensure the index is within bounds
                style = Style(color=colors[color_index])
                colorful_text.append(char, style=style)
            else:
                colorful_text.append(char)
        colorful_text.append("\n")
    return colorful_text

def banner(console):
    os.system('cls' if os.name == 'nt' else 'clear')
    brand_name = figlet_format('GALGENTool', font='drpepper')
    colors = [
        "rgb(255,0,0)", "rgb(255,69,0)", "rgb(255,140,0)", "rgb(255,215,0)", "rgb(173,255,47)", 
        "rgb(0,255,0)", "rgb(0,255,255)", "rgb(0,191,255)", "rgb(0,0,255)", "rgb(139,0,255)",
        "rgb(255,0,255)"
    ]
    colorful_text = gradient_text(brand_name, colors)
    console.print(colorful_text, end=None)
    console.print("[bold green]♕ GALGENTool[/bold green]: скрипт который поможет вам стать самым крутым.")
    console.print(f"[bold green]♕ Telegram[/bold green]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue] or [bold blue]@{__GROUP_USERNAME__}[/bold blue].")
    console.print("[bold red]==================================================[/bold red]")
    console.print("[bold yellow]! Примечание[/bold yellow]: Вам нужно выйти с игры перед использованием !.", end="\n\n")

def load_player_data(cpm):
    response = cpm.get_player_data()
    if response.get('ok'):
        data = response.get('data')
        if 'floats' in data and 'localID' in data and 'деньги' in data and 'коины' in data:
            console.print("[bold][red]================[/red][ ДАННЫЕ ИГРОКА ][red]================[/red][/bold]")
            console.print(f"[bold green]Имя   [/bold green]: { (data.get('Name') if 'Name' in data else 'UNDEFINED') }.")
            console.print(f"[bold green]ЛокальныйID[/bold green]: { (data.get('localID') if 'localID' in data else 'UNDEFINED') }.")
            console.print(f"[bold green]Деньги  [/bold green]: { (data.get('money') if 'money' in data else 'UNDEFINED') }.")
            console.print(f"[bold green]Коины  [/bold green]: { (data.get('coin') if 'coin' in data else 'UNDEFINED') }.")
        else:
            console.print("[bold red]! ОШИБКА[/bold red]: новые учетные записи должны быть авторизованы в игре хотя бы один раз!.")
            exit(1)
    else:
        console.print("[bold red]! ОШИБКА[/bold red]: похоже, ваш логин установлен неправильно !.")
        exit(1)
    
def load_key_data(cpm):
    data = cpm.get_key_data()
    console.print("[bold][red]==================================================[/red][/bold]")
    console.print(f"[bold green]Ключ доступа [/bold green]: { data.get('access_key') }.")
    console.print(f"[bold green]Телеграм ID[/bold green]: { data.get('telegram_id') }.")
    console.print(f"[bold green]Баланс    [/bold green]: { (data.get('coins') if not data.get('is_unlimited') else 'Unlimited') }.")

def load_client_details():
    response = requests.get("http://ip-api.com/json")
    data = response.json()
    console.print("[bold][red]==================================================[/red][/bold]")
    console.print(f"[bold][green]Расположение[/bold][/green]: {data.get('city')}, {data.get('regionName')}, {data.get('countryCode')}")
    console.print(f"[bold][green]Интернет-провайдер[/bold][/green]     : {data.get('isp')}")
    console.print("[bold][red]===================[/red][ УСЛУГИ ][red]===================[/red][/bold]")

def prompt_valid_value(content, tag, password=False):
    while True:
        value = Prompt.ask(content, password=password)
        if not value or value.isspace():
            print(f"{tag} не может быть пустым или состоять только из пробелов. Попробуйте еще раз.")
        else:
            return value

def interpolate_color(start_color, end_color, fraction):
    start_rgb = tuple(int(start_color[i:i+2], 16) for i in (1, 3, 5))
    end_rgb = tuple(int(end_color[i:i+2], 16) for i in (1, 3, 5))
    interpolated_rgb = tuple(int(start + fraction * (end - start)) for start, end in zip(start_rgb, end_rgb))
    return "{:02x}{:02x}{:02x}".format(*interpolated_rgb)

def rainbow_gradient_string(customer_name):
    modified_string = ""
    num_chars = len(customer_name)
    start_color = "{:06x}".format(random.randint(0, 0xFFFFFF))
    end_color = "{:06x}".format(random.randint(0, 0xFFFFFF))
    for i, char in enumerate(customer_name):
        fraction = i / max(num_chars - 1, 1)
        interpolated_color = interpolate_color(start_color, end_color, fraction)
        modified_string += f'[{interpolated_color}]{char}'
    return modified_string

if __name__ == "__main__":
    console = Console()
    signal.signal(signal.SIGINT, signal_handler)
    while True:
        banner(console)
        acc_email = prompt_valid_value("[bold][?] Электронная почта аккаунта[/bold]", "Email", password=False)
        acc_password = prompt_valid_value("[bold][?] Пароль учетной записи[/bold]", "Password", password=False)
        acc_access_key = prompt_valid_value("[bold][?] Ключ доступа[/bold]", "Access Key", password=False)
        console.print("[bold cyan][%] Попытка войти[/bold cyan]: ", end=None)
        cpm = CarParkTool(acc_access_key)
        login_response = cpm.login(acc_email, acc_password)
        if login_response != 0:
            if login_response == 100:
                console.print("[bold red]АККАУНТ НЕ НАЙДЕН[/bold red].")
                sleep(2)
                continue
            elif login_response == 101:
                console.print("[bold red]НЕПРАВИЛЬНЫЙ ПАРОЛЬ[/bold red].")
                sleep(2)
                continue
            elif login_response == 103:
                console.print("[bold red]НЕВЕРНЫЙ КЛЮЧ ДОСТУПА[/bold red].")
                sleep(2)
                continue
            else:
                console.print("[bold red]ПОПРОБУЙТЕ ЕЩЕ РАЗ[/bold red].")
                console.print("[bold yellow]! Примечание[/bold yellow]: убедитесь, что вы заполнили поля !.")
                sleep(2)
                continue
        else:
            console.print("[bold green]УСПЕШНО[/bold green].")
            sleep(2)
        while True:
            banner(console)
            load_player_data(cpm)
            load_key_data(cpm)
            load_client_details()
            choices = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22"]
            console.print("[bold][cyan](01):[/cyan] [gold]Накрутить деньги                 500[/red]")
            console.print("[bold][cyan](02):[/cyan] [gold]Накрутить коины                 1500[/red]")
            console.print("[bold][cyan](03):[/cyan] [gold]Сделать ранг кинг                400[/red]")
            console.print("[bold][cyan](04):[/cyan] [gold]Сделать кастом айди              600[/red]")
            console.print("[bold][cyan](05):[/cyan] [gold]Изменить имя                     100[/red]")
            console.print("[bold][cyan](06):[/cyan] [gold]Изменить имя (На радужное)       100[/red]")
            console.print("[bold][cyan](07):[/cyan] [gold]Установить номера                500[/red]")
            console.print("[bold][cyan](08):[/cyan] [gold]Удалить аккаунт                 FREE[/red]")
            console.print("[bold][cyan](09):[/cyan] [gold]Зарегистрировать аккаунт        FREE[/red]")
            console.print("[bold][cyan](10):[/cyan] [gold]Удалить всех друзей              300[/red]")
            console.print("[bold][cyan](11):[/cyan] [gold]Разблокировать платные авто     1700[/red]")
            console.print("[bold][cyan](12):[/cyan] [gold]Разблокировать все авто         1400[/red]")
            console.print("[bold][cyan](13):[/cyan] [gold]Разблокировать мигалки на всех авто 2000[/red]")
            console.print("[bold][cyan](14):[/cyan] [gold]Разблокировать двигатель w16     800[/red]")
            console.print("[bold][cyan](15):[/cyan] [gold]Разблокировать все гудки         700[/red]")
            console.print("[bold][cyan](16):[/cyan] [gold]Отключить получение урона        700[/red]")
            console.print("[bold][cyan](17):[/cyan] [gold]Разблокировать безлимитное топливо 1500[/red]")
            console.print("[bold][cyan](18):[/cyan] [gold]Разблокировать дом 3            2500[/red]")
            console.print("[bold][cyan](19):[/cyan] [gold]Разблокировать дым              2000[/red]")
            console.print("[bold][cyan](20):[/cyan] [gold]Изменить победы в гонках        800[/red]")
            console.print("[bold][cyan](21):[/cyan] [gold]Изменить поражения в гонках     800[/red]")
            console.print("[bold][cyan](22):[/cyan] [gold]Клонировать аккаунт             4000[/red]")
            console.print("[bold][cyan](0) :[/cyan] [red]Выход[/red]", end="\n\n")
            service = IntPrompt.ask(f"[bold][?] Выберите услугу [red][1-{choices[-1]} or 0][/red][/bold]", choices=choices, show_choices=False)
            if service == 0: # Exit
                console.print(f"[bold yellow][!] Спасибо за использование нашего инструмента, присоединяйтесь к нашему каналу в Telegram[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
            elif service == 1: # Increase Money
                console.print("[bold cyan][!] Укажите, сколько денег вы хотите.[/bold cyan]")
                amount = IntPrompt.ask("[bold][?] Количество[/bold]")
                console.print("[bold cyan][%] Сохранение ваших данных[/bold cyan]: ", end=None)
                if amount > 0 and amount <= 50000000:
                    if cpm.set_player_money(amount):
                        console.print("[bold green]УСПЕШНО.[/bold green]")
                        console.print("==================================")
                        answ = Prompt.ask("[bold cyan][?] Вы хотите выйти?[/bold cyan]", choices=["y", "n"], default="n")
                        if answ == "y": console.print(f"[bold yellow][!] Спасибо за использование нашего инструмента, присоединяйтесь к нашему каналу в Telegram[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
                        else: continue
                    else:
                        console.print("[bold red]НЕУСПЕШНО.[/bold red]")
                        console.print("[bold yellow][!] Пожалуйста, попробуйте еще раз.[/bold yellow]")
                        sleep(2)
                        continue
                else:
                    console.print("[bold red]НЕУСПЕШНО.[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста, используйте допустимые значения.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 2: # Increase Coins
                console.print("[bold cyan][!] Введите желаемое количество монет.[/bold cyan]")
                amount = IntPrompt.ask("[bold][?] Количество[/bold]")
                console.print("[bold cyan][%] Сохранение ваших данных[/bold cyan]: ", end=None)
                if amount > 0 and amount <= 200000:
                    if cpm.set_player_coins(amount):
                        console.print("[bold green]УСПЕШНО.[/bold green]")
                        console.print("==================================")
                        answ = Prompt.ask("[bold cyan][?] Вы хотите выйти? ?[/bold cyan]", choices=["y", "n"], default="n")
                        if answ == "y": console.print(f"[bold yellow][!] Спасибо за использование нашего инструмента, присоединяйтесь к нашему каналу в Telegram[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
                        else: continue
                    else:
                        console.print("[bold red]НЕУСПЕШНО.[/bold red]")
                        console.print("[bold yellow][!] Пожалуйста, попробуйте еще раз.[/bold yellow]")
                        sleep(2)
                        continue
                else:
                    console.print("[bold red]НЕУСПЕШНО.[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста, используйте допустимые значения.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 3: # King Rank
                console.print("[bold red][!] Note:[/bold red]: Если в игре не отображается звание ранг кинг, закройте ее и откройте несколько раз.")
                console.print("[bold red][!] Note:[/bold red]: пожалуйста, не получайте ранг кинг на одном аккаунте дважды.", end="\n\n")
                sleep(2)
                console.print("[bold cyan][%] Даю вам звание ранг кинг[/bold cyan]: ", end=None)
                if cpm.set_player_rank():
                    console.print("[bold green]УСПЕШНО.[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold cyan][?] Вы хотите выйти?[/bold cyan]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"[bold yellow][!] Спасибо за использование нашего инструмента, присоединяйтесь к нашему каналу в Telegram[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
                    else: continue
                else:
                    console.print("[bold red]НЕУСПЕШНО.[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста, попробуйте еще раз.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 4: # Change ID
                console.print("[bold cyan][!] Введите свой новый ID.[/bold cyan]")
                new_id = Prompt.ask("[bold][?] ID[/bold]")
                console.print("[bold cyan][%] Сохранение ваших данных[/bold cyan]: ", end=None)
                if len(new_id) >= 2 and len(new_id) <= 50 and (' ' in new_id) == False:
                    if cpm.set_player_localid(new_id.upper()):
                        console.print("[bold green]УСПЕШНО.[/bold green]")
                        console.print("==================================")
                        answ = Prompt.ask("[bold cyan][?] Вы хотите выйти?[/bold cyan]", choices=["y", "n"], default="n")
                        if answ == "y": console.print(f"[bold yellow][!] Спасибо за использование нашего инструмента, присоединяйтесь к нашему каналу в Telegram[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
                        else: continue
                    else:
                        console.print("[bold red]НЕУСПЕШНО.[/bold red]")
                        console.print("[bold yellow][!] Пожалуйста, попробуйте еще раз.[/bold yellow]")
                        sleep(2)
                        continue
                else:
                    console.print("[bold red]НЕУСПЕШНО.[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста, используйте действительный ID.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 5: # Change Name
                console.print("[bold cyan][!] Введите свое новое имя.[/bold cyan]")
                new_name = Prompt.ask("[bold][?] Имя[/bold]")
                console.print("[bold cyan][%] Сохранение ваших данных[/bold cyan]: ", end=None)
                if len(new_name) >= 0 and len(new_name) <= 30:
                    if cpm.set_player_name(new_name):
                        console.print("[bold green]УСПЕШНО.[/bold green]")
                        console.print("==================================")
                        answ = Prompt.ask("[bold cyan][?] Вы хотите выйти?[/bold cyan]", choices=["y", "n"], default="n")
                        if answ == "y": console.print(f"[bold yellow][!] Спасибо за использование нашего инструмента, присоединяйтесь к нашему каналу в Telegram[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
                        else: continue
                    else:
                        console.print("[bold red]НЕУСПЕШНО.[/bold red]")
                        console.print("[bold yellow][!] Пожалуйста, попробуйте еще раз.[/bold yellow]")
                        sleep(2)
                        continue
                else:
                    console.print("[bold red]НЕУСПЕШНО.[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста, используйте допустимые значения.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 6: # Change Name Rainbow
                console.print("[bold cyan][!] Введите свое новое радужное имя.[/bold cyan]")
                new_name = Prompt.ask("[bold][?] Имя[/bold]")
                console.print("[bold cyan][%] Сохранение ваших данных[/bold cyan]: ", end=None)
                if len(new_name) >= 0 and len(new_name) <= 30:
                    if cpm.set_player_name(rainbow_gradient_string(new_name)):
                        console.print("[bold green]УСПЕШНО.[/bold green]")
                        console.print("==================================")
                        answ = Prompt.ask("[bold cyan][?] Вы хотите выйти?[/bold cyan]", choices=["y", "n"], default="n")
                        if answ == "y": console.print(f"[bold yellow][!] Спасибо за использование нашего инструмента, присоединяйтесь к нашему каналу в Telegram[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
                        else: continue
                    else:
                        console.print("[bold red]НЕУСПЕШНО.[/bold red]")
                        console.print("[bold yellow][!] Пожалуйста, попробуйте еще раз.[/bold yellow]")
                        sleep(2)
                        continue
                else:
                    console.print("[bold red]НЕУСПЕШНО.[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста, используйте действительные значения.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 7: # Number Plates
                console.print("[bold cyan][%] Даем вам номерные знаки[/bold cyan]: ", end=None)
                if cpm.set_player_plates():
                    console.print("[bold green]УСПЕШНО.[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold cyan][?] Вы хотите выйти ?[/bold cyan]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"[bold yellow][!] Спасибо за использование нашего инструмента, присоединяйтесь к нашему каналу в Telegram[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
                    else: continue
                else:
                    console.print("[bold red]НЕУСПЕШНО.[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста, попробуйте еще раз.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 8: # Account Delete
                console.print("[bold cyan][!] После удаления аккаунта пути назад не будет!![/bold cyan]")
                answ = Prompt.ask("[bold cyan][?] Вы хотите удалить этот аккаунт?![/bold cyan]", choices=["y", "n"], default="n")
                if answ == "y":
                    cpm.delete()
                    console.print("[bold cyan][%] Удаление вашей учетной записи[/bold cyan]: [bold green]УСПЕШНО.[/bold green].")
                    console.print("==================================")
                    console.print(f"[bold yellow][!] Спасибо за использование нашего инструмента, присоединяйтесь к нашему каналу в Telegram[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
                else: continue
            elif service == 9: # Account Register
                console.print("[bold cyan][!] Регистрация новой учетной записи.[/bold cyan]")
                acc2_email = prompt_valid_value("[bold][?] Электронная почта аккаунта[/bold]", "Электронная почта", password=False)
                acc2_password = prompt_valid_value("[bold][?] Пароль учетной записи[/bold]", "Пароль", password=False)
                console.print("[bold cyan][%] Создание новой учетной записи[/bold cyan]: ", end=None)
                status = cpm.register(acc2_email, acc2_password)
                if status == 0:
                    console.print("[bold green]УСПЕШНО.[/bold green]")
                    console.print("==================================")
                    console.print(f"[bold red]! ИНФОРМАЦИЯ[/bold red]: Чтобы настроить этот аккаунт с помощью CarParkTool")
                    console.print("Вы чаще всего входите в игру, используя эту учетную запись.")
                    sleep(2)
                    continue
                elif status == 105:
                    console.print("[bold red]НЕУСПЕШНО.[/bold red]")
                    console.print("[bold yellow][!] Этот адрес электронной почты уже существует![/bold yellow]")
                    sleep(2)
                    continue
                else:
                    console.print("[bold red]НЕУСПЕШНО.[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста, попробуйте еще раз.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 10: # Delete Friends
                console.print("[bold cyan][%] Удаление друзей[/bold cyan]: ", end=None)
                if cpm.delete_player_friends():
                    console.print("[bold green]УСПЕШНО.[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold cyan][?] Вы хотите выйти? ?[/bold cyan]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"[bold yellow][!] Спасибо за использование нашего инструмента, присоединяйтесь к нашему каналу в Telegram[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
                    else: continue
                else:
                    console.print("[bold red]НЕУСПЕШНО.[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста, попробуйте еще раз.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 11: # Unlock All Paid Cars
                console.print("[bold yellow]! Примечание[/bold yellow]: Выполнение этой функции займет некоторое время, пожалуйста, не отменяйте ее.", end=None)
                console.print("[bold cyan][%] Разблокировка всех платных автомобилей[/bold cyan]: ", end=None)
                if cpm.unlock_paid_cars():
                    console.print("[bold green]УСПЕШНО.[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold cyan][?] Вы хотите выйти? ?[/bold cyan]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"[bold yellow][!] Спасибо за использование нашего инструмента, присоединяйтесь к нашему каналу в Telegram[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
                    else: continue
                else:
                    console.print("[bold red]НЕУСПЕШНО.[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста, попробуйте еще раз.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 12: # Unlock All Cars
                console.print("[bold cyan][%] Разблокировка всех автомобилей[/bold cyan]: ", end=None)
                if cpm.unlock_all_cars():
                    console.print("[bold green]УСПЕШНО.[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold cyan][?] Вы хотите выйти?[/bold cyan]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"[bold yellow][!] Спасибо за использование нашего инструмента, присоединяйтесь к нашему каналу в Telegram[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
                    else: continue
                else:
                    console.print("[bold red]НЕУСПЕШНО.[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста, попробуйте еще раз.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 13: # Unlock All Cars Siren
                console.print("[bold cyan][%] Разблокировка всех автомобилей сирена[/bold cyan]: ", end=None)
                if cpm.unlock_all_cars_siren():
                    console.print("[bold green]УСПЕШНО.[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold cyan][?] Вы хотите выйти?[/bold cyan]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"[bold yellow][!] Спасибо за использование нашего инструмента, присоединяйтесь к нашему каналу в Telegram[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
                    else: continue
                else:
                    console.print("[bold red]НЕУСПЕШНО.[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста, попробуйте еще раз.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 14: # Unlock w16 Engine
                console.print("[bold cyan][%] Разблокировка двигателя w16[/bold cyan]: ", end=None)
                if cpm.unlock_w16():
                    console.print("[bold green]УСПЕШНО.[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold cyan][?] Вы хотите выйти ?[/bold cyan]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"[bold yellow][!] Спасибо за использование нашего инструмента, присоединяйтесь к нашему каналу в Telegram[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
                    else: continue
                else:
                    console.print("[bold red]НЕУСПЕШНО.[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста, попробуйте еще раз.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 15: # Unlock All Horns
                console.print("[bold cyan][%] Разблокировка всех гудков[/bold cyan]: ", end=None)
                if cpm.unlock_horns():
                    console.print("[bold green]УСПЕШНО.[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold cyan][?] Вы хотите выйти ?[/bold cyan]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"[bold yellow][!] Спасибо за использование нашего инструмента, присоединяйтесь к нашему каналу в Telegram[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
                    else: continue
                else:
                    console.print("[bold red]НЕУСПЕШНО.[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста, попробуйте еще раз.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 16: # Disable Engine Damage
                console.print("[bold cyan][%] Разблокировка Отключения Повреждение[/bold cyan]: ", end=None)
                if cpm.disable_engine_damage():
                    console.print("[bold green]УСПЕШНО.[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold cyan][?] Вы хотите выйти ?[/bold cyan]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"[bold yellow][!] Спасибо за использование нашего инструмента, присоединяйтесь к нашему каналу в Telegram[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
                    else: continue
                else:
                    console.print("[bold red]НЕУСПЕШНО.[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста, попробуйте еще раз.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 17: # Unlimited Fuel
                console.print("[bold cyan][%] Разблокировка неограниченного топлива[/bold cyan]: ", end=None)
                if cpm.unlimited_fuel():
                    console.print("[bold green]УСПЕШНО.[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold cyan][?] Вы хотите выйти ?[/bold cyan]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"[bold yellow][!] Спасибо за использование нашего инструмента, присоединяйтесь к нашему каналу в Telegram[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
                    else: continue
                else:
                    console.print("[bold red]НЕУСПЕШНО.[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста, попробуйте еще раз.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 18: # Unlock House 3
                console.print("[bold cyan][%] Разблокировка дома 3[/bold cyan]: ", end=None)
                if cpm.unlock_houses():
                    console.print("[bold green]УСПЕШНО.[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold cyan][?] Вы хотите выйти?[/bold cyan]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"[bold yellow][!] Спасибо за использование нашего инструмента, присоединяйтесь к нашему каналу в Telegram[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
                    else: continue
                else:
                    console.print("[bold red]НЕУСПЕШНО.[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста, попробуйте еще раз.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 19: # Unlock Smoke
                console.print("[bold cyan][%] Разблокировка дыма[/bold cyan]: ", end=None)
                if cpm.unlock_smoke():
                    console.print("[bold green]УСПЕШНО.[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold cyan][?] Вы хотите выйти ?[/bold cyan]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"[bold yellow][!] Спасибо за использование нашего инструмента, присоединяйтесь к нашему каналу в Telegram[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
                    else: continue
                else:
                    console.print("[bold red]НЕУСПЕШНО.[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста, попробуйте еще раз.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 20: # Change Races Wins
                console.print("[bold cyan][!] Укажите, сколько гонок вы выиграли.[/bold cyan]")
                amount = IntPrompt.ask("[bold][?] Количество[/bold]")
                console.print("[bold cyan][%] Изменение ваших данных[/bold cyan]: ", end=None)
                if amount > 0 and amount <= 10000000:
                    if cpm.set_player_wins(amount):
                        console.print("[bold green]УСПЕШНО.[/bold green]")
                        console.print("==================================")
                        answ = Prompt.ask("[bold cyan][?] Вы хотите выйти ?[/bold cyan]", choices=["y", "n"], default="n")
                        if answ == "y": console.print(f"[bold yellow][!] Спасибо за использование нашего инструмента, присоединяйтесь к нашему каналу в Telegram[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
                        else: continue
                    else:
                        console.print("[bold red]НЕУСПЕШНО.[/bold red]")
                        console.print("[bold yellow][!] Пожалуйста, попробуйте еще раз.[/bold yellow]")
                        sleep(2)
                        continue
                else:
                    console.print("[bold red]НЕУСПЕШНО.[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста, используйте допустимые значения.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 21: # Change Races Loses
                console.print("[bold cyan][!] Укажите, сколько гонок вы проиграли.[/bold cyan]")
                amount = IntPrompt.ask("[bold][?] Количество[/bold]")
                console.print("[bold cyan][%] Изменение ваших данных[/bold cyan]: ", end=None)
                if amount > 0 and amount <= 10000000:
                    if cpm.set_player_loses(amount):
                        console.print("[bold green]УСПЕШНО.[/bold green]")
                        console.print("==================================")
                        answ = Prompt.ask("[bold cyan][?] Вы хотите выйти ?[/bold cyan]", choices=["y", "n"], default="n")
                        if answ == "y": console.print(f"[bold yellow][!] Спасибо за использование нашего инструмента, присоединяйтесь к нашему каналу в Telegram[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
                        else: continue
                    else:
                        console.print("[bold red]НЕУСПЕШНО.[/bold red]")
                        console.print("[bold yellow][!] Пожалуйста, попробуйте еще раз.[/bold yellow]")
                        sleep(2)
                        continue
                else:
                    console.print("[bold red]НЕУСПЕШНО.[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста, используйте допустимые значения.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 22: # Clone Account
                console.print("[bold cyan]Пожалуйста, введите данные учетной записи[/bold cyan]:")
                to_email = prompt_valid_value("[bold][?] Электронная почта аккаунта[/bold]", "Электронная почта", password=False)
                to_password = prompt_valid_value("[bold][?] Пароль учетной записи[/bold]", "Пароль", password=False)
                console.print("[bold cyan][%] Клонирование вашего аккаунта[/bold cyan]: ", end=None)
                if cpm.account_clone(to_email, to_password):
                    console.print("[bold green]УСПЕШНО.[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold cyan][?] Вы хотите выйти ?[/bold cyan]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"[bold yellow][!] Спасибо за использование нашего инструмента, присоединяйтесь к нашему каналу в Telegram[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
                    else: continue
                else:
                    console.print("[bold red]НЕУСПЕШНО.[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста, попробуйте еще раз.[/bold yellow]")
                    sleep(2)
                    continue
            else: continue
            break
        break
