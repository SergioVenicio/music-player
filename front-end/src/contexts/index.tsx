import React from "react";

import { AuthContextProviver } from "./AuthContext";

const AppProvider: React.FC = ({ children }) => (
  <AuthContextProviver>{children}</AuthContextProviver>
);

export default AppProvider;