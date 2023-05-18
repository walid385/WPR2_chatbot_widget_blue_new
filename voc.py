import openai
import speech_recognition as sr
import pyttsx3

# API-Key von OpenAI eintragen
openai.api_key = "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"


# Funktionen für Spracherkennung, GPT-3.5-Anfragen und Text-zu-Sprache
# Text-zu-Sprache (TTS) mit der pyttsx3 Bibliothek
def text_to_speech(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Geschwindigkeit der Sprachausgabe
    engine.setProperty('volume', 0.9)  # Lautstärke (0.0 bis 1.0)
    engine.setProperty('voice', engine.getProperty('voices')[0].id)  # Stimme (0 für männlich, 1 für weiblich)
    engine.say(text)
    engine.runAndWait()

# Sprache-zu-Text mit der speech_recognition Bibliothek
def transcribe_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Sprechen Sie Ihren Text ein:")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language='de-DE')
        print(f"Transkribierter Text: {text}")
        return text
    except Exception as e:
        print(f"Entschuldigung, es gab ein Problem bei der Transkription: {e}")
        return None

# GPT-API Anfrage
def gpt_query(text):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=text,
            max_tokens=1000,
            n=1,
            stop=None,
            temperature=0.5,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Es gab ein Problem bei der Kommunikation mit der GPT-API: {e}")
        return None

# ... (wie im vorherigen Beispiel, ggf. leicht angepasst)

def prompt_for_ingredients():
    text_to_speech("Bitte nennen Sie die Zutaten, die Sie verwenden möchten.")
    ingredients = transcribe_speech()
    if not ingredients:
        text_to_speech("Es wurden keine Zutaten erkannt. Bitte versuchen Sie es erneut.")
        return None
    return ingredients


def generate_recipe_titles(ingredients):
    prompt = f"Generiere 5 Rezepttitel für den Thermomix basierend auf den folgenden Zutaten: {ingredients}"
    response_text = gpt_query(prompt)
    titles = response_text.split('\n')[:5]
    return titles


def prompt_for_recipe_choice(titles):
    text_to_speech("Hier sind die Rezepttitel. Bitte wählen Sie ein Rezept aus:")
    for title in titles:
        text_to_speech(f"{title}")
    selected_title = transcribe_speech()
    return selected_title


def generate_recipe_instructions(recipe_title):
    prompt = f"Generiere eine Liste von Schritten für das vollständige Rezept für den Thermomix von Vorwerk. Schreibe die masseinheiten immer aus: {recipe_title}"
    response_text = gpt_query(prompt)
    response_text.replace ("\n\n","\n")
    instructions = response_text.split('\n')
    return instructions


def prompt_for_cooking_start():
    text_to_speech("Sind Sie bereit, das Rezept zu kochen? Bitte sagen Sie 'start' oder 'abbrechen'.")
    response = transcribe_speech()
    return response


def navigate_instructions(instructions):
    index = 0
    text_to_speech(instructions[index])

    while True:
        response = transcribe_speech()

        if response.lower() in ["weiter", "nächster schritt", "seite", "reiter", "gleiter", "heiter"]:
            index += 1
            if index >= len(instructions):
                text_to_speech("Das war der letzte Schritt des Rezepts.")
                index -= 1
            else:
                text_to_speech(instructions[index])

        elif response in ["zurück", "vorheriger Schritt"]:
            index -= 1
            if index < 0:
                text_to_speech("Das war der erste Schritt des Rezepts.")
                index = 0
            else:
                text_to_speech(instructions[index])

        elif response in ["wiederholen", "aktueller Schritt"]:
            text_to_speech(instructions[index])

        elif response in ["abbrechen", "beenden"]:
            text_to_speech("Das Kochen wurde abgebrochen. Bis zum nächsten Mal!")
            break

        else:
            text_to_speech(
                "Entschuldigung, ich habe Ihre Eingabe nicht verstanden. Bitte sagen Sie 'weiter', 'zurück', 'wiederholen' oder 'abbrechen'.")


def main():
    ingredients = prompt_for_ingredients()


    if not ingredients:
        return
    #ingredients = ["Eier", "Speck"]

    recipe_titles = generate_recipe_titles(ingredients)
    recipe_choice = prompt_for_recipe_choice(recipe_titles) #"Speck-Eier-Frittata"
    recipe_instructions = generate_recipe_instructions(recipe_choice)

    while True:
        start_response = prompt_for_cooking_start()
        if start_response.lower() == "start":
            navigate_instructions(recipe_instructions)
            break
        elif start_response.lower() == "abbrechen":
            text_to_speech("Das Kochen wurde abgebrochen. Bis zum nächsten Mal!")
            break
        else:
            text_to_speech(
                "Entschuldigung, ich habe Ihre Eingabe nicht verstanden. Bitte sagen Sie 'start' oder 'abbrechen'.")

if __name__ == "__main__":
    main()






#def prompt_for_mode():
#    while True:
#        mode = input("Möchten Sie mit Sprache oder Text interagieren? Bitte geben Sie 'Sprache' oder 'Text' ein: ")
#        if mode.lower() in ["sprache", "text"]:
#            return mode.lower()
#        else:
#            print("Ungültige Eingabe. Bitte geben Sie 'Sprache' oder 'Text' ein.")





#def main():
#    mode = prompt_for_mode()  # Fragt den Benutzer nach dem bevorzugten Modus
#
#    # Verwendet den gewählten Modus, um die Zutaten zu bekommen
#    if mode == "text":
#        ingredients = input("Bitte geben Sie die Zutaten ein, die Sie verwenden möchten: ")
#    else:
#        ingredients = prompt_for_ingredients()
#
#    # Wenn es keine Zutaten gibt, beenden Sie die Anwendung
#    if not ingredients:
#        return
#
#    # Generiert die Rezepttitel
#    recipe_titles = generate_recipe_titles(ingredients)
#
#    # Verwendet den gewählten Modus, um die Rezeptwahl des Benutzers zu erhalten
#    if mode == "text":
#        recipe_choice = input("Bitte wählen Sie ein Rezept aus den folgenden Titeln: " + ", ".join(recipe_titles))
#    else:
#        recipe_choice = prompt_for_recipe_choice(recipe_titles)
#
#    # Generiert die Rezeptanweisungen
#    recipe_instructions = generate_recipe_instructions(recipe_choice)
#
#    # Verwendet den gewählten Modus, um die Entscheidung des Benutzers zum Start des Kochens zu erhalten
#    while True:
#        if mode == "text":
#            start_response = input("Sind Sie bereit zu kochen? Bitte tippen Sie 'start' oder 'abbrechen': ")
#        else:
#            start_response = prompt_for_cooking_start()
#
#        # Navigiert durch die Anweisungen oder beendet die Anwendung basierend auf der Entscheidung des Benutzers
#        if start_response.lower() == "start":
#            navigate_instructions(recipe_instructions)
#            break
#        elif start_response.lower() == "abbrechen":
#            text_to_speech("Das Kochen wurde abgebrochen. Bis zum nächsten Mal!")
#            break
#        else:
#            text_to_speech(
#                "Entschuldigung, ich habe Ihre Eingabe nicht verstanden. Bitte sagen Sie 'start' oder 'abbrechen'.")