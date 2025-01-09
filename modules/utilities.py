
import os
import azure.cognitiveservices.speech as speechsdk
import streamlit as st

def speak_text(text, speech_key, speech_region, voice_name='en-US-AvaMultilingualNeural'):
    """
    Uses Azure Text-to-Speech to synthesize speech from the input text.

    Args:
        text (str): The text to be spoken.
        speech_key (str): Azure Cognitive Services Speech API key.
        speech_region (str): Azure region where the Speech resource is hosted.
        voice_name (str): The voice name for speech synthesis (default is multilingual neural voice).
    
    Returns:
        None
    """
    try:
        # Set up the speech configuration
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
        audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

        # Set the voice name for speech synthesis
        speech_config.speech_synthesis_voice_name = voice_name

        # Initialize the Speech Synthesizer
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

        # Synthesize speech from the input text
        speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

        # Handle the result
        if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print(f"Speech synthesized for text: {text}")
        elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_synthesis_result.cancellation_details
            print(f"Speech synthesis canceled: {cancellation_details.reason}")
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    print(f"Error details: {cancellation_details.error_details}")
                    print("Did you set the speech resource key and region values correctly?")
    except Exception as e:
        print(f"An error occurred: {e}")



def listen_azure(speech_key, speech_region, language):
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
    speech_config.speech_recognition_language=language

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    st.write("Speak into your microphone.")
    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(speech_recognition_result.text))
        return speech_recognition_result.text
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")


