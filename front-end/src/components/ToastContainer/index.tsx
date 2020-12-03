import React from 'react'

import { useTransition } from 'react-spring'

import Toast from './Toast'
import { Container } from './styles'

import { ToastMessage } from '../../contexts/ToastContext'

interface ToastContainerParams {
  messages: ToastMessage[]
}
const ToastContainer: React.FC<ToastContainerParams> = ({ messages }) => {
  const transitionConfig = {
    from: { right: '-120%', opacity: 0 },
    enter: { right: '0', opacity: 1 },
    leave: { right: '-120%', opacity: 0 },
  }
  const messagesWithTransitions = useTransition(
    messages,
    messages => messages.id,
    transitionConfig
  )
  return (
    <Container>
      {messagesWithTransitions.map(({item, key, props}) => (
        <Toast key={key} message={item} style={props} />
      ))}
    </Container>
  )
}

export default ToastContainer
