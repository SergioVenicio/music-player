import React, { useCallback, useEffect } from 'react';
import {
  FiAlertCircle,
  FiXCircle,
  FiCheckCircle,
  FiInfo,
} from 'react-icons/fi';

import useToastContext, { ToastMessage } from '../../../contexts/ToastContext';

import { Container } from './styles';

const icons = {
  info: <FiInfo size={24} />,
  error: <FiAlertCircle size={24} />,
  success: <FiCheckCircle size={24} />,
};

interface ToastProps {
  message: ToastMessage;
  style: object;
}
const Toast: React.FC<ToastProps> = ({ message, style }) => {
  const { removeToast } = useToastContext();

  useEffect(() => {
    const timer = setTimeout(() => {
      removeToast(message.id);
    }, 3000);

    return () => {
      clearTimeout(timer);
    };
  }, [message.id, removeToast]);

  const renderIcon = useCallback(() => {
    if (message.type !== 'music') {
      return icons[message.type || 'info']
    }

    return (<img src={message.image} alt={message.title} />)
  }, [message])

  return (
    <Container
      key={message.id}
      hasDescription={Number(!!message.description)}
      type={message.type}
      style={style}
    >
      
      {renderIcon()}

      <div>
        <strong>{message.title}</strong>
        {!!message.description && <p>{message.description}</p>}
      </div>

      <button type='button'>
        <FiXCircle size={18} onClick={() => removeToast(message.id)} />
      </button>
    </Container>
  );
};

export default Toast;
