// src/services/api.js
import axios from 'axios';

const API_URL = 'http://localhost:8000'; // Replace with your FastAPI backend URL

export const generateCSV = async (data) => {
  return axios.post(`${API_URL}/csv-data`, data, {
    responseType: 'blob'
  });
};

export const downloadCSV = async (fileName) => {
  return axios.get(`${API_URL}/download-csv/${fileName}`, {
    responseType: 'blob'
  });
};
