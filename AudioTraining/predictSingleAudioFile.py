from keras import models
import Feature_Extraction_from_sample as feature_extraction
import pickle

SAMPLE_FREQUENCY = 22050

import Feature_Extraction_from_sample as feature_extraction

def predict_single_audio_file(audio_file_path):
    pre_processed = feature_extraction.audio_file_feature_extractor(audio_file_path)
    
    model = models.load_model('Audio_detection_model_1024_batches_5_epochs.keras')


    with open('RobustScaler.pkl', 'rb') as file:
        scaler = pickle.load(file)
    
    #threshold = 0.5
    
    scaled_audio = scaler.transform(pre_processed)
    
    prediction = model.predict(scaled_audio)
    
    #predicted = (prediction >= threshold).astype("int32")
    #return predicted
    
    print(prediction)
    print(prediction.shape)
    
    return prediction


predict_single_audio_file('Dima_recording_real.mp3')



