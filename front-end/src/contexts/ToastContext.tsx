import React, {
    createContext,
    useCallback,
    useContext,
    useState
} from 'react';
import { v4 } from 'uuid';

import ToastContainer from '../components/ToastContainer';

export interface ToastMessage {
    id: string;
    type?: 'success' | 'error' | 'info' | 'music';
    description?: string;
    title: string;
    image?: string;
}

interface ToastContextData {
  addToast(message: Omit<ToastMessage, 'id'>): void;
  removeToast(id: string): void;
}
const toastContext = createContext<ToastContextData>({} as ToastContextData)

const ToastContextProvider: React.FC = ({children}) => {
  const [messages, setMessages] = useState<ToastMessage[]>([])

  const addToast = useCallback(({title, type, description, image}: Omit<ToastMessage, 'id'>) => {
    const id = v4();
    const toast = {
      id,
      title,
      type,
      description,
      image
    }

    setMessages((messages) => [...messages, toast])
  }, [])

  const removeToast = useCallback((id: string) => {
    setMessages((messages) => {
      return messages.filter(message => {
        return message.id !== id ? message : null
      })
    })
  }, [])

  return (
    <toastContext.Provider value={{addToast, removeToast }}>
      {children}
      <ToastContainer messages={messages} />
    </toastContext.Provider>
  )
}


const useToastContext = (): ToastContextData => {
  const context = useContext(toastContext);

  if (!context) {
    throw new Error('useToastContext must be used within ToastContextProviver');
  }

  return context;
}

export default useToastContext;
export { ToastContextProvider }
