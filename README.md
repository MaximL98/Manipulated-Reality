<p align="center"> <img src="https://github.com/MaximL98/Manipulated-Reality/frontend/public/ManipulatedRealityLogo_MR.png" width="15%" height="15%"> </p>
 

## Abstract
This development and research project aims to contribute to the ongoing efforts to combat the generation of deepfakes. We present a novel framework for the detection of deepfake media that involves two distinct models: A hybrid deep learning architecture utilizing the Keras framework for the classification of deepfake content. The framework incorporates a pre-trained InceptionV3 model for video feature extraction, followed by a Long Short-Term Memory (LSTM) network to capture temporal dependencies.
Additionally, by utilizing the SoundFile and Librosa frameworks, which are used for processing audio, we feed the processed audio into a sequential CNN model for identifying fake speech. By combining these models in a unique detection application, we can effectively detect deepfakes that incorporate both visual and auditory manipulations. We can also consider cases involving solely video or audio sources.
Our experimental results demonstrate an accuracy of approximately 83% for detection of video-based deepfakes and 92% of audio-based deepfakes. To ensure widespread accessibility, we have developed a user-friendly web application that allows users to upload suspected deepfake content and receive a probability score indicating its authenticity.
To further enhance the model's performance, a comprehensive hyperparameter optimization study is recommended exploring various combinations of parameters such as loss function, number of epochs, learning rate etc. Additionally, augmenting the training dataset with a diverse range of video and audio content could be beneficial.

## Installation
1.	To install Manipulated Reality, you need to use Python 3.11.3.
2.	Install Node.js 20.11.1, which you can download from this [blog release](https://nodejs.org/en/blog/release/v20.11.1).
3.	Open Git Bash Change the current working directory to the location where you want the cloned directory. Run: `git clone https://github.com/MaximL98/Manipulated-Reality.git `, Press Enter to create your local clone
4.	Once you clone the repository, `run pip install -r requirements.txt` (preferable on a virtual environment via [venv](https://docs.python.org/3/library/venv.html) or [Anaconda](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)), This will install all the dependencies from the given requirements file.
5.	Run `pip install tensorflow`.
6.	Some users might get an error when installing face_recognition library, follow the instructions from this [Github repository](https://github.com/z-mahmud22/Dlib_Windows_Python3.x) to install Dlib (version 3.12) compiled binary wheels on windows x64 OS. After installing, run `pip install -r requirrments.txt` again.
7.	Navigate into the app directory where package-lock.json file is located, meaning the folder named “frontend” (PATH\Manipulated-Reality\frontend). From there run in the terminal, `npm install`. This command will install all the dependencies related to the website application.
8.	Download the models files from the following [Google Drive folder](https://drive.google.com/drive/folders/1L758Rllh4s8ROEiuiqKHcRh5aefXOxpn?usp=sharing).
9.	Place the `Audio_detection_model.keras` and `RobustScaler.plk` in the AudioTraining folder, as for the other two files, create a folder named *models* inside the *video_analysis* folder and place them there.
10.	In the backend folder, create a new folder named static. Inside that folder, create two new folders one named *audio* and the second *videos*.
11.	To run the website, open two terminals. Run `python .\server.py` from the root path (PATH\Manipulated-Reality). In the second terminal navigate to the frontend folder 
(cd .\frontend\), and run `npm start`. Which will run the website at http://localhost:3000/


## Usage
### Youtube demonstration video
[![Manipulated Reality demonstration on YouTube](https://img.youtube.com/vi/7F7X8T10rSU/0.jpg)](https://www.youtube.com/watch?v=7F7X8T10rSU)

Click on the image above to watch the video.

### Tools used
[![Skills](https://skillicons.dev/icons?i=py,sqlite,react,nodejs,flask)](https://skillicons.dev)

## Authors
- [@DimaKyn](https://github.com/DimaKyn)
- [@MaximL98](https://github.com/MaximL98)
