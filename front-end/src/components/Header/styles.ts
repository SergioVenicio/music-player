import styled from "styled-components";


export const Container = styled.div`
  position: relative;
  max-width: 100%;
  width: 100%;
  height: 45px;
  margin-bottom: 45px;
`

export const Content = styled.header`
  max-width: 1024em;
  padding-top: 0.5rem;
  padding-bottom: 0.5em;
  background-color: #343a40;
  display: flex;

  > img {
    cursor: pointer;
    margin-left: 0.5em;
    margin-right: 5rem;
    height: 5em;
  }
`

export const Menu = styled.div``;


export const MenuItem = styled.a`
    cursor: pointer;
    display: inline-block;
    width: 5rem;
    height: 100%;
    margin-left: 1rem;
    line-height: 5rem;
    text-align: center;

    &:hover {
        background-color: #2b2f33;
    }
`;
