import streamlit as st
import cv2
import os
import E2FGVI.test as model




def load_video():
    """Создание формы для загрузки изображения"""
    # Форма для загрузки изображения средствами Streamlit
    uploaded_file = st.file_uploader(
        label='Upload video', type=['mp4'])
    if uploaded_file is not None:
        with open(os.path.join("dataset/video", "video.mp4"), "wb") as f:
            f.write(uploaded_file.getbuffer())
        read_frame_from_videos('dataset/video/video.mp4', 'video_frames')
    else:
        return None

def load_masks():
    uploaded_file = st.file_uploader(
        label='Upload mask', type=['mp4'])
    if uploaded_file is not None:
        with open(os.path.join("dataset/mask", "video.mp4"), "wb") as f:
            f.write(uploaded_file.getbuffer())
        read_frame_from_videos(f'dataset/mask/video.mp4', 'mask_frames')
    else:
        return None




def read_frame_from_videos(path, name):
    capture = cv2.VideoCapture(path)
    frameNr = 0
    while True:
        success, frame = capture.read()
        if success:
            cv2.imwrite(f'dataset/{name}/{frameNr}.jpg', frame)
        else:
            break
        frameNr = frameNr + 1
    capture.release()

st.title('Deleting object from video')
try:
    os.system('mkdir dataset\\video')
    os.system('mkdir dataset\\mask')
    os.system('mkdir dataset\\video_frames')
    os.system('mkdir dataset\\mask_frames')
except:
    print('[-] Folders already exist')

load_video()
load_masks()

result = st.button('Start deleting')
if result:
    with st.spinner('We are making some magic...'):
        model.main_worker("e2fgvi", "E2FGVI/examples/tennis", "E2FGVI/examples/tennis_mask", "E2FGVI/release_model/E2FGVI"
                                                                                            "-CVPR22.pth")
    st.success('Done!')
    video_file = open('E2FGVI/results/results.mp4', 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)
    os.system("rm dataset")




# НЕ забудь в конце удалить все видео






