import customtkinter as ctk
from config import get_language_list, SUPPORTED_LANGUAGES
from translator_engine import translate_text

# Text reshaping libraries to fix the Linux RTL rendering bug
import arabic_reshaper
from bidi.algorithm import get_display

# Text-to-speech: gTTS generates the audio, pygame plays it back
import threading
import os
import pygame
from gtts import gTTS

ctk.set_appearance_mode("System")  
ctk.set_default_color_theme("blue") 

class TranslationApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("CodeAlpha Language Translation Tool")
        self.geometry("600x500")
        self.resizable(False, False)
        
        self.languages = get_language_list()
        self.last_translation = ""  # holds the clean translated text (Copy/Listen read from this, not the textbox)
        
        # --- UI ELEMENTS SETUP ---
        
        self.title_label = ctk.CTkLabel(self, text="AI Language Translator", font=("Arial", 22, "bold"))
        self.title_label.pack(pady=15)
        
        self.lang_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.lang_frame.pack(pady=10)
        
        self.src_dropdown = ctk.CTkOptionMenu(self.lang_frame, values=self.languages)
        self.src_dropdown.set("English")
        self.src_dropdown.grid(row=0, column=0, padx=20)
        
        self.arrow_label = ctk.CTkLabel(self.lang_frame, text="➔", font=("Arial", 16))
        self.arrow_label.grid(row=0, column=1)
        
        self.tgt_dropdown = ctk.CTkOptionMenu(self.lang_frame, values=self.languages)
        self.tgt_dropdown.set("Urdu")
        self.tgt_dropdown.grid(row=0, column=2, padx=20)
        
        # Input Text Box
        self.input_textbox = ctk.CTkTextbox(self, width=500, height=100, font=("Arial", 14))
        self.placeholder = "Type your text here..."
        self.input_textbox.insert("1.0", self.placeholder)
        self.input_textbox.pack(pady=10)
        
        # Bind Event Listeners for automatic placeholder handling
        self.input_textbox.bind("<FocusIn>", self.clear_placeholder)
        self.input_textbox.bind("<FocusOut>", self.restore_placeholder)
        
        # Translate Trigger Button
        self.translate_btn = ctk.CTkButton(self, text="Translate Text", font=("Arial", 14, "bold"), command=self.handle_translation)
        self.translate_btn.pack(pady=10)
        
        # Output Text Box (using an Urdu compatible sans-serif styling backup)
        self.output_textbox = ctk.CTkTextbox(self, width=500, height=100, font=("Arial", 16), fg_color="#2b2b2b")
        self.output_textbox.pack(pady=10)
        
        # Copy + Listen buttons sit side by side under the output box
        self.action_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.action_frame.pack(pady=5)

        self.copy_btn = ctk.CTkButton(
            self.action_frame,
            text="Copy Translation",
            font=("Arial", 13),
            fg_color="#3a3a3a",
            hover_color="#505050",
            command=self.copy_to_clipboard
        )
        self.copy_btn.grid(row=0, column=0, padx=10)

        self.speak_btn = ctk.CTkButton(
            self.action_frame,
            text="Listen",
            font=("Arial", 13),
            fg_color="#3a3a3a",
            hover_color="#505050",
            command=self.speak_translation
        )
        self.speak_btn.grid(row=0, column=1, padx=10)
        
    def clear_placeholder(self, event):
        """Instantly deletes placeholder text when clicking inside the textbox."""
        current_text = self.input_textbox.get("1.0", "end-1c")
        if current_text == self.placeholder:
            self.input_textbox.delete("1.0", "end")
            
    def restore_placeholder(self, event):
        """Restores the default helper string if the user exits without typing anything."""
        current_text = self.input_textbox.get("1.0", "end-1c").strip()
        if not current_text:
            self.input_textbox.insert("1.0", self.placeholder)
        
    def handle_translation(self):
        """Bridge function connecting frontend inputs to backend engine with dynamic RTL alignment correction."""
        raw_input = self.input_textbox.get("1.0", "end-1c")
        source_selection = self.src_dropdown.get()
        target_selection = self.tgt_dropdown.get()
        
        if raw_input == self.placeholder or not raw_input.strip():
            return
        
        self.output_textbox.delete("1.0", "end")
        
        translated_output = translate_text(raw_input, source_selection, target_selection)
        self.last_translation = translated_output  # clean version, kept separate from the display-only reshaped text
        
        # Configure a text alignment tag layout rule dynamically
        if target_selection in ["Urdu", "Arabic"]:
            # Configure the textbox to justify text to the right side
            self.output_textbox.tag_config("rtl", justify="right")
            
            # Apply script letter reshaping and text layout reversal
            reshaped_text = arabic_reshaper.reshape(translated_output)
            final_output = get_display(reshaped_text)
            
            # Insert text with the explicit right-to-left alignment tag rule
            self.output_textbox.insert("1.0", final_output, "rtl")
        else:
            # Standard left-aligned display for English, French, Spanish, etc.
            self.output_textbox.tag_config("ltr", justify="left")
            self.output_textbox.insert("1.0", translated_output, "ltr")

    def copy_to_clipboard(self):
        """Copies the actual clean translation (not the reshaped display version) to the clipboard."""
        text_to_copy = self.last_translation.strip()
        
        if not text_to_copy:
            return
        
        self.clipboard_clear()
        self.clipboard_append(text_to_copy)
        self.update()  # keeps the clipboard content available after the window loses focus
        
        # quick visual feedback so the user knows it worked, then revert after a second
        self.copy_btn.configure(text="Copied!")
        self.after(1200, lambda: self.copy_btn.configure(text="Copy Translation"))

    def speak_translation(self):
        """Reads the actual translated text aloud (not the reshaped display version). Runs in a background thread."""
        text_to_speak = self.last_translation.strip()
        
        if not text_to_speak:
            return
        
        target_selection = self.tgt_dropdown.get()
        lang_code = SUPPORTED_LANGUAGES.get(target_selection, "en")
        
        self.speak_btn.configure(text="Speaking...", state="disabled")
        threading.Thread(target=self._play_audio, args=(text_to_speak, lang_code), daemon=True).start()

    def _play_audio(self, text, lang_code):
        """Generates the speech file and plays it. Runs off the main thread."""
        audio_file = "temp_audio.mp3"
        try:
            tts = gTTS(text=text, lang=lang_code)
            tts.save(audio_file)
            
            pygame.mixer.init()
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            
            # block this background thread until playback finishes
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)
            
            pygame.mixer.quit()
        except Exception as error:
            print(f"Could not play audio: {error}")
        finally:
            if os.path.exists(audio_file):
                os.remove(audio_file)
            # button updates must happen back on the main thread
            self.after(0, lambda: self.speak_btn.configure(text="🔊 Listen", state="normal"))

if __name__ == "__main__":
    app = TranslationApp()
    app.mainloop()