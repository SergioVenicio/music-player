import React, {
  useEffect,
  useState,
  useCallback,
  useRef
} from 'react';

import useAuthContext from '../../contexts/AuthContext';
import useToastContext from '../../contexts/ToastContext';
import usePlayerContext from '../../contexts/PlayerContext';

import {
  FaHeart,
  FaRegHeart,
  FaBackward,
  FaForward,
  FaRegPlayCircle,
  FaRegPauseCircle,
  FaVolumeUp
} from 'react-icons/fa';

import {
  Container,
  AlbumImage,
  AlbumInfo,
  Favorite,
  PlayerControls,
  FowardBtn,
  BackFowardBtn,
  PlayBtn,
  VolumeBar,
  TimerSlider
} from './styles';

interface IMusic {
  id: number;
  name: string;
  duration: string;
  order: number;
  file: string;
  file_type: string;
}

interface PlayerProps {}

const Player: React.FC<PlayerProps> = () => {
  const { user } = useAuthContext();
  const { addToast } = useToastContext();
  const {
    album,
    musics,
    favorites,
    addFavorite,
    removeFavorite
  } = usePlayerContext(); 

  const [currentMusic, setCurrentMusic] = useState<IMusic>();

  const [volume, setVolume] = useState(1.0);
  const [isFavorite, setIsFavorite] = useState(false);
  const [isPaused, setIsPause] = useState(true);
  const [timeElapsed, setTimeElapsed] = useState(0);

  const playerRef = useRef<HTMLAudioElement>(null);

  const handleNext = useCallback(() => {
    const musicOrder = musics.filter((music) => {
      return music.order === (currentMusic as IMusic).order + 1 ? music: false
    })
    if (!musicOrder) {
      setIsPause(true);
    } else if (musicOrder[0] && musicOrder[0].id !== currentMusic?.id) {
      setCurrentMusic(musicOrder[0]);
    }
  }, [currentMusic, musics])

  const handlePreview = useCallback(() => {
    const musicOrder = musics.filter((music) => {
      return music.order === (currentMusic as IMusic).order - 1 ? music: false
    })

    if (musicOrder[0].id !== currentMusic?.id) {
      setCurrentMusic(musicOrder[0]);
    }

  }, [currentMusic, musics])

  const togglePause = () => {
    setIsPause(!isPaused)
  }

  const toggleFavorite = useCallback(() => {
    if (isFavorite) {
      const currentFavorite = favorites.find((like) => {
        return like.music_id === currentMusic?.id
      });
      currentFavorite && removeFavorite(currentFavorite.id);
    } else {
      currentMusic && addFavorite(currentMusic.id)
    }
  }, [isFavorite, currentMusic, favorites, addFavorite, removeFavorite])

  const toggleTimeChange = useCallback((time: number) => {
    if (playerRef.current) {
      playerRef.current.currentTime = time;
    }
    setTimeElapsed(time);
  }, []);

  useEffect(() => {
    const firstMusic = musics.sort((a, b) => {
      return a.order - b.order
    }) as IMusic[];
    setCurrentMusic(firstMusic[0]);
  }, [musics])

  useEffect(() => {
    if (!user || isPaused || !currentMusic ||
        currentMusic.file === playerRef?.current?.src) {
      return;
    }
    addToast({
      title: album.name,
      description: currentMusic?.name,
      image: album.cover_image,
      type: 'music'
    });
  }, [currentMusic, album, addToast, user, isPaused])

  useEffect(() => {
    if (!currentMusic || !playerRef.current ||
      playerRef?.current?.src === currentMusic.file) {
      return;
    }
    const player = (playerRef.current as HTMLAudioElement);
    player.src = currentMusic.file;
  }, [currentMusic])

  useEffect(() => {
    const currentId = currentMusic?.id;
    const favoritesId = favorites?.map(({ music_id }) => music_id);
    if (currentId && favoritesId.length > 0) {
      setIsFavorite(favoritesId.includes(currentId));
    }
  }, [favorites, currentMusic])

  useEffect(() => {
    const player = (playerRef.current as HTMLAudioElement);
    if (isPaused && !player?.paused) {
      player?.pause()
    } else {
      player?.paused && player?.play().then(() => {
        setIsPause(false);
      }).catch((e) => {
        console.log(e);
      })
    }
  }, [isPaused, playerRef, currentMusic])

  useEffect(() => {
    const player = (playerRef.current as HTMLAudioElement);
    if (player !== null) {
      player.volume = volume
    }
  }, [playerRef, volume])

  useEffect(() => {
    if (!playerRef.current) {
      return;
    }
    playerRef.current.ontimeupdate = () => {
      setTimeElapsed(playerRef.current?.currentTime || 0);
    }
  }, [playerRef.current?.src])

  const renderPauseBtn = () => {
    return (
      <FaRegPauseCircle size={50} onClick={togglePause} />
    )
  }

  const renderPlayBtn = () => {
    return (
      <FaRegPlayCircle size={50} onClick={togglePause} />
    )
  }

  const renderContainer = () => {
    return !!user && currentMusic ? (
      <Container>
        <AlbumImage>
          <img src={album.cover_image} alt={album.name} />
        </AlbumImage>
        <AlbumInfo>
          <h5>{album.name}</h5> 
          <Favorite
            isFavorite={isFavorite}
            onClick={toggleFavorite}
          >
            {isFavorite ? <FaHeart /> : <FaRegHeart />}
          </Favorite>
          {currentMusic && <p>{currentMusic.name}</p>}
        </AlbumInfo>    

        <PlayerControls>
          <BackFowardBtn>
            <FaBackward  size={25} onClick={handlePreview} />
          </BackFowardBtn>

          <PlayBtn>
            {isPaused ? renderPlayBtn() : renderPauseBtn()}
          </PlayBtn>

          <FowardBtn>
            <FaForward size={25} onClick={handleNext} />
          </FowardBtn>

        </PlayerControls>

        <VolumeBar>
          <FaVolumeUp />
          <input
            type="range"
            min="0" max="1"
            step="0.1"
            value={volume}
            onChange={(e) => setVolume(Number(e.target.value))}
          />
        </VolumeBar>

        <TimerSlider>
          <input
            type="range"
            min="0" max={playerRef.current?.duration}
            value={timeElapsed}
            onChange={(e) => toggleTimeChange(Number(e.target.value))}
          />
        </TimerSlider>

        <audio ref={playerRef} onEnded={handleNext} />
      </ Container>
    ): null;
  }

  return renderContainer()
}

export default Player;
