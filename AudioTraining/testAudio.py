import predictAudioFile as paf


def test_audio():
    prediction = paf.predict_single_audio_file("ReallyGoodDeepfake.mp3")
    print(prediction)
    
test_audio()