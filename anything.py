from pygame import mixer
import requests

# response = requests.post('http://192.168.234.6:5000/colorDedection', files={"image": open('./logo_elmagd.png', 'rb'), "Content-Type" : "image/png"})
# response = requests.post('http://192.168.234.6:5000/objectDedection', files={"image": open('./profile.jpg', 'rb'), "Content-Type" : "image"})
response = requests.post('http://192.168.234.6:5000/textDedection', files={"image": open('./Screenshot 2024-02-12 032456.png', 'rb'), "Content-Type" : "image"})

# Check if the request was successful
if response.status_code == 200:
    # Assuming the server returns the audio file
    audio_data = response.content
    
    # Save the audio file locally
    with open('output_audio.mp3', 'wb') as audio_file:
        audio_file.write(audio_data)
        
    # Load and play the audio file
    mixer.init()
    mixer.music.load('output_audio.mp3')
    mixer.music.play()

    # Check for any errors reported by Pygame
    while mixer.music.get_busy():
        pass  # Wait for the audio to finish playing

    print("Audio played successfully.")
else:
    print("Error:", response.status_code)

print(response.content)
