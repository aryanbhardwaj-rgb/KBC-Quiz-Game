import tkinter as tk
from PIL import Image, ImageTk
import random
import pygame
import threading
import os

PRIZES = [
    1000, 2000, 3000, 5000, 10000,
    20000, 40000, 80000, 160000, 320000,
    640000, 1250000, 2500000, 5000000, 10000000, 70000000
]
SAFE_HAVENS = [4, 9]
QUESTIONS = [
    {"question": "If you rearrange the letters 'CIFAIPC' you get the name of a:", "options": ["River", "Country", "City", "Ocean"], "answer": 3},
    {"question": "I speak without a mouth and hear without ears. I have nobody, but I come alive with wind. What am I?", "options": ["Echo", "Shadow", "Cloud", "Fire"], "answer": 0},
    {"question": "What comes once in a minute, twice in a moment, but never in a thousand years?", "options": ["The letter M", "A second", "The letter N", "Time"], "answer": 0},
    {"question": "A farmer has 17 sheep, all but 9 die. How many are left alive?", "options": ["8", "9", "17", "None"], "answer": 1},
    {"question": "Which word in the dictionary is spelled incorrectly?", "options": ["Incorrectly", "Wrongly", "Unfairly", "Mistakenly"], "answer": 0},
    {"question": "I have keys but no locks, I have space but no rooms. You can enter, but you cannot go outside. What am I?", "options": ["Piano", "Keyboard", "House", "Car"], "answer": 1},
    {"question": "What is always in front of you but can’t be seen?", "options": ["Future", "Air", "Night", "Shadow"], "answer": 0},
    {"question": "What has many teeth but can’t bite?", "options": ["Comb", "Shark", "Saw", "Zipper"], "answer": 0},
    {"question": "They come at night without being called and are lost in the day without being stolen. What are they?", "options": ["Stars", "Dreams", "Shadows", "Ghosts"], "answer": 0},
    {"question": "What has to be broken before you can use it?", "options": ["Egg", "Glass", "Secret", "Code"], "answer": 0},
    {"question": "I’m tall when I’m young and short when I’m old. What am I?", "options": ["Candle", "Mountain", "Shadow", "Tree"], "answer": 0},
    {"question": "What has lots of rings but no fingers?", "options": ["Tree", "Phone", "Saturn", "Chain"], "answer": 2},
    {"question": "What begins with T, ends with T, and has T in it?", "options": ["Teapot", "Tent", "Toast", "Tart"], "answer": 0},
    {"question": "What can’t talk but will reply when spoken to?", "options": ["Echo", "Shadow", "Phone", "Parrot"], "answer": 0},
    {"question": "What invention lets you look right through a wall?", "options": ["Window", "Door", "Mirror", "Television"], "answer": 0},
    {"question": "What can travel around the world while staying in one spot?", "options": ["Postage stamp", "Plane", "Satellite", "Flag"], "answer": 0},
]
FLIP_QUESTIONS = [
    {"question": "I shave every day, but my beard stays the same. What am I?", "options": ["Barber", "Statue", "Actor", "Sheep"], "answer": 0},
    {"question": "The more of this there is, the less you see. What is it?", "options": ["Darkness", "Fog", "Light", "Snow"], "answer": 0},
]

def create_styled_popup(title, message):
    def popup():
        win = tk.Toplevel()
        win.title(title)
        win.configure(bg="#291C5A")
        win.geometry("430x290")
        win.resizable(0, 0)
        lbl = tk.Label(win, text=message, font=("Segoe UI", 15, "bold"), fg="#FFD700", bg="#291C5A", justify="center", wraplength=395)
        lbl.place(relx=0.5, rely=0.38, anchor='center')
        btn = tk.Button(win, text="OK", font=("Arial", 12, "bold"), bg="#FFD700", fg="#291C5A", command=win.destroy, width=11, bd=2, relief="ridge", activebackground="#FEFFB9")
        btn.place(relx=0.5, rely=0.71, anchor='center')
        win.grab_set()
        win.focus_force()
    return popup

class KBCQuiz(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("KBC QUIZ GAME")
        self.geometry("950x635")
        self.configure(bg="#291C5A")
        self.resizable(True, True)
        pygame.mixer.init()
        self.audio_loaded = False
        self.audio_file = os.path.join("audio.mp3")
        try:
            pygame.mixer.music.load(self.audio_file)
            self.audio_loaded = True
        except Exception as e:
            print("Audio not loaded:", e)
        self.after(200, self.create_start_screen)

    def create_start_screen(self):
        self.start_screen = tk.Frame(self, bg="#291C5A")
        self.start_screen.pack(fill="both", expand=True)
        img_path = os.path.join("assets", "screen.jpg")
        try:
            splash_img = Image.open(img_path).resize((800, 450))
            self.start_img = ImageTk.PhotoImage(splash_img)
        except Exception:
            self.start_img = None
        if self.start_img:
            tk.Label(self.start_screen, image=self.start_img, bg="#291C5A").place(relx=0.5, rely=0.38, anchor="center")
        tk.Label(self.start_screen, text="Welcome to Kaun Banega Crorepati", font=("Arial Black", 28), fg="#FFD700", bg="#291C5A").place(relx=0.5, rely=0.69, anchor="center")
        start_btn = tk.Button(self.start_screen, text="Start Quiz", font=("Arial Black", 18), bg="#FFD700", fg="#2D1679", command=self.start_game)
        start_btn.place(relx=0.5, rely=0.79, anchor="center", width=180, height=50)
        if self.audio_loaded:
            threading.Thread(target=self.start_audio, daemon=True).start()

    def start_audio(self):
        try:
            pygame.mixer.music.play(-1)
        except Exception:
            pass

    def stop_audio(self):
        try:
            pygame.mixer.music.stop()
        except Exception:
            pass

    def start_game(self):
        self.stop_audio()
        self.start_screen.destroy()
        self.init_quiz_vars()
        self.create_quiz_screen()
        self.display_question()

    def init_quiz_vars(self):
        self.current = 0
        self.winnings = 0
        self.selected = tk.IntVar()
        self.lifelines = {'5050': True, "audience": True, "phone": True, "flip": True}
        self.flip_used = False
        self.used_flip_questions = set()
        self.questions = QUESTIONS.copy()
        self.timer_label = None
        self.countdown_id = None
        self.time_left = 0
        self.fullscreen = False

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self.attributes("-fullscreen", self.fullscreen)
    def minimize_window(self):
        self.iconify()

    def create_quiz_screen(self):
        self.quiz_screen = tk.Frame(self, bg="#3C1581")
        self.quiz_screen.pack(fill='both', expand=True)

        controlbar = tk.Frame(self.quiz_screen, bg="#232072")
        controlbar.pack(fill="x")
        tk.Button(controlbar, text="🗖 Full Screen", font=("Arial", 12, "bold"), bg="#FFD700", fg="#202020", command=self.toggle_fullscreen).pack(side="right", padx=7, pady=6)
        tk.Button(controlbar, text="— Minimize", font=("Arial", 12, "bold"), bg="#FFD700", fg="#202020", command=self.minimize_window).pack(side="right", padx=7, pady=6)

        center_frame = tk.Frame(self.quiz_screen, bg="#3C1581")
        center_frame.place(relx=0.22, rely=0.05, relwidth=0.56, relheight=0.90)
        sidebar = tk.Frame(self.quiz_screen, bg="#3C1581")
        sidebar.place(relx=0.80, rely=0.06, relwidth=0.18, relheight=0.84)
        if not hasattr(self, 'logo'):
            try:
                img = Image.open("kbc_logo.png").resize((95, 95))
                self.logo = ImageTk.PhotoImage(img)
            except Exception:
                self.logo = None
        if self.logo:
            tk.Label(center_frame, image=self.logo, bg="#3C1581").pack(anchor="n", pady=(5, 0))
        tk.Label(center_frame, text="KAUN BANEGA CROREPATI", font=("Arial Black", 30, "bold"), fg="#FFD700", bg="#3C1581").pack(anchor="n", pady=(10, 18))
        lifeline_frame = tk.Frame(center_frame, bg="#3C1581")
        lifeline_frame.pack(anchor="n", pady=(0, 8))
        self.lifeline_buttons = []
        lifeline_names = [("50:50", self.use_5050), ("Audience Poll", self.audience_poll), ("Phone a Friend", self.phone_friend), ("Flip Ques.", self.flip_question)]
        for txt, cmd in lifeline_names:
            btn = tk.Button(lifeline_frame, text=txt, command=cmd, font=('Arial', 12, 'bold'), bg='#FDF6AE', fg="#28318C", activebackground='#FFD700', width=12, relief="ridge", bd=3, cursor="hand2")
            btn.pack(side='left', padx=7)
            self.lifeline_buttons.append(btn)
        self.q_label = tk.Label(center_frame, text="", wraplength=560, justify="center", font=("Segoe UI Bold", 20), bg="#3C1581", fg="#fff")
        self.q_label.pack(anchor="n", pady=(14, 0))
        self.opt_buttons = []
        for i in range(4):
            btn = tk.Radiobutton(center_frame, text="", variable=self.selected, value=i, font=("Arial", 14, "bold"), indicatoron=0,
                                 width=25, height=2, bg="#472689", fg="#FFD700", selectcolor="#64ffda",
                                 activebackground="#1f0993", activeforeground="#fff", cursor="hand2")
            btn.pack(anchor="center", pady=8)
            self.opt_buttons.append(btn)
        self.lock_btn = tk.Button(center_frame, text="Lock Kar Diya Jaye", command=self.lock_answer,
                                  font=("Arial Black", 17), bg="#FFD700", fg="#1f1446", bd=5, activebackground="#f0bb04", relief="raised", cursor="hand2")
        self.lock_btn.pack(anchor="center", pady=14)
        self.timer_label = tk.Label(sidebar, text="", font=("Arial Black", 22), fg="#FFD700", bg="#3C1581")
        self.timer_label.pack(anchor='n', pady=(5, 12))
        self.prizebox = tk.Listbox(sidebar, height=16, width=15, font=("Arial", 13, "bold"), bg="#232072", fg="white", highlightbackground="#FFD700", selectbackground="#FFD700", activestyle="none")
        for idx, val in enumerate(reversed(PRIZES)):
            self.prizebox.insert(tk.END, f"₹ {val:,}")
        self.prizebox.pack(fill='both', expand=True, pady=(10, 0))

    # ... (rest of your quiz/game logic remains unchanged)
    def display_question(self):
        if self.countdown_id:
            self.after_cancel(self.countdown_id)
            self.countdown_id = None
        self.timer_label.config(text="")
        if self.current < 10:
            self.time_left = 45
            self.update_timer()
        else:
            self.timer_label.config(text="")
            self.time_left = 0
        if self.current >= len(self.questions):
            self.end_game(win=True)
            return
        q = self.questions[self.current]
        self.q_label.config(text=f"Q{self.current + 1}: {q['question']}")
        self.selected.set(-1)
        for i, btn in enumerate(self.opt_buttons):
            btn.config(text=q['options'][i], state=tk.NORMAL, bg="#472689")
        self.prizebox.selection_clear(0, tk.END)
        self.prizebox.selection_set(15 - self.current)
        for btn in self.lifeline_buttons:
            btn.config(state=tk.NORMAL)
        for name, i in zip(['5050', 'audience', 'phone', 'flip'], range(4)):
            if not self.lifelines[name]:
                self.lifeline_buttons[i].config(state=tk.DISABLED)
        self.flip_used = False

    def update_timer(self):
        if self.time_left > 0:
            self.timer_label.config(text=f"⏱ {self.time_left}s")
            self.time_left -= 1
            self.countdown_id = self.after(1000, self.update_timer)
        else:
            if self.current < 10:
                self.timer_label.config(text="Time's up!")
                for btn in self.opt_buttons:
                    btn.config(state=tk.DISABLED)
                popup = create_styled_popup("Time Up!", "Your time for this question has ended!\nYou take home your guaranteed winnings.")
                popup()
                self.end_game(win=False)

    def use_5050(self):
        if self.lifelines['5050']:
            q = self.questions[self.current]
            indices = [i for i in range(4) if i != q['answer']]
            remove_two = random.sample(indices, 2)
            for idx in remove_two:
                self.opt_buttons[idx].config(state=tk.DISABLED)
            self.lifelines['5050'] = False
            self.lifeline_buttons.config(state=tk.DISABLED)

    def audience_poll(self):
        if not self.lifelines["audience"]: return
        q = self.questions[self.current]
        correct_idx = q['answer']
        correct_pct = random.randint(50, 70)
        remaining = [random.randint(0, 100 - correct_pct) for _ in range(3)]
        while sum(remaining) + correct_pct != 100:
            idx = random.choice([0,1,2])
            remaining[idx] += 1 if sum(remaining) + correct_pct < 100 else -1
        poll = [0,0,0,0]
        widx = 0
        for i in range(4):
            if i == correct_idx:
                poll[i] = correct_pct
            else:
                poll[i] = remaining[widx]
                widx += 1
        abcd = "ABCD"
        result_text = ""
        for i, percent in enumerate(poll):
            result_text += f"{abcd[i]}. {q['options'][i]} : {percent}%\n"
        popup = create_styled_popup("AUDIENCE POLL", result_text)
        popup()
        self.lifelines["audience"] = False
        self.lifeline_buttons.config(state=tk.DISABLED)

    def phone_friend(self):
        if not self.lifelines["phone"]: return
        q = self.questions[self.current]
        correct_idx = q['answer']
        suggested_idx = correct_idx if random.random() < 0.75 else random.randint(0,3)
        msg = f"Your friend thinks the answer is:\n\n{q['options'][suggested_idx]}"
        popup = create_styled_popup("PHONE A FRIEND", msg)
        popup()
        self.lifelines["phone"] = False
        self.lifeline_buttons.config(state=tk.DISABLED)

    def flip_question(self):
        if not self.lifelines["flip"]: return
        flip_qs = [q for i, q in enumerate(FLIP_QUESTIONS) if i not in self.used_flip_questions]
        if not flip_qs:
            popup = create_styled_popup("No Flips", "No flip questions left!")
            popup()
            return
        new_q = flip_qs
        self.used_flip_questions.add(FLIP_QUESTIONS.index(new_q))
        self.questions[self.current] = new_q
        self.flip_used = True
        self.lifelines["flip"] = False
        self.lifeline_buttons.config(state=tk.DISABLED)
        self.display_question()

    def lock_answer(self):
        if self.countdown_id:
            self.after_cancel(self.countdown_id)
            self.countdown_id = None
        val = self.selected.get()
        if val == -1:
            popup = create_styled_popup("No Selection", "Choose an option to lock!")
            popup()
            return
        correct = self.questions[self.current]['answer']
        for idx, btn in enumerate(self.opt_buttons):
            if idx == correct:
                btn.config(bg="#27e18f")
            elif idx == val:
                btn.config(bg="#ff4e53")
        self.after(1100, lambda: self.evaluate_answer(val, correct))

    def evaluate_answer(self, val, correct):
        if val == correct:
            self.winnings = PRIZES[self.current]
            self.current += 1
            self.display_question()
        else:
            self.end_game(win=False)

    def fallback_amount(self):
        for sh in reversed(SAFE_HAVENS):
            if self.current > sh:
                return PRIZES[sh]
        return 0

    def end_game(self, win=False):
        if win:
            msg = f"Congratulations!\n\nYou WON ₹{self.winnings:,}!"
            popup = create_styled_popup("CONGRATULATIONS!", msg)
            popup()
        else:
            msg = f"Game Over!\n\nYou take home ₹{self.fallback_amount():,}."
            popup = create_styled_popup("GAME OVER", msg)
            popup()
        self.after(100, self.close_if_needed)

    def close_if_needed(self):
        pass

if __name__ == "__main__":
    app = KBCQuiz()
    app.mainloop()
