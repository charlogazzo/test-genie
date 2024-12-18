// src/components/HeaderForm.js
import React, { useState } from 'react';
import axios from 'axios';
import { generateCSV } from '../services/api';
import './HeaderForm.css'

const HeaderForm = ({ setDownloadUrl }) => {
  const [headers, setHeaders] = useState([{ name: '', description: '', sample_data: [''] }]);

  const handleAddHeader = () => {
    setHeaders([...headers, { name: '', description: '', sample_data: [''] }]);
  };

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

  const handleSubmit = async (event) => {
    event.preventDefault();
    const requestData = { headers, number_of_records: 10 }; // Adjust number of records as needed

    try {
      const response = await generateCSV(requestData);
      const url = window.URL.createObjectURL(new Blob([response.data]));
      setDownloadUrl(url);
    } catch (error) {
      console.error('Error generating CSV:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
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
      <button type="button" onClick={handleAddHeader}>Add Header</button>
      <button type="submit">Generate CSV</button>
    </form>
  );
};

export default HeaderForm;
