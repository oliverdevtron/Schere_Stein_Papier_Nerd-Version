import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os
from datetime import datetime

class RockPaperScissorsGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Schere, Stein, Papier - Deluxe Edition")
        self.root.geometry("800x600")
        self.root.configure(bg='#2c3e50')
        
        # Spiel-Status
        self.current_mode = None
        self.difficulty = "mittel"
        self.game_variant = "classic"  # classic oder nerd
        self.player1_score = 0
        self.player2_score = 0
        self.rounds_played = 0
        self.player1_name = "Spieler 1"
        self.player2_name = "Computer"
        
        # Highscore-Datei
        self.highscore_file = "highscores.json"
        self.load_highscores()
        
        # Spielregeln definieren
        self.classic_rules = {
            "Stein": ["Schere"],
            "Schere": ["Papier"], 
            "Papier": ["Stein"]
        }
        
        self.nerd_rules = {
            "Schere": ["Papier", "Echse"],
            "Papier": ["Stein", "Spock"],
            "Stein": ["Echse", "Schere"],
            "Echse": ["Spock", "Papier"],
            "Spock": ["Schere", "Stein"]
        }
        
        # Schwierigkeitsgrade für KI
        self.ai_strategies = {
            "leicht": self.ai_random,
            "mittel": self.ai_pattern,
            "schwer": self.ai_counter
        }
        
        # Spieler-Historie für KI-Strategien
        self.player_history = []
        
        self.create_main_menu()
        
    def load_highscores(self):
        """Lädt die Highscores aus der JSON-Datei"""
        try:
            if os.path.exists(self.highscore_file):
                with open(self.highscore_file, 'r') as f:
                    self.highscores = json.load(f)
            else:
                self.highscores = []
        except:
            self.highscores = []
    
    def save_highscores(self):
        """Speichert die Highscores in die JSON-Datei"""
        try:
            with open(self.highscore_file, 'w') as f:
                json.dump(self.highscores, f, indent=2)
        except:
            pass
    
    def add_highscore(self, name, score, mode, variant):
        """Fügt einen neuen Highscore hinzu"""
        self.highscores.append({
            "name": name,
            "score": score,
            "mode": mode,
            "variant": variant,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        
        # Nach Score sortieren (absteigend)
        self.highscores.sort(key=lambda x: x["score"], reverse=True)
        
        # Nur Top 5 behalten
        self.highscores = self.highscores[:5]
        self.save_highscores()
    
    def create_main_menu(self):
        """Erstellt das Hauptmenü"""
        # Alle Widgets löschen
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Titel
        title_frame = tk.Frame(self.root, bg='#2c3e50')
        title_frame.pack(pady=20)
        
        title = tk.Label(title_frame, text="SCHERE, STEIN, PAPIER", 
                        font=("Arial", 24, "bold"), fg='#ecf0f1', bg='#2c3e50')
        title.pack()
        
        subtitle = tk.Label(title_frame, text="Deluxe Edition", 
                           font=("Arial", 12), fg='#bdc3c7', bg='#2c3e50')
        subtitle.pack()
        
        # Hauptmenü-Buttons
        menu_frame = tk.Frame(self.root, bg='#2c3e50')
        menu_frame.pack(pady=30)
        
        buttons = [
            ("👤 vs 🤖 Mensch vs Computer", lambda: self.setup_game("human_vs_ai")),
            ("👤 vs 👤 Mensch vs Mensch", lambda: self.setup_game("human_vs_human")),
            ("🤖 vs 🤖 Computer vs Computer", lambda: self.setup_game("ai_vs_ai")),
            ("🏆 Highscores", self.show_highscores),
            ("⚙️ Einstellungen", self.show_settings),
            ("❌ Beenden", self.root.quit)
        ]
        
        for text, command in buttons:
            btn = tk.Button(menu_frame, text=text, command=command,
                          font=("Arial", 12), width=25, height=2,
                          bg='#3498db', fg='white', 
                          activebackground='#2980b9', activeforeground='white',
                          relief='flat', cursor='hand2')
            btn.pack(pady=5)
            
    def show_highscores(self):
        """Zeigt die Highscore-Tabelle"""
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Titel
        title = tk.Label(self.root, text="🏆 HIGHSCORES", 
                        font=("Arial", 20, "bold"), fg='#ecf0f1', bg='#2c3e50')
        title.pack(pady=20)
        
        # Highscore-Tabelle
        frame = tk.Frame(self.root, bg='#2c3e50')
        frame.pack(pady=20)
        
        if not self.highscores:
            no_scores = tk.Label(frame, text="Noch keine Highscores vorhanden!", 
                               font=("Arial", 14), fg='#bdc3c7', bg='#2c3e50')
            no_scores.pack()
        else:
            # Header
            header_frame = tk.Frame(frame, bg='#34495e')
            header_frame.pack(fill='x', padx=10, pady=5)
            
            headers = ["Rang", "Name", "Score", "Modus", "Variante", "Datum"]
            for i, header in enumerate(headers):
                lbl = tk.Label(header_frame, text=header, font=("Arial", 12, "bold"),
                             fg='white', bg='#34495e', width=12)
                lbl.grid(row=0, column=i, padx=5, pady=5)
            
            # Scores
            for i, score in enumerate(self.highscores):
                score_frame = tk.Frame(frame, bg='#ecf0f1' if i % 2 == 0 else '#bdc3c7')
                score_frame.pack(fill='x', padx=10, pady=2)
                
                values = [f"#{i+1}", score["name"], str(score["score"]), 
                         score["mode"], score["variant"], score["date"]]
                
                for j, value in enumerate(values):
                    lbl = tk.Label(score_frame, text=value, font=("Arial", 10),
                                 bg=score_frame['bg'], width=12)
                    lbl.grid(row=0, column=j, padx=5, pady=5)
        
        # Zurück-Button
        back_btn = tk.Button(self.root, text="← Zurück zum Hauptmenü", 
                           command=self.create_main_menu,
                           font=("Arial", 12), bg='#95a5a6', fg='white',
                           activebackground='#7f8c8d', activeforeground='white',
                           relief='flat', cursor='hand2')
        back_btn.pack(pady=20)
        
    def show_settings(self):
        """Zeigt die Einstellungen"""
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Titel
        title = tk.Label(self.root, text="⚙️ EINSTELLUNGEN", 
                        font=("Arial", 20, "bold"), fg='#ecf0f1', bg='#2c3e50')
        title.pack(pady=20)
        
        settings_frame = tk.Frame(self.root, bg='#2c3e50')
        settings_frame.pack(pady=20)
        
        # Schwierigkeitsgrad
        tk.Label(settings_frame, text="Schwierigkeitsgrad:", 
                font=("Arial", 14, "bold"), fg='#ecf0f1', bg='#2c3e50').pack(pady=(0,10))
        
        difficulty_frame = tk.Frame(settings_frame, bg='#2c3e50')
        difficulty_frame.pack(pady=10)
        
        difficulty_var = tk.StringVar(value=self.difficulty)
        difficulties = [("Leicht", "leicht"), ("Mittel", "mittel"), ("Schwer", "schwer")]
        
        for text, value in difficulties:
            rb = tk.Radiobutton(difficulty_frame, text=text, variable=difficulty_var,
                              value=value, font=("Arial", 12), fg='#ecf0f1', bg='#2c3e50',
                              selectcolor='#3498db', activebackground='#2c3e50',
                              activeforeground='#ecf0f1')
            rb.pack(side='left', padx=20)
        
        # Spielvariante
        tk.Label(settings_frame, text="Spielvariante:", 
                font=("Arial", 14, "bold"), fg='#ecf0f1', bg='#2c3e50').pack(pady=(20,10))
        
        variant_frame = tk.Frame(settings_frame, bg='#2c3e50')
        variant_frame.pack(pady=10)
        
        variant_var = tk.StringVar(value=self.game_variant)
        variants = [("Klassisch (3 Optionen)", "classic"), ("Nerd-Modus (5 Optionen)", "nerd")]
        
        for text, value in variants:
            rb = tk.Radiobutton(variant_frame, text=text, variable=variant_var,
                              value=value, font=("Arial", 12), fg='#ecf0f1', bg='#2c3e50',
                              selectcolor='#3498db', activebackground='#2c3e50',
                              activeforeground='#ecf0f1')
            rb.pack(pady=5)
        
        # Buttons
        btn_frame = tk.Frame(settings_frame, bg='#2c3e50')
        btn_frame.pack(pady=30)
        
        def save_settings():
            self.difficulty = difficulty_var.get()
            self.game_variant = variant_var.get()
            messagebox.showinfo("Einstellungen", "Einstellungen gespeichert!")
        
        save_btn = tk.Button(btn_frame, text="💾 Speichern", command=save_settings,
                           font=("Arial", 12), bg='#27ae60', fg='white',
                           activebackground='#229954', activeforeground='white',
                           relief='flat', cursor='hand2', width=15)
        save_btn.pack(side='left', padx=10)
        
        back_btn = tk.Button(btn_frame, text="← Zurück", command=self.create_main_menu,
                           font=("Arial", 12), bg='#95a5a6', fg='white',
                           activebackground='#7f8c8d', activeforeground='white',
                           relief='flat', cursor='hand2', width=15)
        back_btn.pack(side='left', padx=10)
        
    def setup_game(self, mode):
        """Spiel-Setup basierend auf dem gewählten Modus"""
        self.current_mode = mode
        self.player1_score = 0
        self.player2_score = 0
        self.rounds_played = 0
        self.player_history = []
        
        # Namen setzen basierend auf Modus
        if mode == "human_vs_ai":
            self.player2_name = f"Computer ({self.difficulty})"
        elif mode == "human_vs_human":
            self.player2_name = "Spieler 2"
        elif mode == "ai_vs_ai":
            self.player1_name = "Computer A"
            self.player2_name = "Computer B"
        
        self.create_game_screen()
        
    def create_game_screen(self):
        """Erstellt den Haupt-Spielbildschirm"""
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Titel mit Modus-Info
        mode_text = {
            "human_vs_ai": "👤 vs 🤖",
            "human_vs_human": "👤 vs 👤", 
            "ai_vs_ai": "🤖 vs 🤖"
        }
        
        variant_text = "Klassisch" if self.game_variant == "classic" else "Nerd-Modus"
        
        title = tk.Label(self.root, text=f"{mode_text[self.current_mode]} - {variant_text}", 
                        font=("Arial", 18, "bold"), fg='#ecf0f1', bg='#2c3e50')
        title.pack(pady=10)
        
        # Score-Anzeige
        score_frame = tk.Frame(self.root, bg='#34495e')
        score_frame.pack(fill='x', padx=20, pady=10)
        
        self.score_label = tk.Label(score_frame, 
                                   text=f"{self.player1_name}: {self.player1_score}   |   {self.player2_name}: {self.player2_score}", 
                                   font=("Arial", 14, "bold"), fg='white', bg='#34495e')
        self.score_label.pack(pady=10)
        
        # Spielbereich
        game_frame = tk.Frame(self.root, bg='#2c3e50')
        game_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Auswahl-Buttons für Spieler 1 (falls Mensch)
        if self.current_mode in ["human_vs_ai", "human_vs_human"]:
            self.create_player_controls(game_frame)
        else:
            # Bei AI vs AI automatisch spielen
            self.create_ai_vs_ai_controls(game_frame)
            
        # Ergebnis-Anzeige
        self.result_frame = tk.Frame(game_frame, bg='#2c3e50')
        self.result_frame.pack(pady=20)
        
        # Zurück-Button
        back_btn = tk.Button(self.root, text="← Zurück zum Hauptmenü", 
                           command=self.create_main_menu,
                           font=("Arial", 12), bg='#95a5a6', fg='white',
                           activebackground='#7f8c8d', activeforeground='white',
                           relief='flat', cursor='hand2')
        back_btn.pack(pady=10)
        
    def create_player_controls(self, parent):
        """Erstellt die Steuerung für menschliche Spieler"""
        controls_frame = tk.Frame(parent, bg='#2c3e50')
        controls_frame.pack(pady=20)
        
        # Spieler 1 Auswahl
        p1_frame = tk.Frame(controls_frame, bg='#3498db', relief='raised', bd=2)
        p1_frame.pack(side='left', padx=20, pady=10)
        
        tk.Label(p1_frame, text=self.player1_name, font=("Arial", 14, "bold"), 
                fg='white', bg='#3498db').pack(pady=10)
        
        # Buttons je nach Variante
        options = ["Stein", "Schere", "Papier"]
        if self.game_variant == "nerd":
            options.extend(["Echse", "Spock"])
            
        self.p1_buttons = {}
        for option in options:
            btn = tk.Button(p1_frame, text=self.get_symbol(option), 
                          command=lambda x=option: self.player_choice(x),
                          font=("Arial", 16), width=8, height=2,
                          bg='white', fg='#2c3e50',
                          activebackground='#ecf0f1', activeforeground='#2c3e50',
                          relief='flat', cursor='hand2')
            btn.pack(pady=5, padx=10)
            self.p1_buttons[option] = btn
            
        # Spieler 2 Bereich (falls Mensch vs Mensch)
        if self.current_mode == "human_vs_human":
            p2_frame = tk.Frame(controls_frame, bg='#e74c3c', relief='raised', bd=2)
            p2_frame.pack(side='right', padx=20, pady=10)
            
            tk.Label(p2_frame, text=self.player2_name, font=("Arial", 14, "bold"), 
                    fg='white', bg='#e74c3c').pack(pady=10)
            
            self.p2_buttons = {}
            for option in options:
                btn = tk.Button(p2_frame, text=self.get_symbol(option), 
                              command=lambda x=option: self.player2_choice(x),
                              font=("Arial", 16), width=8, height=2,
                              bg='white', fg='#2c3e50',
                              activebackground='#ecf0f1', activeforeground='#2c3e50',
                              relief='flat', cursor='hand2')
                btn.pack(pady=5, padx=10)
                self.p2_buttons[option] = btn
                
        self.player1_choice = None
        self.player2_choice = None
        
    def create_ai_vs_ai_controls(self, parent):
        """Erstellt die Steuerung für AI vs AI"""
        controls_frame = tk.Frame(parent, bg='#2c3e50')
        controls_frame.pack(pady=20)
        
        info_label = tk.Label(controls_frame, text="Beobachte, wie die KIs gegeneinander spielen!", 
                            font=("Arial", 14), fg='#ecf0f1', bg='#2c3e50')
        info_label.pack(pady=20)
        
        start_btn = tk.Button(controls_frame, text="▶️ Automatisches Spiel starten", 
                            command=self.start_ai_vs_ai,
                            font=("Arial", 14), bg='#27ae60', fg='white',
                            activebackground='#229954', activeforeground='white',
                            relief='flat', cursor='hand2', width=25, height=2)
        start_btn.pack(pady=10)
        
        self.auto_play_active = False
        
    def get_symbol(self, choice):
        """Gibt das entsprechende Symbol für eine Wahl zurück"""
        symbols = {
            "Stein": "✊ Stein",
            "Schere": "✌️ Schere", 
            "Papier": "✋ Papier",
            "Echse": "🦎 Echse",
            "Spock": "🖖 Spock"
        }
        return symbols.get(choice, choice)
        
    def player_choice(self, choice):
        """Spieler 1 macht eine Wahl"""
        self.player1_choice = choice
        
        if self.current_mode == "human_vs_ai":
            # Computer-Wahl generieren
            self.player2_choice = self.get_ai_choice()
            self.play_round()
        elif self.current_mode == "human_vs_human":
            # Warten auf Spieler 2
            self.update_choice_display()
            
    def player2_choice(self, choice):
        """Spieler 2 macht eine Wahl (nur bei Mensch vs Mensch)"""
        self.player2_choice = choice
        
        if self.player1_choice and self.player2_choice:
            self.play_round()
        else:
            self.update_choice_display()
            
    def update_choice_display(self):
        """Aktualisiert die Anzeige der getroffenen Wahlen"""
        for widget in self.result_frame.winfo_children():
            widget.destroy()
            
        if self.player1_choice:
            p1_label = tk.Label(self.result_frame, 
                              text=f"{self.player1_name}: {self.get_symbol(self.player1_choice)}",
                              font=("Arial", 12), fg='#3498db', bg='#2c3e50')
            p1_label.pack()
            
        if self.player2_choice:
            p2_label = tk.Label(self.result_frame, 
                              text=f"{self.player2_name}: {self.get_symbol(self.player2_choice)}",
                              font=("Arial", 12), fg='#e74c3c', bg='#2c3e50')
            p2_label.pack()
            
        if not self.player1_choice or not self.player2_choice:
            waiting_label = tk.Label(self.result_frame, 
                                   text="Warte auf Spieler-Auswahl...",
                                   font=("Arial", 12), fg='#bdc3c7', bg='#2c3e50')
            waiting_label.pack()
            
    def get_ai_choice(self):
        """Generiert eine KI-Wahl basierend auf Schwierigkeitsgrad"""
        options = ["Stein", "Schere", "Papier"]
        if self.game_variant == "nerd":
            options.extend(["Echse", "Spock"])
            
        return self.ai_strategies[self.difficulty](options)
        
    def ai_random(self, options):
        """Leichte KI: Zufällige Auswahl"""
        return random.choice(options)
        
    def ai_pattern(self, options):
        """Mittlere KI: Versucht einfache Muster zu erkennen"""
        if len(self.player_history) < 2:
            return random.choice(options)
            
        # Schaue auf die letzten beiden Züge
        last_moves = self.player_history[-2:]
        if last_moves[0] == last_moves[1]:
            # Spieler wiederholt möglicherweise - wähle Counter
            return self.get_counter_choice(last_moves[1])
        else:
            # Zufällige Wahl
            return random.choice(options)
            
    def ai_counter(self, options):
        """Schwere KI: Analysiert Spielermuster und kontert"""
        if len(self.player_history) < 3:
            return random.choice(options)
            
        # Analysiere die häufigste Wahl des Spielers
        from collections import Counter
        choice_count = Counter(self.player_history)
        most_common = choice_count.most_common(1)[0][0]
        
        # 70% Chance auf Counter, 30% Zufall
        if random.random() < 0.7:
            return self.get_counter_choice(most_common)
        else:
            return random.choice(options)
            
    def get_counter_choice(self, player_choice):
        """Gibt die beste Wahl gegen eine Spieler-Wahl zurück"""
        rules = self.classic_rules if self.game_variant == "classic" else self.nerd_rules
        
        # Finde alle Optionen, die gegen player_choice gewinnen
        for choice, beats in rules.items():
            if player_choice in beats:
                return choice
                
        # Fallback: zufällige Wahl
        options = list(rules.keys())
        return random.choice(options)
        
    def start_ai_vs_ai(self):
        """Startet das automatische AI vs AI Spiel"""
        self.auto_play_active = True
        self.play_ai_vs_ai_round()
        
    def play_ai_vs_ai_round(self):
        """Spielt eine Runde AI vs AI"""
        if not self.auto_play_active:
            return
            
        options = ["Stein", "Schere", "Papier"]
        if self.game_variant == "nerd":
            options.extend(["Echse", "Spock"])
            
        self.player1_choice = random.choice(options)  # AI A
        self.player2_choice = random.choice(options)  # AI B
        
        self.play_round()
        
        # Nächste Runde nach 2 Sekunden
        if self.player1_score < 5 and self.player2_score < 5:
            self.root.after(2000, self.play_ai_vs_ai_round)
        else:
            self.auto_play_active = False
            
    def play_round(self):
        """Spielt eine Runde und bestimmt den Gewinner"""
        # Spieler-Historie aktualisieren (für KI-Strategien)
        if self.current_mode == "human_vs_ai":
            self.player_history.append(self.player1_choice)
            
        # Gewinner bestimmen
        winner = self.determine_winner(self.player1_choice, self.player2_choice)
        
        # Scores aktualisieren
        if winner == 1:
            self.player1_score += 1
        elif winner == 2:
            self.player2_score += 1
            
        self.rounds_played += 1
        
        # Ergebnis anzeigen
        self.show_round_result(winner)
        
        # Spiel beenden prüfen
        if self.player1_score >= 5 or self.player2_score >= 5:
            self.end_game()
        else:
            # Neue Runde vorbereiten
            self.player1_choice = None
            self.player2_choice = None
            
    def determine_winner(self, choice1, choice2):
        """Bestimmt den Gewinner einer Runde"""
        if choice1 == choice2:
            return 0  # Unentschieden
            
        rules = self.classic_rules if self.game_variant == "classic" else self.nerd_rules
        
        if choice2 in rules[choice1]:
            return 1  # Spieler 1 gewinnt
        else:
            return 2  # Spieler 2 gewinnt
            
    def show_round_result(self, winner):
        """Zeigt das Ergebnis einer Runde"""
        for widget in self.result_frame.winfo_children():
            widget.destroy()
            
        # Wahlen anzeigen
        choices_frame = tk.Frame(self.result_frame, bg='#2c3e50')
        choices_frame.pack(pady=10)
        
        p1_label = tk.Label(choices_frame, 
                          text=f"{self.player1_name}: {self.get_symbol(self.player1_choice)}",
                          font=("Arial", 14, "bold"), fg='#3498db', bg='#2c3e50')
        p1_label.pack(side='left', padx=20)
        
        vs_label = tk.Label(choices_frame, text="VS", 
                          font=("Arial", 12, "bold"), fg='#ecf0f1', bg='#2c3e50')
        vs_label.pack(side='left', padx=10)
        
        p2_label = tk.Label(choices_frame, 
                          text=f"{self.player2_name}: {self.get_symbol(self.player2_choice)}",
                          font=("Arial", 14, "bold"), fg='#e74c3c', bg='#2c3e50')
        p2_label.pack(side='left', padx=20)
        
        # Ergebnis anzeigen
        if winner == 0:
            result_text = "🤝 UNENTSCHIEDEN!"
            result_color = '#f39c12'
        elif winner == 1:
            result_text = f"🎉 {self.player1_name} GEWINNT!"
            result_color = '#27ae60'
        else:
            result_text = f"🎉 {self.player2_name} GEWINNT!"
            result_color = '#27ae60'
            
        result_label = tk.Label(self.result_frame, text=result_text,
                              font=("Arial", 16, "bold"), fg=result_color, bg='#2c3e50')
        result_label.pack(pady=15)
        
        # Score aktualisieren
        self.score_label.config(text=f"{self.player1_name}: {self.player1_score}   |   {self.player2_name}: {self.player2_score}")
        
        # Regel-Erklärung (nur bei Gewinner)
        if winner != 0:
            explanation = self.get_rule_explanation(self.player1_choice, self.player2_choice)
            if explanation:
                rule_label = tk.Label(self.result_frame, text=explanation,
                                    font=("Arial", 10), fg='#bdc3c7', bg='#2c3e50')
                rule_label.pack(pady=5)
                
    def get_rule_explanation(self, choice1, choice2):
        """Gibt eine Erklärung der angewendeten Regel zurück"""
        rules = self.classic_rules if self.game_variant == "classic" else self.nerd_rules
        
        if choice2 in rules[choice1]:
            # choice1 gewinnt gegen choice2
            explanations = {
                ("Stein", "Schere"): "Stein zerschmettert Schere",
                ("Schere", "Papier"): "Schere schneidet Papier", 
                ("Papier", "Stein"): "Papier bedeckt Stein",
                ("Stein", "Echse"): "Stein zerquetscht Echse",
                ("Echse", "Spock"): "Echse vergiftet Spock",
                ("Spock", "Schere"): "Spock zertrümmert Schere",
                ("Schere", "Echse"): "Schere köpft Echse",
                ("Echse", "Papier"): "Echse frisst Papier",
                ("Papier", "Spock"): "Papier widerlegt Spock",
                ("Spock", "Stein"): "Spock verdampft Stein",
                ("Stein", "Schere"): "Stein zerstört Schere"
            }
            return explanations.get((choice1, choice2), "")
        elif choice1 in rules[choice2]:
            # choice2 gewinnt gegen choice1
            explanations = {
                ("Schere", "Stein"): "Stein zerschmettert Schere",
                ("Papier", "Schere"): "Schere schneidet Papier",
                ("Stein", "Papier"): "Papier bedeckt Stein",
                ("Echse", "Stein"): "Stein zerquetscht Echse", 
                ("Spock", "Echse"): "Echse vergiftet Spock",
                ("Schere", "Spock"): "Spock zertrümmert Schere",
                ("Echse", "Schere"): "Schere köpft Echse",
                ("Papier", "Echse"): "Echse frisst Papier",
                ("Spock", "Papier"): "Papier widerlegt Spock",
                ("Stein", "Spock"): "Spock verdampft Stein",
                ("Schere", "Stein"): "Stein zerstört Schere"
            }
            return explanations.get((choice2, choice1), "")
        return ""
        
    def end_game(self):
        """Beendet das Spiel und zeigt das Endergebnis"""
        winner_name = self.player1_name if self.player1_score > self.player2_score else self.player2_name
        winner_score = max(self.player1_score, self.player2_score)
        
        # Highscore hinzufügen (nur bei Mensch vs Computer oder Mensch vs Mensch)
        if self.current_mode in ["human_vs_ai", "human_vs_human"]:
            mode_text = "Mensch vs Computer" if self.current_mode == "human_vs_ai" else "Mensch vs Mensch"
            variant_text = "Klassisch" if self.game_variant == "classic" else "Nerd-Modus"
            self.add_highscore(winner_name, winner_score, mode_text, variant_text)
        
        # Endergebnis-Dialog
        result_text = f"🏆 SPIEL BEENDET!\n\n"
        result_text += f"Gewinner: {winner_name}\n"
        result_text += f"Endstand: {self.player1_score} : {self.player2_score}\n"
        result_text += f"Gespielte Runden: {self.rounds_played}"
        
        messagebox.showinfo("Spielende", result_text)
        
        # Zurück zum Hauptmenü
        self.create_main_menu()
        
    def run(self):
        """Startet das Spiel"""
        self.root.mainloop()

# Spiel starten
if __name__ == "__main__":
    game = RockPaperScissorsGame()
    game.run()
