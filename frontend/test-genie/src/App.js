import React, { useState } from 'react';
import HeaderForm from './components/HeaderForm';
import DownloadButton from './components/DownloadButton';
import './App.css';

function App() {
  const [downloadUrl, setDownloadUrl] = useState(null);
  const [jsonData, setJsonData] = useState(null);

  return (
    <div className="App">
      <h1>CSV/JSON Generator</h1>
      <HeaderForm setDownloadUrl={setDownloadUrl} setJsonData={setJsonData} />
      <DownloadButton downloadUrl={downloadUrl} jsonData={jsonData} />
    </div>
  );
}

export default App;
