import React from 'react';

import Logo from '../Logo'

import { Container, Content } from './styles'

const Header: React.FC = () => {
  return (
    <Container>
      <Content>
        <Logo />
      </Content>
    </Container>
  )
}

export default Header;