from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import StringProperty, ListProperty, BooleanProperty, NumericProperty
from kivy.animation import Animation
import os, json, random, webbrowser
from datetime import datetime, date, timedelta

try:
    from plyer import notification, vibrator, call, sms
except Exception:
    notification = None
    vibrator = None
    call = None
    sms = None


MESSAGES = {
    "cute": [
        "You are my favorite person.",
        "Your smile makes my whole day better.",
        "I love having you in my life.",
        "You are beautiful even on hard days.",
        "I am proud to love you.",
        "You make my life softer.",
        "You are my favorite hello.",
        "You make boring days feel special.",
        "I love your heart.",
        "I am lucky to have you."
    ],
    "support": [
        "You are not a burden.",
        "One small step is still progress.",
        "Resting is not failing.",
        "You do not have to do everything today.",
        "You are doing better than you think.",
        "Your feelings are real and they matter.",
        "A hard day does not mean a bad life.",
        "You are allowed to need help.",
        "You are safe right now.",
        "You are not weak for struggling."
    ],
    "bad_day": [
        "Bad days do not make you hard to love.",
        "You do not need to be okay for me to love you.",
        "I am proud of you for getting through this moment.",
        "You can take the smallest step possible.",
        "You are safe with me.",
        "You are not too much.",
        "You are allowed to rest.",
        "This feeling will not last forever.",
        "You do not have to explain everything right now.",
        "Just breathe. I am here with you."
    ]
}


KV = """
#:import dp kivy.metrics.dp

<NavButton@Button>:
    size_hint_y: None
    height: dp(52)
    background_color: app.button_color
    color: 1,1,1,1
    font_size: 16

<Card@Label>:
    color: 1,1,1,1
    font_size: 18
    halign: "center"
    valign: "middle"
    text_size: self.width - dp(20), None
    size_hint_y: None
    height: self.texture_size[1] + dp(30)

<Title@Label>:
    font_size: 32
    bold: True
    color: app.accent_color
    size_hint_y: None
    height: dp(55)

ScreenManager:
    HomeScreen:
    MedsScreen:
    MessagesScreen:
    BreathingScreen:
    LoveLettersScreen:
    CarePlanScreen:
    EmergencyScreen:
    SettingsScreen:

<HomeScreen>:
    name: "home"
    ScrollView:
        BoxLayout:
            orientation: "vertical"
            size_hint_y: None
            height: self.minimum_height
            padding: dp(14)
            spacing: dp(9)
            canvas.before:
                Color:
                    rgba: app.bg_color
                Rectangle:
                    pos: self.pos
                    size: self.size

            Title:
                text: "Flora Daily"

            Card:
                text: root.dashboard

            NavButton:
                text: "☀️ Start Day"
                on_release: root.start_day()

            NavButton:
                text: "💊 Meds"
                on_release: app.go("meds")

            NavButton:
                text: "💗 Messages"
                on_release: app.go("messages")

            NavButton:
                text: "🫁 Breathing"
                on_release: app.go("breathing")

            NavButton:
                text: "💌 Love Letters"
                on_release: app.go("letters")

            NavButton:
                text: "🧸 Care Plan"
                on_release: app.go("care")

            NavButton:
                text: "🚨 Emergency"
                on_release: app.go("emergency")

            NavButton:
                text: "⚙️ Settings"
                on_release: app.go("settings")

<MedsScreen>:
    name: "meds"
    BoxLayout:
        orientation: "vertical"
        padding: dp(14)
        spacing: dp(9)
        canvas.before:
            Color:
                rgba: app.bg_color
            Rectangle:
                pos: self.pos
                size: self.size

        Title:
            text: "Medication"

        Card:
            text: root.meds_text

        NavButton:
            text: "Morning Meds Taken"
            on_release: root.mark("morning")

        NavButton:
            text: "Night Meds Taken"
            on_release: root.mark("night")

        NavButton:
            text: "Skipped Today"
            on_release: root.mark("skipped")

        NavButton:
            text: "Back"
            on_release: app.go("home")

<MessagesScreen>:
    name: "messages"
    BoxLayout:
        orientation: "vertical"
        padding: dp(14)
        spacing: dp(9)
        canvas.before:
            Color:
                rgba: app.bg_color
            Rectangle:
                pos: self.pos
                size: self.size

        Title:
            text: "Messages"

        Card:
            text: root.message

        NavButton:
            text: "Cute Message"
            on_release: root.pick("cute")

        NavButton:
            text: "Support Message"
            on_release: root.pick("support")

        NavButton:
            text: "Bad Day Message"
            on_release: root.pick("bad_day")

        NavButton:
            text: "Random Message"
            on_release: root.random_msg()

        NavButton:
            text: "Back"
            on_release: app.go("home")

<BreathingScreen>:
    name: "breathing"
    BoxLayout:
        orientation: "vertical"
        padding: dp(14)
        spacing: dp(9)
        canvas.before:
            Color:
                rgba: app.bg_color
            Rectangle:
                pos: self.pos
                size: self.size

        Title:
            text: "Breathing"

        Label:
            id: breath_circle
            text: root.breath_text
            font_size: 24
            bold: True
            color: 1,1,1,1
            size_hint: None, None
            size: dp(root.circle_size), dp(root.circle_size)
            pos_hint: {"center_x": .5}
            canvas.before:
                Color:
                    rgba: app.accent_color
                Ellipse:
                    pos: self.pos
                    size: self.size

        NavButton:
            text: "Start Breathing"
            on_release: root.start_breathing()

        NavButton:
            text: "Back"
            on_release: app.go("home")

<LoveLettersScreen>:
    name: "letters"
    BoxLayout:
        orientation: "vertical"
        padding: dp(14)
        spacing: dp(9)
        canvas.before:
            Color:
                rgba: app.bg_color
            Rectangle:
                pos: self.pos
                size: self.size

        Title:
            text: "Love Letters"

        TextInput:
            id: letter_input
            hint_text: "Write a love letter..."
            multiline: True

        NavButton:
            text: "Save Letter"
            on_release: root.save_letter()

        NavButton:
            text: "Show Random Letter"
            on_release: root.show_letter()

        NavButton:
            text: "Back"
            on_release: app.go("home")

<CarePlanScreen>:
    name: "care"
    BoxLayout:
        orientation: "vertical"
        padding: dp(14)
        spacing: dp(9)
        canvas.before:
            Color:
                rgba: app.bg_color
            Rectangle:
                pos: self.pos
                size: self.size

        Title:
            text: "Care Plan"

        TextInput:
            id: helps
            hint_text: "What helps when she feels sad?"
            multiline: True

        TextInput:
            id: avoid
            hint_text: "What should I avoid saying/doing?"
            multiline: True

        TextInput:
            id: comfort
            hint_text: "Comfort steps that help..."
            multiline: True

        NavButton:
            text: "Save Care Plan"
            on_release: root.save_plan()

        NavButton:
            text: "Load Care Plan"
            on_release: root.load_plan()

        NavButton:
            text: "Back"
            on_release: app.go("home")

<EmergencyScreen>:
    name: "emergency"
    BoxLayout:
        orientation: "vertical"
        padding: dp(14)
        spacing: dp(9)
        canvas.before:
            Color:
                rgba: .10,.02,.04,1
            Rectangle:
                pos: self.pos
                size: self.size

        Label:
            text: "Emergency Support"
            font_size: 31
            bold: True
            color: 1,.35,.45,1
            size_hint_y: None
            height: dp(55)

        Card:
            text: root.help_text

        NavButton:
            text: "Text Brandon"
            on_release: root.text_contact()

        NavButton:
            text: "Call Brandon"
            on_release: root.call_contact()

        NavButton:
            text: "Ground Me"
            on_release: root.ground()

        NavButton:
            text: "Back"
            on_release: app.go("home")

<SettingsScreen>:
    name: "settings"
    ScrollView:
        BoxLayout:
            orientation: "vertical"
            size_hint_y: None
            height: self.minimum_height
            padding: dp(14)
            spacing: dp(8)
            canvas.before:
                Color:
                    rgba: app.bg_color
                Rectangle:
                    pos: self.pos
                    size: self.size

            Title:
                text: "Settings"

            Label:
                text: "Her Name"
                color: 1,1,1,1
                size_hint_y: None
                height: dp(25)
            TextInput:
                id: her_name
                multiline: False
                size_hint_y: None
                height: dp(48)

            Label:
                text: "Your Phone Number"
                color: 1,1,1,1
                size_hint_y: None
                height: dp(25)
            TextInput:
                id: phone
                multiline: False
                input_filter: "int"
                size_hint_y: None
                height: dp(48)

            Label:
                text: "Support Reminder Minutes"
                color: 1,1,1,1
                size_hint_y: None
                height: dp(25)
            TextInput:
                id: reminder_minutes
                multiline: False
                input_filter: "int"
                size_hint_y: None
                height: dp(48)

            Label:
                text: "Morning Med Time, example 09:00"
                color: 1,1,1,1
                size_hint_y: None
                height: dp(25)
            TextInput:
                id: morning_time
                multiline: False
                size_hint_y: None
                height: dp(48)

            Label:
                text: "Night Med Time, example 21:00"
                color: 1,1,1,1
                size_hint_y: None
                height: dp(25)
            TextInput:
                id: night_time
                multiline: False
                size_hint_y: None
                height: dp(48)

            Label:
                text: "Theme: pink, purple, blue, red"
                color: 1,1,1,1
                size_hint_y: None
                height: dp(25)
            TextInput:
                id: theme
                multiline: False
                size_hint_y: None
                height: dp(48)

            NavButton:
                text: "Save Settings"
                on_release: root.save_settings()

            NavButton:
                text: "Export Backup"
                on_release: root.export_backup()

            NavButton:
                text: "Back"
                on_release: app.go("home")
"""


class BaseScreen(Screen):
    def popup(self, title, msg):
        Popup(
            title=title,
            content=Label(text=msg, font_size=18, halign="center", valign="middle", text_size=(320, None)),
            size_hint=(0.88, 0.48)
        ).open()


class HomeScreen(BaseScreen):
    dashboard = StringProperty("")

    def on_enter(self):
        self.dashboard = App.get_running_app().dashboard_text()

    def start_day(self):
        app = App.get_running_app()
        today = str(date.today())
        app.data["last_awake"] = datetime.now().strftime("%Y-%m-%d %I:%M %p")
        app.data.setdefault("awake_days", [])
        if today not in app.data["awake_days"]:
            app.data["awake_days"].append(today)
        app.save_data()
        app.start_support_timer()
        self.dashboard = app.dashboard_text()
        self.popup("Started 💗", "Day started. Support reminders are on.")


class MedsScreen(BaseScreen):
    meds_text = StringProperty("Track meds here.")

    def on_enter(self):
        self.refresh()

    def refresh(self):
        app = App.get_running_app()
        today = str(date.today())
        items = app.data.get("meds", {}).get(today, [])
        if not items:
            self.meds_text = "No meds marked today."
        else:
            self.meds_text = "\n".join([f"{x['type']} at {x['time']}" for x in items])

    def mark(self, med_type):
        app = App.get_running_app()
        today = str(date.today())
        app.data.setdefault("meds", {}).setdefault(today, [])
        app.data.setdefault("med_days", [])
        app.data["meds"][today].append({"type": med_type, "time": datetime.now().strftime("%I:%M %p")})
        if med_type != "skipped" and today not in app.data["med_days"]:
            app.data["med_days"].append(today)
        app.save_data()
        self.refresh()
        self.popup("Saved 💊", f"{med_type} saved.")


class MessagesScreen(BaseScreen):
    message = StringProperty("Pick a message.")

    def pick(self, group):
        self.message = random.choice(MESSAGES[group])

    def random_msg(self):
        self.message = random.choice(App.get_running_app().all_messages())


class BreathingScreen(BaseScreen):
    breath_text = StringProperty("Ready")
    circle_size = NumericProperty(150)

    def start_breathing(self):
        self.breath_text = "Inhale"
        self.circle_size = 150
        anim1 = Animation(circle_size=260, duration=4)
        anim2 = Animation(circle_size=260, duration=4)
        anim3 = Animation(circle_size=150, duration=6)
        anim1.bind(on_complete=lambda *x: setattr(self, "breath_text", "Hold"))
        anim2.bind(on_complete=lambda *x: setattr(self, "breath_text", "Exhale"))
        anim3.bind(on_complete=lambda *x: setattr(self, "breath_text", "Done 💗"))
        (anim1 + anim2 + anim3).start(self)


class LoveLettersScreen(BaseScreen):
    def save_letter(self):
        text = self.ids.letter_input.text.strip()
        if not text:
            self.popup("Empty", "Write a letter first.")
            return
        app = App.get_running_app()
        app.data.setdefault("letters", []).append({"time": datetime.now().strftime("%Y-%m-%d %I:%M %p"), "text": text})
        app.save_data()
        self.ids.letter_input.text = ""
        self.popup("Saved", "Love letter saved.")

    def show_letter(self):
        letters = App.get_running_app().data.get("letters", [])
        if not letters:
            self.popup("No Letters", "Save one first.")
            return
        self.popup("Love Letter 💌", random.choice(letters)["text"])


class CarePlanScreen(BaseScreen):
    def save_plan(self):
        app = App.get_running_app()
        app.data["care_plan"] = {
            "helps": self.ids.helps.text,
            "avoid": self.ids.avoid.text,
            "comfort": self.ids.comfort.text
        }
        app.save_data()
        self.popup("Saved", "Care plan saved.")

    def load_plan(self):
        plan = App.get_running_app().data.get("care_plan", {})
        self.ids.helps.text = plan.get("helps", "")
        self.ids.avoid.text = plan.get("avoid", "")
        self.ids.comfort.text = plan.get("comfort", "")
        self.popup("Loaded", "Care plan loaded.")


class EmergencyScreen(BaseScreen):
    help_text = StringProperty(
        "This page is for hard moments.\n\nIf she feels unsafe, reach out to a trusted person or local emergency support."
    )

    def ground(self):
        self.help_text = (
            "Look around.\n"
            "Name 5 things you see.\n"
            "Press your feet into the floor.\n"
            "Take one slow breath.\n\n"
            "You are here. You are safe right now."
        )

    def text_contact(self):
        phone = App.get_running_app().settings_data.get("phone", "")
        if not phone:
            self.popup("No Number", "Add your phone number in settings.")
            return
        try:
            webbrowser.open(f"sms:{phone}")
        except Exception:
            self.popup("Text", f"Text this number: {phone}")

    def call_contact(self):
        phone = App.get_running_app().settings_data.get("phone", "")
        if not phone:
            self.popup("No Number", "Add your phone number in settings.")
            return
        try:
            webbrowser.open(f"tel:{phone}")
        except Exception:
            self.popup("Call", f"Call this number: {phone}")


class SettingsScreen(BaseScreen):
    def on_enter(self):
        app = App.get_running_app()
        self.ids.her_name.text = app.settings_data.get("her_name", "baby")
        self.ids.phone.text = app.settings_data.get("phone", "")
        self.ids.reminder_minutes.text = str(app.settings_data.get("reminder_minutes", "20"))
        self.ids.morning_time.text = app.settings_data.get("morning_time", "09:00")
        self.ids.night_time.text = app.settings_data.get("night_time", "21:00")
        self.ids.theme.text = app.settings_data.get("theme", "pink")

    def save_settings(self):
        app = App.get_running_app()
        app.settings_data["her_name"] = self.ids.her_name.text.strip() or "baby"
        app.settings_data["phone"] = self.ids.phone.text.strip()
        app.settings_data["reminder_minutes"] = self.ids.reminder_minutes.text.strip() or "20"
        app.settings_data["morning_time"] = self.ids.morning_time.text.strip() or "09:00"
        app.settings_data["night_time"] = self.ids.night_time.text.strip() or "21:00"

        theme = self.ids.theme.text.strip().lower()
        app.settings_data["theme"] = theme if theme in ["pink", "purple", "blue", "red"] else "pink"

        app.save_settings()
        app.apply_theme()
        app.start_med_checker()
        self.popup("Saved", "Settings saved.")

    def export_backup(self):
        app = App.get_running_app()
        path = os.path.join(app.user_data_dir, "flora_daily_backup.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"data": app.data, "settings": app.settings_data}, f, indent=2)
        self.popup("Backup Saved", path)


class FloraDailyApp(App):
    bg_color = ListProperty([0.08, 0.06, 0.10, 1])
    accent_color = ListProperty([1, 0.55, 0.82, 1])
    button_color = ListProperty([0.95, 0.35, 0.65, 1])

    def build(self):
        self.title = "Flora Daily"
        self.data_path = os.path.join(self.user_data_dir, "data.json")
        self.settings_path = os.path.join(self.user_data_dir, "settings.json")
        self.data = self.load_json(self.data_path, {})
        self.settings_data = self.load_json(self.settings_path, {
            "her_name": "baby",
            "phone": "",
            "reminder_minutes": "20",
            "morning_time": "09:00",
            "night_time": "21:00",
            "theme": "pink"
        })
        self.apply_theme()
        root = Builder.load_string(KV)
        Clock.schedule_once(lambda dt: self.start_med_checker(), 1)
        return root

    def go(self, screen):
        self.root.current = screen

    def load_json(self, path, default):
        if not os.path.exists(path):
            return default
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return default

    def save_data(self):
        with open(self.data_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2)

    def save_settings(self):
        with open(self.settings_path, "w", encoding="utf-8") as f:
            json.dump(self.settings_data, f, indent=2)

    def apply_theme(self):
        theme = self.settings_data.get("theme", "pink")
        if theme == "purple":
            self.bg_color = [0.07, 0.04, 0.12, 1]
            self.accent_color = [0.75, 0.45, 1, 1]
            self.button_color = [0.50, 0.25, 0.75, 1]
        elif theme == "blue":
            self.bg_color = [0.04, 0.06, 0.10, 1]
            self.accent_color = [0.45, 0.70, 1, 1]
            self.button_color = [0.20, 0.45, 0.85, 1]
        elif theme == "red":
            self.bg_color = [0.10, 0.03, 0.04, 1]
            self.accent_color = [1, 0.35, 0.45, 1]
            self.button_color = [0.85, 0.20, 0.28, 1]
        else:
            self.bg_color = [0.08, 0.06, 0.10, 1]
            self.accent_color = [1, 0.55, 0.82, 1]
            self.button_color = [0.95, 0.35, 0.65, 1]

    def all_messages(self):
        pool = []
        for group in MESSAGES.values():
            pool.extend(group)
        return pool

    def dashboard_text(self):
        today = str(date.today())
        meds = len(self.data.get("meds", {}).get(today, []))
        awake = self.data.get("last_awake", "Not started yet")
        return (
            f"Hi {self.settings_data.get('her_name', 'baby')} 💗\n\n"
            f"Awake: {awake}\n"
            f"Meds Today: {meds}\n"
            f"Morning Med Time: {self.settings_data.get('morning_time')}\n"
            f"Night Med Time: {self.settings_data.get('night_time')}"
        )

    def notify(self, title, msg):
        if vibrator:
            try:
                vibrator.vibrate(0.2)
            except Exception:
                pass

        if notification:
            try:
                notification.notify(title=title, message=msg, timeout=8)
                return
            except Exception:
                pass

        Popup(
            title=title,
            content=Label(text=msg, font_size=18, halign="center", valign="middle", text_size=(320, None)),
            size_hint=(0.88, 0.48)
        ).open()

    def start_support_timer(self):
        Clock.unschedule(self.support_reminder)
        minutes = max(1, int(self.settings_data.get("reminder_minutes", "20")))
        Clock.schedule_interval(self.support_reminder, minutes * 60)

    def support_reminder(self, dt):
        self.notify("Little Reminder 💗", random.choice(self.all_messages()))

    def start_med_checker(self):
        Clock.unschedule(self.check_med_times)
        Clock.schedule_interval(self.check_med_times, 60)

    def check_med_times(self, dt):
        now = datetime.now().strftime("%H:%M")
        today = str(date.today())

        for key, label in [("morning_time", "Morning meds"), ("night_time", "Night meds")]:
            target = self.settings_data.get(key, "")
            notify_key = f"{today}_{key}"

            if now == target and self.data.get("last_med_notice") != notify_key:
                self.data["last_med_notice"] = notify_key
                self.save_data()
                self.notify("Medication Reminder 💊", f"{label} time.")

if __name__ == "__main__":
    FloraDailyApp().run()
