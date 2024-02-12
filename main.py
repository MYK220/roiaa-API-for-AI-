import pytesseract
import langid
from googletrans import Translator
from gtts import gTTS
from ultralytics import YOLO
from flask import Flask, request, send_file
from googletrans import Translator
from flask_restful import Resource, Api
import io
from sklearn.cluster import KMeans
from skimage import io
import webcolors
from googletrans import Translator
# import subprocess
from gtts import gTTS
# Ultralytics
from ultralytics import YOLO


app = Flask(__name__)
api = Api(app)

class colorDedection(Resource):
    def post(self):
        try:
            image=request.files['image']
            image.save("image.jpg")
            #===============================            
            image_url = "image.jpg"
            image = io.imread(image_url)

            # Reshape the image to be a list of pixels
            pixels = image.reshape(-1, 3)

            # Determine the number of clusters (colors) you want to detect
            num_clusters = 1  # We are detecting the dominant color

            # Perform K-means clustering
            kmeans = KMeans(n_clusters=num_clusters, random_state=0)
            kmeans.fit(pixels)

            # Get the RGB value of the cluster center (the dominant color)
            dominant_color_rgb = kmeans.cluster_centers_[0]

            # Convert RGB to a hex color
            hex_color = '#{0:02X}{1:02X}{2:02X}'.format(int(dominant_color_rgb[0]), int(dominant_color_rgb[1]), int(dominant_color_rgb[2]))

            # Define a list of primary colors and their RGB values
            primary_colors = {
                "Red": (255, 0, 0),
                "Green": (0, 255, 0),
                "Blue": (0, 0, 255),
                "Yellow": (255, 255, 0),
                "Cyan": (0, 255, 255),
                "Magenta": (255, 0, 255),
                "Orange": (255, 165, 0),
                "Purple": (128, 0, 128),
                "Pink": (255, 192, 203),
                "Brown": (139, 69, 19),
                "Gray": (128, 128, 128),
                "Black": (0, 0, 0),
                "White": (255, 255, 255),
                "Gold": (255, 215, 0),
                "Silver": (192, 192, 192),
                "Bronze": (205, 127, 50),
                "Lavender": (230, 230, 250),
                "Turquoise": (64, 224, 208),
                "Lime": (0, 255, 0),
                "Navy": (0, 0, 128),
                "Maroon": (128, 0, 0),
                "Teal": (0, 128, 128),
                "Olive": (128, 128, 0),
                "Aqua": (0, 128, 128),
                "Fuchsia": (255, 0, 128),
                "Indigo": (75, 0, 130),
                "Beige": (245, 245, 220),
                "Violet": (238, 130, 238),
                "Crimson": (220, 20, 60),
                "SlateGray": (112, 128, 144),
                # Add more primary colors as needed
            }

            # Use webcolors to find the color name for the hex color
            try:
                color_name = webcolors.hex_to_name(hex_color)
                print(f"The dominant color in the image is {color_name}.")
            except ValueError:
                print(f"The dominant color in the image is a hex color: {hex_color}.")

            # Calculate the Euclidean distance to find the nearest primary color
            def euclidean_distance(color1, color2):
                return sum((c1 - c2) ** 2 for c1, c2 in zip(color1, color2)) ** 0.5

            closest_primary_color = min(primary_colors, key=lambda color: euclidean_distance(primary_colors[color], dominant_color_rgb))

            # Load the image from a local file
            image_path = "image.jpg"
            image = io.imread(image_path)

            # Reshape the image to be a list of pixels
            pixels = image.reshape(-1, 3)

            # Determine the number of clusters (colors) you want to detect
            num_clusters = 5  # You can adjust this number based on your needs

            # Perform K-means clustering
            kmeans = KMeans(n_clusters=num_clusters, random_state=0)
            kmeans.fit(pixels)

            # Get the RGB values of the cluster centers (the dominant colors)
            dominant_colors_rgb = kmeans.cluster_centers_

            # Convert RGB to hex colors
            hex_colors = ['#{:02X}{:02X}{:02X}'.format(int(color[0]), int(color[1]), int(color[2])) for color in dominant_colors_rgb]

            # Find the color names for the hex colors and their nearest primary colors
            color_names = []
            nearest_primary_colors = []

            for hex_color in hex_colors:
                try:
                    color_name = webcolors.hex_to_name(hex_color)
                    color_names.append(color_name)
                except ValueError:
                    color_names.append(f"Hex: {hex_color}")

                # Calculate the Euclidean distance to find the nearest primary color
                dominant_color_rgb = [int(hex_color[i:i+2], 16) for i in (1, 3, 5)]
                closest_primary_color = min(primary_colors, key=lambda color: euclidean_distance(primary_colors[color], dominant_color_rgb))
                nearest_primary_colors.append(closest_primary_color)

            for i in range(len(hex_colors)):
                print(f"Dominant color {i+1}: {color_names[i]}")
                print(f"Nearest primary color {i+1}: {nearest_primary_colors[i]}")

            outPut_colors = (' and ').join(nearest_primary_colors)

            #======================
            translator = Translator()
            translated_color = translator.translate(outPut_colors, src='en', dest='ar')
            output_color = translated_color.text

            # Convert the detected objects to speech
            tts = gTTS("اللون هو ال" + output_color, lang='ar')
            tts.save("color.mp3")

            return send_file('./color.mp3', mimetype='audio/mp3', as_attachment=True)
        except Exception as e:
            return {'error': str(e)}, 500  # رمز الخطأ 500 لخطأ في الخادم

class textDedection(Resource):
    def post(self):
        try:
            # Open the image from the downloaded content
            image = request.files['image']
            image.save("ocr.png")

            def detect_language(text):
                # Detect the language of the text
                lang, _ = langid.classify(text)
                return lang

            # Perform OCR on the image
            extracted_text = pytesseract.image_to_string("ocr.png", lang='eng+ara')

            if not extracted_text:
                print("No text found in the image.")
                tts = gTTS("مفيش كلام فى الصورة", lang='ar')
            else:
                ## Translate the color name to Arabic
                if detect_language(extracted_text) == 'en':
                    translator = Translator()
                    translated_extracted_text = translator.translate(extracted_text, src='en', dest='ar')
                    myText = "الكلام باللغة الإنجليزية ولكن تمت ترجمته من قبلنا لنبدأ : "
                    output_text = translated_extracted_text.text
                    tts = gTTS(myText + output_text, lang='ar')
                else:
                    translated_extracted_text = extracted_text
                    tts = gTTS(translated_extracted_text, lang='ar')
                    print(translated_extracted_text)

            tts.save("extracted_text.mp3")
            return send_file('./extracted_text.mp3', mimetype='audio/mp3', as_attachment=True)
        except Exception as e:
            return {'error': str(e)}, 500  # رمز الخطأ 500 لخطأ في الخادم

class objectDedection(Resource):
    def post(self):
        try:
            image=request.files['image']
            image.save("image.jpg")
            #===============================            
            image_url = "image.jpg"
            # To Translate
            model = YOLO("yolov8n.pt")
            results = model.predict(image_url)
            cls= results[0].boxes.cls
            classes = dict()
            for cno in cls:
                if model.names[int(cno)] not in classes:
                    classes[model.names[int(cno)]] = 1
                else:
                    classes[model.names[int(cno)]] += 1        

            msg = "there is: "

            for c in classes:
                msg += str(classes[c]) + " " + c + " and "    
                
            # Create a Translator object
            translator = Translator()

            # Translate "Detected Objects" to Arabic
            translated_text = translator.translate(msg, src='en', dest='ar').text

            print(translated_text)
            # Convert the detected objects to speech
            tts = gTTS(translated_text, lang='ar')
            tts.save("text.mp3")

            return send_file('./text.mp3', mimetype='audio/mp3', as_attachment=True)
        except Exception as e:
            return {'error': str(e)}, 500  # رمز الخطأ 500 لخطأ في الخادم

api.add_resource(colorDedection, '/colorDedection')
api.add_resource(textDedection, '/textDedection')
api.add_resource(objectDedection, '/objectDedection')

if __name__ == '__main__':
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    app.run(debug=True, host='0.0.0.0')


