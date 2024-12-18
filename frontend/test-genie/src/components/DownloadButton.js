// src/components/DownloadButton.js
import React from 'react';

const DownloadButton = ({ downloadUrl }) => {
  return (
    downloadUrl && (
      // find a way to get the csv file to be named
      // the name should be the same as what is stored in the server
      <a href={downloadUrl} download="data.csv">
        <button>Download CSV</button>
      </a>
    )
  );
};

export default DownloadButton;
