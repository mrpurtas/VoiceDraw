# import streamlit as st
# import threading  #Ses kaydetme sürecinin kesinti olmaksızın devam eden bir veri akışına ihtiyaç duyduğunu ve streamlit her bir etkileşimde sayfayı yenilediği için bu veri akışının bozulduğunu biliyoruz dolayısıyla buna çare olarak da threadingden faydalanacağız yani farklı iş parçalarını işlemcinin farklı bölümlerine havale ederek eşzamanlı olarak işletilmesini sağlayacağız 
# import recorder
# import transcriptor
# import painter
# import datetime

# #export PATH="/opt/homebrew/bin:$PATH"


# if "record_active" not in st.session_state:
#     st.session_state.record_active = threading.Event()
#     st.session_state.recording_status = "Başlamaya Hazırız!"
#     st.session_state.recording_completed = False
#     st.session_state.latest_image = ""
#     st.session_state.messages = []
#     st.session_state.frames = []

# def start_recording():   #ses kaydı baslatılsın dedıgımızde neler olmalı
#     st.session_state.record_active.set() #bır threadin baslayıp baslamadıgını yorumlayıcımız bılecek .set sayesınde
#     st.session_state.frames.clear()
#     st.session_state.recording_status = "🔴  **Sesiniz Kaydediliyor...**"
#     st.session_state.recording_completed = False

#     frames = st.session_state.frames
#     threading.Thread(target=recorder.record, args=(st.session_state.record_active, frames)).start()    #her başlat butonuna tıklandığında bu thread başlayacak ve bütün kayıt işlemleri ayrı bir işlem parçası olarak streamlette yaşanan kesintilerden etkilenmeden yoluna devam edecek, start metodunu çağırıyoruz bu start metodunu çağırdımız noktada gerçekten yeni bir thread açılıyor ve işlemcisi streamlitin diğer yaptığı işlerden bağımsız olarak bu trade altındaki record metodunu yürütmeye devam ediyor.


# def stop_recording():
#     st.session_state.record_active.clear()
#     st.session_state.recording_status = "✅  **Kayıt Tamamlandı**"
#     st.session_state.recording_completed = True



# st.set_page_config(page_title="VoiceDraw", layout="wide", page_icon="./icons/app_icon.png")
# st.image(image="./icons/top_banner.png", use_column_width=True)
# st.title("VoiceDraw: Sesli Çizim")
# st.divider()

# col_audio, col_image = st.columns([1,4]) #1e 4 bolduk genıslıklerı 

# with col_audio:
#     st.subheader("Ses Kaydı")
#     st.divider()
#     status_message = st.info(st.session_state.recording_status) #ses kaydı devam ediyor mu etmıyor mu u st info widgetla gosterıyoruz
#     st.divider()

#     subcol_left, subcol_right = st.columns([1,2])

#     with subcol_left:
#         start_btn = st.button(label="Başlat", on_click=start_recording, disabled=st.session_state.record_active.is_set()) #kayıt basladıysa start butonumuz dısabled olsun 
#         stop_btn = st.button(label="Durdur", on_click=stop_recording, disabled = not st.session_state.record_active.is_set())
#     with subcol_right:
#         recorded_audio = st.empty()

#         if st.session_state.recording_completed:
#             recorded_audio.audio(data="voice_prompt.wav")

#     st.divider()
#     latest_image_use = st.checkbox(label="Son Resmi Kullan")

# with col_image:
#     st.subheader("Görsel Çıktılar")
#     st.divider()

#     for message in st.session_state.messages:
#         if message["role"] == "assistant":
#             with st.chat_message(name=message["role"], avatar="./icons/ai_avatar.png"):
#                 st.warning("İşte Sizin İçin Oluşturduğum Görsel:")
#                 st.image(message["content"], width=300)
#         elif message["role"] == "user":
#             with st.chat_message(name=message["role"], avatar="./icons/user_avatar.png"):
#                 st.success(message["content"])
#     if stop_btn:
#         with st.chat_message(name="user", avatar="./icons/user_avatar.png"):
#             with st.spinner("Sesiniz Çözümleniyor..."):
#                 voice_prompt = transcriptor.transcribe_with_whisper(audio_file_name="voice_prompt.wav")
#             st.success(voice_prompt)

#     # if stop_btn:
#     #     with st.chat_message(name="user", avatar="./icons/user_avatar.png"):
#     #         with st.spinner("Sesiniz Çözümleniyor..."):
#     #             voice_prompt = transcriptor.transcribe_with_whisper(audio_file_name="voice_prompt.wav")
#     #         st.success(voice_prompt)

#         st.session_state.messages.append({"role": "user", "content": voice_prompt})

#         with st.chat_message(name="assistant", avatar="./icons/ai_avatar.png"):
#             st.warning("İşte Sizin İçin Oluşturduğum Görsel:")
#             with st.spinner("Görseliniz Oluşturuluyor..."):
#                 if latest_image_use:
#                     image_file_name = painter.generate_image(image_path=st.session_state.latest_image, prompt=voice_prompt)
#                 else:
#                     image_file_name = painter.generate_image_with_dalle(prompt=voice_prompt)
    
#             st.image(image=image_file_name, width=300)

#             with open(image_file_name, "rb") as file:
#                 st.download_button(
#                     label="Resmi İndir",
#                     data=file,
#                     file_name=image_file_name,
#                     mime="image/png"
#                 )

    
#         st.session_state.messages.append({"role": "assistant", "content": image_file_name})
#         st.session_state.latest_image = image_file_name

# import streamlit as st
# import transcriptor
# import painter
# from st_audiorec import st_audiorec

# # Initialize session state
# if "latest_image" not in st.session_state:
#     st.session_state.latest_image = ""
#     st.session_state.messages = []

# # Function to handle audio processing
# def process_audio():
#     audio_data = st.session_state.audio_data
#     if audio_data is not None:
#         # Save the audio file
#         audio_file_name = 'voice_prompt.wav'
#         with open(audio_file_name, 'wb') as f:
#             f.write(audio_data.getbuffer())

#         # Transcribe the audio file
#         voice_prompt = transcriptor.transcribe_with_whisper(audio_file_name=audio_file_name)
#         st.session_state.messages.append({"role": "user", "content": voice_prompt})

#         # Generate image based on the transcription
#         if st.session_state.latest_image_use:
#             image_file_name = painter.generate_image(image_path=st.session_state.latest_image, prompt=voice_prompt)
#         else:
#             image_file_name = painter.generate_image_with_dalle(prompt=voice_prompt)
        
#         st.session_state.messages.append({"role": "assistant", "content": image_file_name})
#         st.session_state.latest_image = image_file_name

# # Streamlit page configuration
# st.set_page_config(page_title="VoiceDraw", layout="wide", page_icon="./icons/app_icon.png")
# st.image(image="./icons/top_banner.png", use_column_width=True)
# st.title("VoiceDraw: Sesli Çizim")
# st.divider()

# # Layout columns
# col_audio, col_image = st.columns([1, 4])

# with col_audio:
#     st.subheader("Ses Kaydı")
#     st.divider()

#     # Record audio
#     st.session_state.audio_data = st_audiorec()  # Removed key parameter
#     st.session_state.latest_image_use = st.checkbox(label="Son Resmi Kullan")
#     process_button = st.button("Kaydı İşle", on_click=process_audio)

#     if st.session_state.audio_data is not None:
#         st.audio(st.session_state.audio_data, format='audio/wav')

# with col_image:
#     st.subheader("Görsel Çıktılar")
#     st.divider()

#     for message in st.session_state.messages:
#         if message["role"] == "assistant":
#             st.warning("İşte Sizin İçin Oluşturduğum Görsel:")
#             st.image(message["content"], width=300)
#         elif message["role"] == "user":
#             st.success(message["content"])

"""import streamlit as st
from st_audiorec import st_audiorec
import transcriptor
import painter

# Initialize session state
if "latest_image" not in st.session_state:
    st.session_state.latest_image = ""
    st.session_state.messages = []
    st.session_state.audio_data = None

# Function to handle audio processing
def process_audio():
    if st.session_state.audio_data is not None:
        # Save the audio file
        audio_file_name = 'voice_prompt.wav'
        with open(audio_file_name, 'wb') as f:
            f.write(st.session_state.audio_data)  # Write bytes directly

        # Transcribe the audio file
        voice_prompt = transcriptor.transcribe_with_whisper(audio_file_name=audio_file_name)
        st.session_state.messages.append({"role": "user", "content": voice_prompt})

        # Generate image based on the transcription
        image_file_name = painter.generate_image_with_dalle(prompt=voice_prompt)
        st.session_state.messages.append({"role": "assistant", "content": image_file_name})
        st.session_state.latest_image = image_file_name

# Function to reset the application state
def reset_app():
    st.session_state.latest_image = ""
    st.session_state.messages = []
    st.session_state.audio_data = None

# Streamlit page configuration
st.set_page_config(page_title="VoiceDraw", layout="wide", page_icon="./icons/app_icon.png")
st.image(image="./icons/top_banner.png", use_column_width=True)
st.title("VoiceDraw: Sesli Çizim")
st.divider()

# Layout columns
col_audio, col_image = st.columns([1, 2.5])

with col_audio:
    st.subheader("Ses Kaydı")
    st.session_state.audio_data = st_audiorec()  # Get audio data from the custom component

    # Buttons for recording actions
    st.button("Kaydı İşle", on_click=process_audio)
    st.button("Sıfırla", on_click=reset_app)

    # Checkbox to decide whether to use the latest image or not
    st.session_state.latest_image_use = st.checkbox("Son Resmi Kullan", value=True)

    # Audio player to play the recorded audio
    if st.session_state.audio_data is not None:
        st.audio(st.session_state.audio_data, format='audio/wav')

with col_image:
    st.subheader("Görsel Çıktılar2")
    
    # Display messages and images
    for message in st.session_state.messages:
        if message["role"] == "assistant":
            st.warning("İşte Sizin İçin Oluşturduğum Görsel:")
            st.image(message["content"], width=300)
        elif message["role"] == "user":
            st.success(message["content"])"""

import streamlit as st
from st_audiorec import st_audiorec
import transcriptor
import painter

# Initialize session state
if "latest_image" not in st.session_state:
    st.session_state.latest_image = ""
    st.session_state.messages = []
    st.session_state.audio_data = None

# Function to handle audio processing
def process_audio():
    if st.session_state.audio_data is not None:
        # Save the audio file
        audio_file_name = 'voice_prompt.wav'
        with open(audio_file_name, 'wb') as f:
            f.write(st.session_state.audio_data)  # Write bytes directly, no need for getbuffer

        # Transcribe the audio file
        voice_prompt = transcriptor.transcribe_with_whisper(audio_file_name=audio_file_name)
        st.session_state.messages.append({"role": "user", "content": voice_prompt})

        # Generate image based on the transcription
        image_file_name = painter.generate_image_with_dalle(prompt=voice_prompt)
        st.session_state.messages.append({"role": "assistant", "content": image_file_name})
        st.session_state.latest_image = image_file_name


# Function to reset the application state
def reset_app():
    st.session_state.latest_image = ""
    st.session_state.messages = []
    st.session_state.audio_data = None

# Streamlit page configuration
st.set_page_config(page_title="VoiceDraw", layout="wide", page_icon="./icons/app_icon.png")
st.image(image="./icons/top_banner.png", use_column_width=True)
st.title("VoiceDraw: Sesli Çizim")
st.divider()

# Layout columns
col_audio, col_image = st.columns([1, 2.5])

with col_audio:
    st.subheader("Ses Kaydı")
    # Get audio data from the custom component and store in session state
    audio_data = st_audiorec()  # Removed key argument
    if audio_data is not None:
        st.session_state.audio_data = audio_data

    # Button to process the audio data
    if st.button("Kaydı İşle"):
        process_audio()

    # Checkbox to decide whether to use the latest image or not
    use_latest_image = st.checkbox("Son Resmi Kullan", value=True)
    st.session_state.latest_image_use = use_latest_image

    # Display messages
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        if role == "user":
            st.info(content)
        elif role == "assistant":
            st.success(content)

with col_image:
    st.subheader("Görsel Çıktılar")
    # Display messages and images
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        if role == "assistant":
            st.warning("İşte Sizin İçin Oluşturduğum Görsel:")
            st.image(content, width=300)  # Görseli göster

            # Download button for the image
            with open(content, "rb") as file:
                btn = st.download_button(
                    label="Görseli İndir",
                    data=file,
                    file_name="generated_image.png",
                    mime="image/png"
                )
        elif role == "user":
            st.info(content)

# Button to reset the application state
if st.button("Sıfırla"):
    reset_app()
