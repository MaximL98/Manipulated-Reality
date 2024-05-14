### Abstract
Deepfakes, a synthetic type of media created using artificial intelligent technics, pose a growing threat, leveraging the artificial intelligence sophisticated power to create convincing social, political, and general day-to-day misinformation. This capstone project investigates a deepfake detection approach utilizing deep learning technics to create multimodal analysis models. The system will analyze eye and mouth movements within video frames, along with voice characteristics, to identify deepfakes. Users will be able to upload videos, the system will preprocess them using established libraries like Face-Recognition and OpenCV for facial landmark detection and extraction of mouth and eye region. Audio extraction leverages libraries like MoviePy and SpeechRecognition. The system will include three separate machine learning models, each built upon a Convolutional Neural Networks which are deep learning algorithms particularly adept at image and video analysis, each model specifically trained for video and or audio data respectively, are employed for analysis. Training data consists of short-form videos from the FaceForensics++, Celeb-DF, DFDC datasets for video, and human speech audio files from WaveFake, In-The-Wild, Deep-Voice datasets for audio. Each model outputs a probability score indicating the likelihood of the input being a deepfake. The system integrates with a user-friendly web application built with Django and JavaScript to facilitate video/audio upload and result visualization. This work acknowledges the limitations and challenges inherent in developing these deepfake detection models. Especially, it considers the ongoing advancements in deepfake generation techniques that require continuous adaptation of detection models, alongside the ever-growing computational demands such models place on training resources.


## Authors
- [@DimaKyn](https://github.com/DimaKyn)
- [@MaximL98](https://github.com/MaximL98)
