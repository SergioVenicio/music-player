import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import reportWebVitals from './reportWebVitals';

import path from 'path';
import dotenv from 'dotenv';
import dotenvExpand from 'dotenv-expand';


const envConfig = dotenv.config({
  path: path.resolve(__dirname, '../.env')
});
dotenvExpand(envConfig);

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
