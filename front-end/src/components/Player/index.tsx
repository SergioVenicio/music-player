import React, {useEffect, useState} from 'react';

import useAuthContext from '../../contexts/AuthContext';
import usePlayerContext from '../../contexts/PlayerContext';

import { FaHeart, FaRegHeart } from 'react-icons/fa';

import { Container, AlbumImage, AlbumInfo, Favorite } from './styles';

interface IMusic {
    id: number;
    name: string;
    duration: string;
    order: number;
}
interface Album {
    name: string;
    released_date: string;
    cover_image: string;
}
interface PlayerProps {}

const Player: React.FC<PlayerProps> = () => {
    const { user } = useAuthContext();
    const { album, musics, favorites } = usePlayerContext(); 
    const [currentMusic, setCurrentMusic] = useState<IMusic>();
    const [isFavorite, setIsFavorite] = useState(false);

    useEffect(() => {
        const currentId = currentMusic?.id;
        const favoritesId = favorites?.map(({ id }) => id);
        if (currentId && favoritesId.length > 0) {
            setIsFavorite(favoritesId.includes(currentId));
        }
    }, [favorites, currentMusic])

    useEffect(() => {
        const firstMusic = musics.sort((a, b) => {
            return a.order - b.order
        }) as IMusic[];
        setCurrentMusic(firstMusic[0]);
    }, [musics])

    const renderContainer = () => {
        return !!user && currentMusic ? (
            <Container>
                <AlbumImage>
                    <img src={album.cover_image} alt={album.name} />
                </AlbumImage>
                <AlbumInfo>
                    <h5>{album.name}</h5> 
                    <Favorite isFavorite={isFavorite}>
                        {isFavorite ? <FaHeart /> : <FaRegHeart />}
                    </Favorite>
                    {currentMusic && <p>{currentMusic.name}</p>}
                </AlbumInfo>    
            </ Container>
        ): null;
    }

    return renderContainer()
}

export default Player;
