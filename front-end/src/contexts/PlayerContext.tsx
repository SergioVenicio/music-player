import React, {
  createContext,
  useCallback,
  useContext,
  useState,
  useEffect
} from 'react';

import useAuthContext from './AuthContext';
import useToastContext from './ToastContext';

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
  addFavorite: (music_id: number) => Promise<void>;
  removeFavorite: (like_id: number) => Promise<void>;
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

  const { user, signOut } = useAuthContext();
  const { addToast } = useToastContext();

  const [favorites, setFavorites] = useState<ILike[]>(() => []);

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
      const { data } = await api.get('/api/v1/music', {params: {album_id}});

      setMusics(() => {
        const musics = data.results.map(
          (music: IMusic) => music
        ) as IMusic[];
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

  const getLikes = useCallback(async () => {
    try {
      const { data } = await api.get(
        '/api/v1/likes', { params: { user_id: user.id }}
      );
      setFavorites(() => {
        return data.results.map((like: ILike) => like) as ILike[];
      })
    } catch(error) {
      if (!error.response || error.response.status === 401) {
        signOut();
        addToast({
          title: 'Session Expired',
          type: 'error'
        });
      }
      addToast({
        title: 'cant connect to server',
        description: 'try again later',
        type: 'error'
      });
    }
  }, [user, signOut, addToast]);

  const addFavorite = useCallback(async (music_id: number) => {
    try {
      await api.post('/api/v1/likes', { user_id: user.id, music_id});
      await getLikes();
    } catch(error) {
      if (error.response.status === 401) {
        signOut();
        addToast({
          title: 'Session Expired',
          type: 'error'
        });
      }
      addToast({
        title: 'cant connect to server',
        description: 'try again later',
        type: 'error'
      });
    }
  }, [signOut, user, getLikes, addToast]);

  const removeFavorite = useCallback(async (like_id: number) => {
      try {
        await api.delete(`/api/v1/likes/${like_id}`);
        setFavorites((favorites) => {
          return favorites.filter((fav) => {
            return fav.id !== like_id ? fav : false
          });
        })
      } catch(error) {
        if (error.response.status === 401) {
          signOut();
          addToast({
            title: 'Session Expired',
            type: 'error'
          });
        }
        addToast({
          title: 'cant connect to server',
          description: 'try again later',
          type: 'error'
        });
      }
  }, [signOut, addToast]);

  useEffect(() => {
    if (!user) {
      return;
    }
    getLikes();
  }, [user, musics, signOut, getLikes]);

  return (
    <PlayerContext.Provider
      value={{
        musics,
        album,
        favorites,
        setPlayerAlbum,
        addFavorite,
        removeFavorite
      }}
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
