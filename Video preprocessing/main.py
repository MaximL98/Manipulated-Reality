from PIL import Image
import face_recognition
import os

folder_frames_real = "extracted_frames_real"
folder_faces_real = "faces_from_frames_real"

folder_frames_fake = "extracted_frames_fake"
folder_faces_fake = "faces_from_frames_fake"

image_list = []
frame_count = 0

for filename in os.listdir(folder_frames_fake):
    f = os.path.join(folder_frames_fake, filename)
    if os.path.isfile(f):
        image = face_recognition.load_image_file(f)
    image_list.append(image)
    
for image in image_list:
    face_locations = face_recognition.face_locations(image)

    for face_location in face_locations:
        frame_name = f'{folder_faces_fake}/frame_{frame_count:05d}.jpg'
        top, right, bottom, left = face_location

        face_image = image[top:bottom, left:right]
        pil_image = Image.fromarray(face_image)
        pil_image.save(frame_name)
        frame_count += 10









