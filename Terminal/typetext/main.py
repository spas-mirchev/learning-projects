from tkinter import *
import random
import time

with open('script.txt', 'r') as fr:
    content = fr.readlines()

text = random.choice(content).replace(',', '').replace('.', '').lower()

running = False


def start_timer():
    global running
    if not running:
        chronometar()
        running = True


def chronometar():
    if time_var.get() > 0:
        time_var.set(time_var.get()-1)
        time_entry.after(1000, chronometar)
        running = True
    else:
        stop_writing()


def stop_writing():
    final_string = e_var.get()
    cpm = len(final_string)
    wpm = len(final_string.split())
    original_text = text[:cpm]
    main_field.delete('1.0', 'end')
    entry_text.delete(0, 'end')
    entry_text.config(state='disabled')
    time.sleep(2)

    faults = [final_string.find(final_string[i], i) for i in range(
        cpm) if (original_text[i] != final_string[i])]
    main_field.insert(
        '1.0', f'{final_string}\n{text[:len(final_string)]}')
    main_field.config(state='disabled')
    for i in faults:
        f_index = '1.' + str(i)
        next_index = '1.' + str(i+1)
        main_field.tag_add("fault", f_index, next_index)
        main_field.tag_config("fault", foreground="red",)

    cpm_entry.insert(0, cpm)
    wpm_entry.insert(0, wpm)

    with open('score.txt', 'r+') as fs:
        best_score = fs.read()
        if int(wpm_entry.get()) > int(best_score):
            fs.seek(0)
            fs.write(wpm_entry.get())
            best_score = wpm_entry.get()
    overall.config(
        text=f'You wrote {wpm} words per minute. You have only {len(faults)} mistakes.  Your best score is {best_score} ')


def restart():
    global running
    global faults
    global text

    text = random.choice(content)
    running = False
    faults = []
    main_field.config(state='normal')
    main_field.delete('1.0', 'end')
    main_field.insert('1.0', text)
    first_word_bg()
    cpm_entry.delete(0, 'end')
    wpm_entry.delete(0, 'end')
    time_entry.delete(0, 'end')
    entry_text.delete(0, 'end')
    entry_text.config(state='normal')
    time_var.set(60)


def first_word_bg():
    first_word_bg = '1.' + str(text.find(' '))
    main_field.tag_add("first_word", '1.0', first_word_bg)
    main_field.tag_config("first_word", background="cyan3",
                          foreground="black",)


test = 't'


def on_key(var, mode, callback):
    global test
    #print("Traced variable is {}".format(e_var.get()))

    start_timer()
    start_index = '1.' + str(int(len(e_var.get())-1))
    current_index = int(len(e_var.get())-1)
    next_index = '1.' + str(len(e_var.get()))
    ext_index = '1.' + str(len(test))

    if text[current_index] == e_var.get()[-1]:
        main_field.tag_delete('back')
        main_field.tag_add("here", start_index, next_index)
        main_field.tag_config("here", foreground="white",)

    elif text[current_index] != e_var.get()[-1]:

        main_field.tag_add("there", start_index, next_index)
        main_field.tag_config("there", foreground="red",)

        if e_var.get()[-1] == " ":
            e_var.set(e_var.get()[:-1] + '_')

    if text[current_index] == ' ':
        next_space = next_index + 'wordend'
        main_field.tag_add("space", next_index, next_space)
        main_field.tag_config("space",  background="cyan3")

    if len(test) > len(e_var.get()):
        main_field.tag_remove('there', next_index, ext_index)

        main_field.tag_add("back", next_index, ext_index)

        main_field.tag_config("back", foreground="black",)

    test = e_var.get()


window = Tk()
window.title("Type speed checker")

e_var = StringVar()
time_var = IntVar(window, 20)

header = Label(
    text='How fast are your fingers? Do the one-minute typing test to find out!\nPress the space bar after each word.\nAt the end, you will get your typing speed in CPM and WPM. Good luck!', font=("Helvetica", 16), fg='indigo')

header.grid(row=0, column=1, columnspan=5, sticky=W, pady=20, padx=10)

cpm_label = Label(text='CPM: ', fg="navy blue",)
cpm_label.grid(row=1, column=0, sticky=E)

cpm_entry = Entry(width=5, font=("Helvetica", 16), fg="navy blue",)
cpm_entry.grid(row=1, column=1, sticky=W, pady=20)

wpm = Label(text='WPM: ', fg="navy blue",)
wpm.grid(row=1, column=2, sticky=E)

wpm_entry = Entry(width=5, font=("Helvetica", 16), fg="navy blue",)
wpm_entry.grid(row=1, column=3, sticky=W, pady=10)

time_left = Label(text='Time left: ', fg="navy blue",)
time_left.grid(row=1, column=4, sticky=E)

time_entry = Entry(width=5, font=("Helvetica", 16),
                   fg="navy blue", textvariable=time_var)
time_entry.grid(row=1, column=5, sticky=W, pady=10)

restart = Button(text='Restart', font=(
    "Helvetica", 14), bg='azure2', fg='firebrick1', relief='groove', command=restart)
restart.grid(row=4, column=5, sticky=E, pady=30)

main_field = Text(height=12, width=60, padx=10, pady=10, highlightthickness=0, wrap=WORD,
                  fg="navy blue", borderwidth=4, relief='groove', font=("Mohave", 22,))
main_field.insert('1.0', text)
main_field.grid(row=2, column=0, columnspan=7, padx=10, pady=10)
# first word background
first_word_bg()

entry_text = Entry(width=60, font=("Helvetica", 22), textvariable=e_var)
entry_text.grid(row=3, column=0, columnspan=6,  pady=10)

overall = Label(
    text='', font=("Helvetica", 16), fg='indigo',)
overall.grid(row=4, column=0, columnspan=6,  pady=30)

e_var.trace_add("write", on_key)

window.mainloop()
