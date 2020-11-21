import React, { ButtonHTMLAttributes } from 'react';

import { Container } from './styles';

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
    backgroundColor?: string;
    color?: string;
}

const Button: React.FC<ButtonProps> = ({
    type, backgroundColor, color, children, onClick
}) => {
    return (
        <Container
            type={type}
            backgroundColor={backgroundColor}
            color={color}
            onClick={onClick}
        >
            { children }
        </Container>
    )
}

export default Button;
