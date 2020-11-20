import React from 'react';
import { BrowserRouter } from 'react-router-dom'

import GlobalStyle from "./styles/global";

import AppProvider from "./contexts";

import Routes from './routes'

import Header from './components/Header';
import Player from './components/Player';

const App = () => {
  return (
    <>
      <div className="App">
        <BrowserRouter>
          <AppProvider>
            <Header />
            <Routes />
            <Player />
          </AppProvider>
        </BrowserRouter>
      </div>
      <GlobalStyle />
    </>
  );
}


export default App;
