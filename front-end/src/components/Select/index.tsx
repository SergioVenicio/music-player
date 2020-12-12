import React from 'react';

import {Container} from './styles';

interface IOption {
  id: number,
  value: string
}

interface SelectProps {
  onChange(e: React.ChangeEvent<HTMLSelectElement>): void
  validOptions: IOption[]
}
const Select = ({validOptions, onChange}: SelectProps) => {
  const renderOptions = () => {
    return (
      validOptions.map(({id, value}) => (
        <option key={id} value={id}>{value}</option>
      ))
    )
  }

  return (
    <Container onChange={onChange}>
      <option>Choice a option</option>
      {renderOptions()}
    </Container>
  )
}

export default Select;
