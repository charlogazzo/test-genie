import React, { useState } from 'react';
import { generateCSV, generateJSON, generateSQL } from '../services/api';
import './HeaderForm.css';

const HeaderForm = ({ setDownloadUrl, setJsonData, setFileType }) => {
  const [headers, setHeaders] = useState([{ name: '', description: '', sample_data: [''] }]);
  const [fileType, internalSetFileType] = useState('csv'); // State to handle file type selection
  const [tableName, setTableName] = useState(''); // State to handle table name for SQL
  const [createTable, setCreateTable] = useState(false); // State to handle CREATE TABLE option for SQL

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

  const handleFileTypeChange = (event) => {
    internalSetFileType(event.target.value);
    setFileType(event.target.value); // Update the parent component's state
  };

  const handleTableNameChange = (event) => {
    setTableName(event.target.value);
  };

  const handleCreateTableChange = (event) => {
    setCreateTable(event.target.checked);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const requestData = {
      headers,
      number_of_records: 10, // Adjust number of records as needed
      table_name: tableName,
      create_table: createTable ? 'CREATE TABLE' : '' // Set CREATE TABLE option
    };

    try {
      if (fileType === 'csv') {
        const response = await generateCSV(requestData);
        const url = window.URL.createObjectURL(new Blob([response.data]));
        setDownloadUrl(url);
        setJsonData(null);
      } else if (fileType === 'json') {
        const response = await generateJSON(requestData);
        setJsonData(response.data);
        setDownloadUrl(null);
      } else if (fileType === 'sql') {
        const response = await generateSQL(requestData);
        const url = window.URL.createObjectURL(new Blob([response.data], { type: 'text/plain' }));
        setDownloadUrl(url);
        setJsonData(null);
      }
    } catch (error) {
      console.error(`Error generating ${fileType.toUpperCase()}:`, error);
    }
  };

  return (
    <form className="header-form" onSubmit={handleSubmit}>
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
      <div className="dropdown">
        <label htmlFor="fileType">Select File Type:</label>
        <select id="fileType" value={fileType} onChange={handleFileTypeChange}>
          <option value="csv">CSV</option>
          <option value="json">JSON</option>
          <option value="sql">SQL</option>
        </select>
      </div>
      {fileType === 'sql' && (
        <div className="sql-options">
          <input
            type="text"
            name="table_name"
            placeholder="Table Name"
            value={tableName}
            onChange={handleTableNameChange}
            required
          />
          <label>
            <input
              type="checkbox"
              name="create_table"
              checked={createTable}
              onChange={handleCreateTableChange}
            />
            Include CREATE TABLE statement
          </label>
        </div>
      )}
      <div className="buttons">
        <button type="button" onClick={handleAddHeader}>Add Header</button>
        <button type="submit">Generate File</button>
      </div>
    </form>
  );
};

export default HeaderForm;
