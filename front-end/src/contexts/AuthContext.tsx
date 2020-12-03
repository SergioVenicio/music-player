import React, {
  createContext,
  useCallback,
  useContext,
  useState
} from "react";

import jwt_decode from "jwt-decode";

import api from "../services/api";

import useToastContext from './ToastContext';

interface SignInCredentials {
  email: string;
  password: string;
}

interface User {
  id: number;
  name: string;
  email: string;
  avatar: string;
}

interface JWToken {
  user_id: number;
  user: User
}

interface AuthContextState {
  user: User;
  signIn({ email, password }: SignInCredentials): Promise<void>;
  signOut(): void;
  updateUser(user: User): void;
}
const AuthContext = createContext<AuthContextState>({} as AuthContextState);

interface AuthState {
  token: string;
  user: User;
}
const AuthContextProviver: React.FC = ({ children }) => {
  const { addToast } = useToastContext();
  const [data, setData] = useState<AuthState>(() => {
    const token = localStorage.getItem("@MUSIC_PLAYER:token");
    const user = localStorage.getItem("@MUSIC_PLAYER:user");

    if (token && user) {
      api.defaults.headers.authorization = `Bearer ${token}`;
      return {
        token: token,
        user: JSON.parse(user),
      };
    }

    return {} as AuthState;
  });

  const signIn = useCallback(
    async ({ email, password }: SignInCredentials): Promise<void> => {
      const { data } = await api.post("/api/v1/token", {
        email,
        password,
      });

      const { access } = data;
      const { user_id, user }  = jwt_decode(access) as JWToken;

      api.defaults.headers.authorization = `Bearer ${access}`;
      localStorage.setItem("@MUSIC_PLAYER:token", access);
      localStorage.setItem("@MUSIC_PLAYER:user", JSON.stringify({
        ...user,
        id: user_id
      }));

      setData({
        user: {          
          ...user,
          id: user_id,
        } as User,
        token: access,
      });

      addToast({
        title: 'Sigin success',
        type: 'success'
      });
    },
    [addToast]
  );

  const signOut = useCallback(() => {
    setData({} as AuthState);
    localStorage.clear();
  }, []);

  const updateUser = useCallback(
    (user: User) => {
      setData({
        token: data.token,
        user,
      });
      localStorage.setItem("@MUSIC_PLAYER:user", JSON.stringify(user));
    },
    [setData, data.token]
  );

  return (
    <AuthContext.Provider
      value={{ user: data.user, signIn, signOut, updateUser }}
    >
      {children}
    </AuthContext.Provider>
  );
};

const useAuthContext = (): AuthContextState => {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error("Use Auth must be used within AuthContextProviver");
  }

  return context;
};

export default useAuthContext;
export { AuthContextProviver };
