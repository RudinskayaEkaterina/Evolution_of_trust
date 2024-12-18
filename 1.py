import tkinter as tk
from tkinter import messagebox
import random

root = tk.Tk()
root.title("Эволюция Доверия")
root.geometry("900x600")

user_score = 0
computer_score = 0
last_user_choice = None
computer_strategy= ["Всегда Сотрудничает", "Всегда Мухлюет", "Подражает"]
computer_strategy = random.choice(computer_strategy)
rounds_played = 0

button_frame = tk.Frame(root)
button_frame.pack(side="bottom", pady=10)

score_label = tk.Label(root, text=f"Очки пользователя: {user_score} | Очки компьютера: {computer_score}")
score_label.pack(pady=10)

start_image = tk.PhotoImage(file="./begin.png")
start_label = tk.Label(root, image=start_image)
start_label.image = start_image
start_label.pack(pady=10)

def rules():
    rules_window = tk.Toplevel(root)
    rules_window.title("Правила")
    rules_window.geometry("500x300")
    
    label = tk.Label(rules_window, text="Добро пожаловать в Эволюцию Доверия!\nВ этой игре у тебя два выбора - положить монетку в машинку перед тобой,\nлибо же не делать этого. У твоего противиника-компьютера такой же выбор.\nНе зависимо от того, положил ли ты монетку в машину, либо компьютер,\nлибо вы оба, либо же никто из вас, в машине появятся две дополнительные монетки\nкоторые разделятся между вами в зависимости от того, кто какой выбор сделал.\n Цель игры - угадать, какой стратегией пользовался компьютер,\nа также получить как можно больше монеток.\n \n Удачи!")
    label.pack(pady=20)

    close_button = tk.Button(rules_window, text="Хорошо!", command=rules_window.destroy)
    close_button.pack(pady=10)

def image_score(user_choice, computer_choice):
    global user_score, computer_score

    if user_choice == "Сотрудничать" and computer_choice == "Сотрудничать":
        user_score += 2
        computer_score += 2
        image = "./coopcoop.png"
    elif user_choice == "Сотрудничать" and computer_choice == "Мухлевать":
        user_score -= 1
        computer_score += 3
        image = "./coopcheat.png"
    elif user_choice == "Мухлевать" and computer_choice == "Сотрудничать":
        user_score += 3
        computer_score -= 1
        image = "./cheatcoop.png"
    elif user_choice == "Мухлевать" and computer_choice == "Мухлевать":
        image = "./cheatcheat.png"

    for widget in root.winfo_children():
        if isinstance(widget, tk.Label) and widget != score_label:
            widget.destroy()

    user_image = tk.PhotoImage(file=image)
    user_label = tk.Label(root, image=user_image)
    user_label.image = user_image
    user_label.pack(pady=10)
    score_label.config(text=f"Очки пользователя: {user_score} | Очки компьютера: {computer_score}")

def computer_choice_func():
    global last_user_choice, computer_strategy
    
    if computer_strategy == "Всегда Сотрудничает":
        return "Сотрудничать"
    elif computer_strategy == "Всегда Мухлюет":
        return "Мухлевать"
    elif computer_strategy == "Подражает":
        return last_user_choice if last_user_choice else "Сотрудничать"

def click(user_choice):
    global last_user_choice, rounds_played
    
    if rounds_played < 5:
        comp_choice = computer_choice_func()
        image_score(user_choice, comp_choice)
        last_user_choice = user_choice
        rounds_played += 1
    else:
        guess_strategy()

def guess_strategy():
    for widget in root.winfo_children():
        if not isinstance(widget, tk.Frame):
            widget.destroy()
    button_coop.destroy()
    button_cheat.destroy()

    label = tk.Label(root, text="Какая была стратегия компьютера?")
    label.pack(pady=10)

    button_always_coop = tk.Button(root, text="Всегда Сотрудничает", command=lambda: check("Всегда Сотрудничает"))
    button_always_coop.pack(pady=5)

    button_always_cheat = tk.Button(root, text="Всегда Мухлюет", command=lambda: check("Всегда Мухлюет"))
    button_always_cheat.pack(pady=5)

    button_copycat = tk.Button(root, text="Подражает", command=lambda: check("Подражает"))
    button_copycat.pack(pady=5)

def check(guess):
    if guess == computer_strategy:
        messagebox.showinfo("Результат", "Поздравляю! Вы угадали стратегию!")
    elif computer_strategy == "Всегда Сотрудничает":
        messagebox.showinfo(f"Результат", "Вы не угадали. Стратегия была: Всегда Сотрудничает")
    elif computer_strategy == "Всегда Мухлюет":
        messagebox.showinfo(f"Результат", "Вы не угадали. Стратегия была: Всегда Мухлюет")
    else:
        messagebox.showinfo(f"Результат", "Вы не угадали. Стратегия была: Подражает")
    root.quit()

def log_results():
    with open("log.txt") as log_file:
        if user_score > computer_score:
            return "Победа"
        elif user_score < computer_score:
            return "Поражение"
        else:
            return "Ничья"
    log_file.write(f"Конечный счет: Пользователь {user_score} - Компьютер {computer_score}. Результат: {result}\n")

button_coop = tk.Button(button_frame, text="Сотрудничать", command=lambda: click("Сотрудничать"))
button_coop.pack(side="left", padx=5)

button_cheat = tk.Button(button_frame, text="Мухлевать", command=lambda: click("Мухлевать"))
button_cheat.pack(side="right", padx=5)

button_rules = tk.Button(button_frame, text="Правила", command=rules)
button_rules.pack(side="bottom", padx=5)

root.mainloop()
