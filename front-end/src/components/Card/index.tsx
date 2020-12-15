import React from 'react';

import { Container, Content } from './styles';

interface CardProps {
	description: string;
	image: string;
  onClick?: () => void;
}

const Card: React.FC<CardProps> = ({ description, image, onClick }) => {
	return (
		<Container onClick={onClick}>
      <Content>
        <img src={image} alt={description} />
        <p>{ description }</p>
      </Content>
		</ Container>
	)
}

export default Card;
