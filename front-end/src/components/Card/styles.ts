import styled from 'styled-components';


export const Content = styled.div`
    color: #919aa1;
    font-family: 'Roboto Slab' serif;
    font-size: 17px;
    font-weight: 400;

    & p {
        padding: 0.5rem 1rem;
    }

    & img {
        width: 300px;
        max-height: 10.5rem;
    }
`;

export const Container = styled.div`
	display: flex;
	position: relative;
	flex-direction: column;
	border: 1px solid #dfdfdf;
	float: left;
	margin-bottom: 1.5rem;
	margin-left: 5rem;
    height: 13.8rem;
    transition: all 0.3s;

    &:hover {
        border-color: #323436;
        box-shadow: 1px 1px 4px 2px rgba(50, 52, 54, 0.50);
    }

    &:hover p {
        color: #323436;
    }

`;
