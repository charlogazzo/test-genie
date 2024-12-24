import React from 'react';

const DownloadButton = ({ downloadUrl, jsonData, fileType }) => {
  const getDownloadName = () => {
    switch (fileType) {
      case 'csv':
        return 'data.csv';
      case 'json':
        return 'data.json';
      case 'sql':
        return 'data.sql';
      default:
        return 'download';
    }
  };

  return (
    <div>
      {fileType === 'csv' && downloadUrl && (
        <a href={downloadUrl} download={getDownloadName()}>
          <button>Download CSV</button>
        </a>
      )}
      {fileType === 'json' && jsonData && (
        <a href={`data:text/json;charset=utf-8,${encodeURIComponent(JSON.stringify(jsonData, null, 4))}`} download={getDownloadName()}>
          <button>Download JSON</button>
        </a>
      )}
      {fileType === 'sql' && downloadUrl && (
        <a href={downloadUrl} download={getDownloadName()}>
          <button>Download SQL</button>
        </a>
      )}
    </div>
  );
};

export default DownloadButton;
