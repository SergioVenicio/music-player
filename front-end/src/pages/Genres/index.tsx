import React, { useState, useEffect } from 'react';
import { useHistory } from 'react-router-dom';

import api from '../../services/api';

import Card from '../../components/Card';

import { Container, CardContainer } from './styles';

interface IGenre {
    id: number;
    description: string;
    genre_image: string;
}

const Genres: React.FC = () => {
    const [genres, setGenres] = useState<IGenre[]>();

    const history = useHistory();
    const navigateToBandPage = (genre_id: number) => {
        history.push(`/bands/${genre_id}`)
    }

    useEffect(() => {
        api.get('/api/v1/genre').then(({ data }) => {
            setGenres(() => {
                return data.results.map((genre: IGenre) => {
                    return {
                        ...genre
                    }
                }) as IGenre[]
            });
        });
    }, []);

    const showCards = () => {
        return genres && genres.map(genre => {
            return (
                <CardContainer
                    key={genre.id}
                    onClick={() => navigateToBandPage(genre.id)}
                >
                    <Card
                        description={genre.description}
                        image={genre.genre_image}
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

export default Genres;
