import axios from 'axios';

const API_URL = 'http://localhost:8000'; // Replace with your FastAPI backend URL

export const generateCSV = async (data) => {
  return axios.post(`${API_URL}/csv-data`, data, {
    responseType: 'blob'
  });
};

export const generateJSON = async (data) => {
  return axios.post(`${API_URL}/json-data`, data, {
    responseType: 'json'
  });
};

export const generateSQL = async (data) => {
  return axios.post(`${API_URL}/sql-data`, data, {
    responseType: 'blob'
  });
};

export const downloadCSV = async (fileName) => {
  return axios.get(`${API_URL}/download-csv/${fileName}`, {
    responseType: 'blob'
  });
};

export const downloadJSON = async (fileName) => {
  return axios.get(`${API_URL}/download-json/${fileName}`, {
    responseType: 'json'
  });
};

export const downloadSQL = async (fileName) => {
  return axios.get(`${API_URL}/download-sql/${fileName}`, {
    responseType: 'blob'
  });
};
