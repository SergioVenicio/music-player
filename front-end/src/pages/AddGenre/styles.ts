import styled from 'styled-components'

export const Container = styled.div`
    width: 100%;
    margin-top: 5rem;
    display: flex;
    align-items: center;
    justify-content: center;
`

export const Form = styled.form`
    width: 45rem;
    & > input {
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
    }

`

export const ButtonWrapper = styled.div`
    display: flex;
    align-items: center;
    justify-content: center;

    & > button {
        width: 15rem;
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
        align-self: center;
    }
`

export const FileWrapper = styled.div`
    display: none;
`
