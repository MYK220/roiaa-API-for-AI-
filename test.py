from PIL import Image
import pytesseract
import requests
from io import BytesIO
import langid
from googletrans import Translator
import subprocess
from gtts import gTTS
# from IPython.display import Audio, display

# Image URL
# image_url = 'https://mostaql.hsoubcdn.com/uploads/thumbnails/637713/405643/0e67f8d9-b037-4b89-91d2-27d9de8d2497.png'
image_url = 'https://academic-englishuk.com/wp-content/uploads/2020/03/A-basic-paragraph-on-CSR-by-AEUK.png'
# Download the image from the URL
response = requests.get(image_url)

if response.status_code == 200:
    # Open the image from the downloaded content
    image = Image.open(BytesIO(response.content))

    # Perform OCR on the image
    extracted_text = pytesseract.image_to_string(image, lang='eng+ara')

    if not extracted_text:
        print("No text found in the image.")
        tts = gTTS("مفيش كلام فى الصورة", lang='ar')
        tts.save("No_EXIST.mp3")
        # display(Audio("No_EXIST.mp3"))
    else:
        print("Extracted Text:")
        print(extracted_text)
else:
    print(f"Failed to download image. Status code: {response.status_code}")
    tts = gTTS("معلش مش عارفين نقرأ الصورة جرب تانى", lang='ar')
    tts.save("failed_read.mp3")
    # display(Audio("failed_read.mp3"))
    
def detect_language(text):
    # Detect the language of the text
    lang, _ = langid.classify(text)
    return lang


print(extracted_text)
detect_language(extracted_text)

# # Translate the color name to Arabic
if detect_language(extracted_text) == 'en':
    translator = Translator()
    translated_extracted_text = translator.translate(extracted_text, src='en', dest='ar')
    print(translated_extracted_text.text)
else:
    translated_extracted_text = extracted_text
    print(translated_extracted_text)
    
# Convert the detected objects to speech
if detect_language(extracted_text) == 'en':
    myText = "الكلام باللغة الإنجليزية ولكن تمت ترجمته من قبلنا لنبدأ : "
    output_text = translated_extracted_text.text
    tts = gTTS(myText + output_text, lang='ar')
else:
    tts = gTTS(translated_extracted_text, lang='ar')
    
tts.save("extracted_text.mp3")
# Display the spoken result in the Colab notebook
# display(Audio("extracted_text.mp3"))