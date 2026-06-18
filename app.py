import gradio as gr
from config import get_language_list
from translator_engine import translate_text
from gtts import gTTS
import os

# Fetch available language options from your existing config
languages = get_language_list()

def web_translator_pipeline(text, source_lang, target_lang):
    """
    Takes web inputs, runs the translation backend, and generates 
    an audio file for the browser's native audio player.
    """
    if not text.strip() or text == "Type your text here...":
        return "Please enter valid text.", None
        
    # 1. Run your existing core translation logic script
    translated_text = translate_text(text, source_lang, target_lang)
    
    # 2. Generate Text-to-Speech audio using gTTS directly for the web
    # We map the language target to its correct code using a simple inline check
    from config import SUPPORTED_LANGUAGES
    lang_code = SUPPORTED_LANGUAGES.get(target_lang, "en")
    
    audio_path = "output_voice.mp3"
    try:
        tts = gTTS(text=translated_text, lang=lang_code)
        tts.save(audio_path)
    except Exception as e:
        print(f"Audio generation failed: {e}")
        audio_path = None # Return None if audio generation fails safely
        
    # Gradio automatically handles text orientation and audio players natively!
    return translated_text, audio_path

# --- GRADIO WEB INTERFACE SETUP ---
with gr.Blocks(theme=gr.themes.Default(primary_hue="blue")) as demo:
    gr.Markdown("# AI Language Translation Tool")
    gr.Markdown("Select your languages, type your text, and instantly get the translated text and audio playback.")
    
    with gr.Row():
        src_drop = gr.Dropdown(choices=languages, value="English", label="Source Language")
        tgt_drop = gr.Dropdown(choices=languages, value="Urdu", label="Target Language")
        
    with gr.Row():
        input_text = gr.Textbox(placeholder="Type your text here...", lines=4, label="Input Text")
        output_text = gr.Textbox(label="Translated Text", lines=4)
        
    with gr.Row():
        submit_btn = gr.Button("Translate Text", variant="primary")
        
    audio_playback = gr.Audio(label="Audio Voice Output", type="filepath")
    
    # Connect UI button action to our web processing pipeline
    submit_btn.click(
        fn=web_translator_pipeline,
        inputs=[input_text, src_drop, tgt_drop],
        outputs=[output_text, audio_playback]
    )

if __name__ == "__main__":
    demo.launch()