import React from 'react';

import { AuthContextProviver } from './AuthContext';
import { ToastContextProvider } from './ToastContext';
import { PlayerContextProvider } from './PlayerContext';

const AppProvider: React.FC = ({ children }) => (
  <ToastContextProvider>
    <AuthContextProviver>
      <PlayerContextProvider>
        {children}
      </PlayerContextProvider>
    </AuthContextProviver>
  </ToastContextProvider>
);

export default AppProvider;
