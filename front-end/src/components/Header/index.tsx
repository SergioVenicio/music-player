import React from 'react';
import { useHistory } from 'react-router';

import Logo from '../Logo'

import { Container, Content } from './styles'

const Header: React.FC = () => {
  const history = useHistory();

  return (
    <Container>
        <Content onClick={() => history.push('/')} >
                <Logo />
        </Content>
    </Container>
  )
}

export default Header;
