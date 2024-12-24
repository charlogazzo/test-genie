import React, { useState } from 'react';
import HeaderForm from './components/HeaderForm';
import DownloadButton from './components/DownloadButton';
import './App.css';

function App() {
  const [downloadUrl, setDownloadUrl] = useState(null);
  const [jsonData, setJsonData] = useState(null);
  const [fileType, setFileType] = useState('csv'); // Add state to keep track of file type

  return (
    <div className="App">
      <h1>CSV/JSON/SQL Generator</h1>
      <HeaderForm setDownloadUrl={setDownloadUrl} setJsonData={setJsonData} setFileType={setFileType} />
      <DownloadButton downloadUrl={downloadUrl} jsonData={jsonData} fileType={fileType} />
    </div>
  );
}

export default App;
