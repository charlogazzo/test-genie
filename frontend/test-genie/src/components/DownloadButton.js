// src/components/DownloadButton.js
import React from 'react';

const DownloadButton = ({ downloadUrl }) => {
  return (
    downloadUrl && (
      <a href={downloadUrl} download="data.csv">
        <button>Download CSV</button>
      </a>
    )
  );
};

export default DownloadButton;
