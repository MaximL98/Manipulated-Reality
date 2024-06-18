import React, { useState, useEffect } from 'react';

function App() {
  const [data, setData] = useState({ members: [] }); 

  useEffect(() => {
    fetch("/upload")
      .then(res => res.json())
      .then(data => setData(data)); // Update entire data state
  }, []);

  return (
      <form action='upload' method="post" encType="multipart/form-data">
        <input type="file" name='video' accept="mp4,mkv,avi" />
        <button>Upload</button>
      </form>
  );
}

export default App;