import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

import useAuthContext from '../../contexts/AuthContext';
import usePlayerContext from '../../contexts/PlayerContext';

import api from '../../services/api';

import Card from '../../components/Card';

import { Container, CardContainer } from './styles';

interface IAlbum {
    id: number;
    name: string;
    released_date: string;
    cover_image: string;
}

interface IUrlParams {
    band_id: string;
}

const Albums: React.FC = () => {
    const [albums, setAlbums] = useState<IAlbum[]>();
    const { band_id } = useParams<IUrlParams>();
    const { setPlayerAlbum } = usePlayerContext();

    const { signOut } = useAuthContext();

    const handleChoiceAlbum = (album: IAlbum) => {
        setPlayerAlbum(album);
    }

    useEffect(() => {
        api.get(
            '/api/v1/album',
            {
                params: {
                    band_id
                }
            }
        ).then(({ data }) => {
            setAlbums(() => {
                return data.results.map((album: IAlbum) => {
                    return {
                        ...album
                    }
                }) as IAlbum[]
            });
        }).catch((error) => {
            if (error.response.status === 401) {
                signOut();
            }
            console.error(error);
        });
    }, [band_id, signOut]);

    const showCards = () => {
        return albums && albums.map(album => {
            return (
                <CardContainer
                    key={album.id}
                    onClick={() => handleChoiceAlbum(album)}
                >
                    <Card
                        description={album.name}
                        image={album.cover_image}
                    />
                </ CardContainer>
            )
        })
    }
    return (
        <Container>
            {showCards()}
        </Container>
    )
}

export default Albums;
