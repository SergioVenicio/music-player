import React from 'react';
import { useHistory } from 'react-router';

import logo from '../../assets/logo.png';

const Logo: React.FC = () => {
  const history = useHistory();

  return (
    <img src={logo} alt="Music Player" onClick={() => history.push('/') }/>
  )
}

export default Logo;
