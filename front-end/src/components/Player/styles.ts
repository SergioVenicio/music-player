import styled from "styled-components";

export const Container = styled.div`
    position: absolute;
    display: grid;
    grid-template-columns: auto auto 1fr;
    width: 100%;
    height: 70px;
    background: #343a40;
    bottom: 0;
`;

export const AlbumImage = styled.div`
    height: 3.8em;
    margin-top: 0.3em;
    margin-left: 0.3em;
    width: auto;
    max-width: 8rem;

    & img {
        height: 100%;
        width: 100%;
        border-radius: 2px;
    }
`;

export const AlbumInfo = styled.div`
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
    position: absolute;
    margin-left: 1.5rem;
    cursor: pointer;
`;

export const PlayerControls = styled.div`
    display: flex;
    position: absolute;
    width: auto;
    left: 45%;
    margin-top: 0.2rem;
`

export const BackFowardBtn = styled.div`
    cursor: pointer;
    width: 5rem;
    margin-top: 1rem;
`

export const FowardBtn = styled.div`
    cursor: pointer;
    margin-left: 4rem;
    margin-top: 1rem;
`

export const PlayBtn = styled.div`
    cursor: pointer;
`

export const VolumeBar = styled.div`
    display: inline;
    position: absolute;
    right: 1rem;
    top: 2rem;

    & input {
        margin-left: 0.5rem;
        margin-top: 0.3rem;
        width: 10rem;
        height: 0.3rem;
        float: right;
    }

    & input:focus {
        outline: none;
    }

    & input::-webkit-slider-thumb {
      -webkit-appearance: none;
      border: 1px solid #000;
    }

    & input::-moz-range-thumb {
        box-shadow: 1px 1px 1px #000000, 0px 0px 1px #0d0d0d;
        border: 1px solid #fff;
        height: 14px;
        width: 14px;
        border-radius: 8px;
        background: #ffffff;
        cursor: pointer;
    }


    & svg {
        float: left;
    }

    & input::-ms-thumb {
        box-shadow: 1px 1px 1px #000000, 0px 0px 1px #0d0d0d;
        border: 1px solid #000000;
        height: 6px;
        width: 6px;
        border-radius: 3px;
        background: #ffffff;
        cursor: pointer;
    }

    & input::-ms-track {
        height: 0.5rem;
        width: 100%;
        cursor: pointer;
        background: white;
        color: white;
    }
`

export const TimerSlider = styled.div`
    position: absolute;
    margin-top: 3rem;
    width: 20.5rem;
    margin-left: 40%;


    & input {
        margin-left: 0.5rem;
        margin-top: 0.3rem;
        width: 100%;
        height: 0.2rem;
    }

    & input:focus {
        outline: none;
    }

    & input::-webkit-slider-thumb {
      -webkit-appearance: none;
      border: 0.8px solid #000;
    }

    & input::-moz-range-thumb {
        box-shadow: 1px 1px 1px #000000, 0px 0px 1px #0d0d0d;
        border: 1px solid #fff;
        height: 10px;
        width: 10px;
        border-radius: 8px;
        background: #ffffff;
        cursor: pointer;
    }


    & svg {
        float: left;
    }

    & input::-ms-thumb {
        box-shadow: 1px 1px 1px #000000, 0px 0px 1px #0d0d0d;
        border: 1px solid #000000;
        height: 6px;
        width: 6px;
        border-radius: 3px;
        background: #ffffff;
        cursor: pointer;
    }

    & input::-ms-track {
        height: 0.5rem;
        width: 100%;
        cursor: pointer;
        background: white;
        color: white;
    }
`
