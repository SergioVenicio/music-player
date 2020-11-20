import styled from "styled-components";

export const Container = styled.input`
    transition: all 0.5s;
    width: 100%;
    height: 40px;
    border: 1px solid #dfdfdf;
    border-radius: 0;
    padding: 1em;
    line-height: 1.5;
    color: #55595c;
    background-color: #f7f7f9;
    font-weight: 200;
    font-size: 0.90rem;

    &:focus {
        border: 1px solid black;
    }
`
