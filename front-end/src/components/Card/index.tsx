import React from 'react';

import { Container } from './styles';

interface CardProps {
	description: string;
	image: string;
}

const Card: React.FC<CardProps> = ({ description, image }) => {
	return (
		<Container>
			<img src={image} alt={description} />
			<p>{ description }</p>
		</ Container>
	)
}

export default Card;
