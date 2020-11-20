import styled from "styled-components";

export const Container = styled.div`
    position: absolute;
    width: 100%;
    height: 70px;
    background: #343a40;
    bottom: 0;
`;

export const AlbumImage = styled.div`
    position: relative;
    float: left;
    display: block;
    height: 50px;
    height: 3.3em;
    margin-top: 0.6em;
    margin-left: 0.5em;
    width: 85px;

    & img {
        height: 100%;
        width: 100%;
        border-radius: 2px;
    }
`;

export const AlbumInfo = styled.div`
    float: left;
    margin-top: 1rem;
    margin-left: 0.6rem;

    & h5 {
        display: inline;
    }
    & p {
        font-size: 0.7rem;
    }
`;

interface FavoriteProps {
    isFavorite: boolean;
}
export const Favorite = styled.div<FavoriteProps>`
    display: inline;
    margin-left: 1rem;
    cursor: pointer;
`;
