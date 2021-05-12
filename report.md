# Lab1: Automatic Speech Recognition

[toc]

# Modifications

## Summary

- Redesign all the *UI* of the app (Use QtDesigner)

- Two types of *triggers* (Click button or Say something)

- Change *PocketSphinx* to *BaiduAip*

## UI Appearence

- **Window name**: Voice Assistant
- **State indicater**: A playable gif

## Interaction Logic

There are two ways to activate the assistant:

1. Click the button

2. Say something directly

## Speech Recognition

- Use tools in `SpeechRecognition` package to **listen** to user's command. It will stop automatically when no further detection.
- Use `BaiduAip` to **recognize** the audio.
- Use `difflib` to **understand** what user has said.
- Use `QTimer` and `QThread` to do asr tasks in the background. Loops every 1 second.

## Assistant Functions

- Play some music
- Open the notepad
- Open the browser
- Open Wechat
- Search something (Using *bing* search engine)

# Analysis

## Accuracy of speech recognition

### SR library

- `Pocket Sphinx`

  - Support only one language per recognization.
  - Tested, but very poor.
  - Offline.
  - Free.

- `BaiduAip`

  - Support Chinese and some common English.
  - Used in IME, very accurate.
  - Online.
  - Free limited / Paid.

### Audio Record

- `PyAudio`: 

  - Support multi sampling rates, number of channels, audio format.
  - Set how long we need to record manually 

- `SpeechRecognition`: 

  - Only support 1 channel. 
  - Can adjust for ambient noise: `sr.Recognizer().adjust_for_ambient_noise`
  - Records a single phrase until there is no sound.

### Improvement

- Audio Record

  - Use duration of 0.5 second for `adjust_for_ambient_noise` call
  - Rating 16000, 1 Channel, Format pyaudio.paInt16

- SR library

  - We use baidu short speech recognization service. It's much better.
  