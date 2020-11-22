import axios from 'axios';

const backEndUrl = process.env.REACT_APP_BACKEND_DOMAIN || 'localhost:8000';
export default axios.create({
  baseURL: `http://${backEndUrl}`,
});
