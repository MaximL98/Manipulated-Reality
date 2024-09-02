from keras import models
import AudioTraining.Feature_Extraction_from_sample as feature_extraction
import pickle


SAMPLE_FREQUENCY = 22050

def predict_single_audio_file(audio_file_path):
    print("Starting audio pre-processing...")
    pre_processed = feature_extraction.audio_file_feature_extractor(audio_file_path)
    
    print("Loading audio detection model...")
    model = models.load_model('AudioTraining/Audio_detection_model_1024_batches_5_epochs.keras')


    with open('AudioTraining/RobustScaler.pkl', 'rb') as file:
        scaler = pickle.load(file)
    
    #threshold = 0.5
    
    scaled_audio = scaler.transform(pre_processed)
    print("Starting audio prediction...")
    prediction = model.predict(scaled_audio)
    
    #predicted = (prediction >= threshold).astype("int32")
    #return predicted
    prediction = prediction.tolist()
    numberOfSamples = len(prediction)
    totalSum = 0
    for i in range(numberOfSamples):
        totalSum += prediction[i][0]
    
    result = totalSum / numberOfSamples
    return result




