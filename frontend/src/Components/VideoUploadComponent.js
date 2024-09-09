import React, { useState } from 'react';
import ReactPlayer from 'react-player';

const VideoUploadComponent = () => {
  const [videoFile, setVideoFile] = useState(null);
  const [videoUrl, setVideoUrl] = useState('');

  const handleVideoChange = (event) => {
    const file = event.target.files[0];
    setVideoFile(file);
    setVideoUrl(URL.createObjectURL(file));
  };

  return (
    <div>
      <input type="file" accept="video/*" onChange={handleVideoChange} />
      {videoUrl && (
        <ReactPlayer url={videoUrl} width="100%" height="100%" controls={true} />
      )}
    </div>
  );
};

export default VideoUploadComponent;