import React, { createContext, useCallback, useContext, useState, useEffect } from 'react';

import useAuthContext from './AuthContext';

import api from '../services/api';

interface IAlbum {
    id: number;
    name: string;
    released_date: string;
    cover_image: string;
}

interface IMusic {
    id: number;
    name: string;
    order: number;
    file: string;
    file_type: string;
    duration: string;
}

interface PlayerContextState {
    musics: IMusic[];
    favorites: ILike[];
    album: IAlbum;
    setPlayerAlbum: (album: IAlbum) => Promise<void>;
}

interface ILike {
    id: number;
    user_id: number;
    music_id: number;
}

const PlayerContext = createContext<PlayerContextState>({} as PlayerContextState);

const PlayerContextProvider: React.FC = ({ children }) => {
    const albumKey = '@MUSIC_PLAYER::PLAYER:album';
    const musicKey = '@MUSIC_PLAYER::PLAYER:musics';

    const [favorites, setFavorites] = useState<ILike[]>(() => []);
    const { user } = useAuthContext();

    const [musics, setMusics] = useState<IMusic[]>(() => {
        const musics = localStorage.getItem(musicKey);
        return musics ? JSON.parse(musics) : [] as IMusic[];
    })

    const [album, setAlbum] = useState<IAlbum>(() => {
        const album = localStorage.getItem(albumKey);
        return album ? JSON.parse(album) : {} as IAlbum;
    })

    const getMusics = useCallback(
        async (album_id: number): Promise<void> => {
            const { data } = await api.get(
                '/api/v1/music', {
                    params: {
                        album_id
                    }
                }
            );
            setMusics(() => {
                const musics = data.results.map((music: IMusic) => music) as IMusic[];
                localStorage.setItem(musicKey, JSON.stringify(musics));
                return musics;
            });
        }, []
    )

    const setPlayerAlbum = useCallback(async (album: IAlbum) => {
        setAlbum(album)
        getMusics(album.id);
        localStorage.setItem(albumKey, JSON.stringify(album));
    }, [getMusics]);

    useEffect(() => {
        if (!user) {
            return;
        }
        api.get('/api/v1/likes', { params: { user_id: user.id }}).then(({ data }) => {
            setFavorites(() => {
                return data.results.map((like: ILike) => like) as ILike[];
            })
        });
    }, [user, musics]);

    return (
        <PlayerContext.Provider
            value={{ musics, album, favorites, setPlayerAlbum }}
        >
                {children}
        </PlayerContext.Provider>
    )
}

const usePlayerContext = (): PlayerContextState => {
    const context = useContext(PlayerContext);
    return context;
}

export default usePlayerContext;
export { PlayerContextProvider };
