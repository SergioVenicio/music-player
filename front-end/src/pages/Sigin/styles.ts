import styled from "styled-components";


export const Container = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
`

export const FormWrapper = styled.div`
  width: 35em;
  height: auto;
  display: flex;
  margin-top: 0.5rem;
  flex-direction: column;
  border: 1px solid #dfdfdf;
`

export const FormHeader = styled.div`
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #1a1a1a;
  border-top-left-radius: 5px;
  border-top-right-radius: 5px;

  > img {
    align-self: center;
    height: 10em;
    margin-top: 0.5rem;
    margin-bottom: 0.5rem;
  }
`

export const Form = styled.form`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  padding: 0.5em;
  padding-bottom: 1em;
  padding-top: 1em;
  background: #FFF;

  > input {
    width: 100%;
  }

  > hr {
    margin-top: .75rem;
    margin-bottom: .75rem;
    width: 100%;
    border: 0;
    border-top: 1px solid rgba(0,0,0,0.1);
  }
`

export const FormButtons = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-top: 1px solid rgba(0,0,0,0.1);
  padding-top: 1rem;
  padding-bottom: 1rem;
`