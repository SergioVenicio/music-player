import styled from 'styled-components';

interface ContainerProps {
    backgroundColor?: string;
    color?: string;
}
export const Container = styled.button<ContainerProps>`
    width: 5rem;
    height: 2.5rem;
    border: none;
    bortder-radius: 0;
    font-size: 0.75rem;
    cursor: pointer;
    font-weight: 600;

    background-color: ${
        (props) => props?.backgroundColor ? props.backgroundColor : '#1a1a1a'
    };
    color: ${
        (props) => props?.color ? props.color : '#fafafa'
    };
 `
