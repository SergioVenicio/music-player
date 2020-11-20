import React from "react";

import { AuthContextProviver } from "./AuthContext";
import { PlayerContextProvider } from "./PlayerContext";

const AppProvider: React.FC = ({ children }) => (
    <AuthContextProviver>
        <PlayerContextProvider>
            {children}
        </PlayerContextProvider>
    </AuthContextProviver>
);

export default AppProvider;
