import React, { useState } from 'react';
import { generateCSV, generateJSON } from '../services/api';
import './HeaderForm.css';

const HeaderForm = ({ setDownloadUrl, setJsonData }) => {
  const [headers, setHeaders] = useState([{ name: '', description: '', sample_data: [''] }]);

  const handleAddHeader = () => setHeaders([...headers, { name: '', description: '', sample_data: [''] }]);

  const handleInputChange = (index, event) => {
    const { name, value } = event.target;
    const newHeaders = [...headers];
    if (name === 'sample_data') {
      newHeaders[index][name] = value.split(',').map(item => item.trim());
    } else {
      newHeaders[index][name] = value;
    }
    setHeaders(newHeaders);
  };

  const handleCSVSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await generateCSV({ headers, number_of_records: 10 });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      setDownloadUrl(url);
    } catch (error) {
      console.error('Error generating CSV:', error);
    }
  };

  const handleJSONSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await generateJSON({ headers, number_of_records: 10 });
      setJsonData(response.data);
    } catch (error) {
      console.error('Error generating JSON:', error);
    }
  };

  return (
    <form className="header-form">
      {headers.map((header, index) => (
        <div key={index} className="header-row">
          <input
            type="text"
            name="name"
            placeholder="Header Name"
            value={header.name}
            onChange={(e) => handleInputChange(index, e)}
            required
          />
          <input
            type="text"
            name="description"
            placeholder="Description"
            value={header.description}
            onChange={(e) => handleInputChange(index, e)}
          />
          <input
            type="text"
            name="sample_data"
            placeholder="Sample Data (comma separated)"
            value={header.sample_data.join(', ')}
            onChange={(e) => handleInputChange(index, e)}
          />
        </div>
      ))}
      <div className="buttons">
        <button type="button" onClick={handleAddHeader}>Add Header</button>
        <button type="submit" onClick={handleCSVSubmit}>Generate CSV</button>
        <button type="submit" onClick={handleJSONSubmit}>Generate JSON</button>
      </div>
    </form>
  );
};

export default HeaderForm;
