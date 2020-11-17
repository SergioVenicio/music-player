import React from 'react';

import GlobalStyle from "./styles/global";

import AppProvider from "./contexts";

import Header from './components/Header';

const App = () => {
  return (
    <>
      <div className="App">
        <AppProvider>
          <Header />
        </AppProvider>
      </div>
      <GlobalStyle />
    </>
  );
}


export default App;