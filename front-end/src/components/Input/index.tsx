import React, { InputHTMLAttributes } from 'react';

import { Container } from './styles'

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
	name: string;
	type: string;
	placeholder?: string;
	value?: string;
	onChange?: (e: React.ChangeEvent<HTMLInputElement>) => void;
  inputRef?: React.RefObject<HTMLInputElement>
}

const Input = ({name, type, placeholder, value, onChange, inputRef} : InputProps) => {
	return <Container
		name={name}
		type={type}
		placeholder={placeholder}
		value={value}
		onChange={onChange}
    ref={inputRef}
	/>
}

export default Input;
