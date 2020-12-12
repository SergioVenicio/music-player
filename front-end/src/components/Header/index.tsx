import React from 'react';
import { useHistory } from 'react-router';

import Logo from '../Logo'

import {
  Container,
  Content,
  Menu,
  MenuItem
} from './styles'

const Header: React.FC = () => {
  const history = useHistory();

  return (
    <Container>
      <Content>
        <Logo/>
        <Menu>
          <MenuItem onClick={() => history.push('/genre/new')}>Genres</MenuItem>
          <MenuItem onClick={() => history.push('/band/new')}>Bands</MenuItem>
          <MenuItem onClick={() => history.push('/album/new')}>Albums</MenuItem>
          <MenuItem onClick={() => history.push('/music/new')}>Music</MenuItem>
        </Menu>
      </Content>
    </Container>
  )
}

export default Header;
