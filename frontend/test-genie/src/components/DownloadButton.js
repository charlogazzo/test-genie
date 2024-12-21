import React from 'react';

const DownloadButton = ({ downloadUrl, jsonData }) => {
  return (
    <div>
      {downloadUrl && (
        <a href={downloadUrl} download="data.csv">
          <button>Download CSV</button>
        </a>
      )}
      {jsonData && (
        <a href={`data:text/json;charset=utf-8,${encodeURIComponent(JSON.stringify(jsonData))}`} download="data.json">
          <button>Download JSON</button>
        </a>
      )}
    </div>
  );
};

export default DownloadButton;
