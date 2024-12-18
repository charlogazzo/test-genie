// src/App.js
import React, { useState } from 'react';
import HeaderForm from './components/HeaderForm';
import DownloadButton from './components/DownloadButton';
import './App.css';

function App() {
  const [downloadUrl, setDownloadUrl] = useState(null);

  return (
    <div className="App">
      <h1>CSV Generator</h1>
      <HeaderForm setDownloadUrl={setDownloadUrl} />
      <DownloadButton downloadUrl={downloadUrl} />
    </div>
  );
}

export default App;
