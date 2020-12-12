import React, {
  useCallback,
  useEffect,
  useState,
  useRef
} from 'react';

import useAuthContext from '../../contexts/AuthContext';
import useToastContext from '../../contexts/ToastContext';

import Input from '../../components/Input';
import Select from '../../components/Select';
import Button from '../../components/Button';

import api from '../../services/api'

import { 
  Container,
  Form,
  FileWrapper,
  ButtonWrapper
} from './styles'

interface MusicOrder {
  order: number
}
interface IAlbum {
  id: number
  name: string
}
const AddMusic: React.FC = () => {
  const { signOut } = useAuthContext();
  const { addToast } = useToastContext();

  const [name, setName] = useState('');
  const [order, setOrder] = useState(1);
  const [album, setAlbum] = useState<IAlbum>();
  const [availableAlbums, setAvailableAlbums] = useState<IAlbum[]>([]);
  const [musicFile, setMusicFile] = useState('');
  const [fileName, setFileName] = useState('');

  const refFile = useRef<HTMLInputElement>(null);

  const getAlbums = useCallback(async (page: Number) => {
    try {
      const response = await api.get(`/api/v1/album?page=${page}`);
      return response.data;
    } catch ({ response }) {
      if (response.status === 401) {
        signOut();
				addToast({
					title: 'Session Expired',
					type: 'error'
				});
        return;
      }
    }
  }, [signOut, addToast])

  useEffect(() => {
    const fetchBands = async () => {
      var page = 1;
      while (true) {
        const data = await getAlbums(page);
        if (data?.results) {
          setAvailableAlbums((albums) => [
            ...albums,
            ...data.results
          ])
        }

        if (data?.next == null) {
          break;
        }

        page++;
      }
    }
    fetchBands()
  }, [getAlbums]);

  useEffect(() => {
    if (!album) {
      return;
    }

    api.get(`/api/v1/music?album_id=${album?.id}`).then(({data}) => {
      if (!data.results) {
        return;
      }
      const orders = data.results.map(({order}: MusicOrder) => order)
      const lastOrder = Math.max(...orders);
      setOrder(lastOrder + 1);
    }).catch(({response}) => {
      if (response.status === 401) {
        signOut();
				addToast({
					title: 'Session Expired',
					type: 'error'
				});
        return;
      }
    }) 
  }, [album, signOut, addToast])

  const handleFileChange = useCallback((files: FileList | null) => {
    if (!files?.length) {
      return;
    }

    const fileName = files.item(0)?.name as string;
    const fileReader = new FileReader();
    fileReader.readAsDataURL(files[0]);
    fileReader.onload = () => {
      setMusicFile(fileReader?.result as string);
      setFileName(fileName.split('.')[0]);
    }
  }, [])

  const handleSelectChange = useCallback((value: number) => {
    const choicedAlbum = availableAlbums.filter((album) => {
      return album.id === value ? album: false
    })

    if (choicedAlbum.length > 0) {
      setAlbum(choicedAlbum[0])
    }
  }, [availableAlbums])

  const handleSubmit = useCallback(() => {
    api.post(
      '/api/v1/music',
      {
        name,
        album_id: album?.id,
        order: order,
        file: musicFile
      }
    ).then((response) => {
      setOrder((order) => order + 1)
      addToast({
        title: 'New Music',
        description: 'Music Saved',
        type: 'success'
      })
    }).catch(({ response }) => {
      if (response.status === 401) {
        signOut();
        return;
      }
      addToast({
        title: 'New Music',
        description: response.data.error || 'try again later!',
        type: 'error'
      })
    })
  }, [addToast, name, musicFile, order, album, signOut])

  return (
    <Container>
      <Form>
        <Input
          name='name'
          type='text'
          placeholder='Name'
          value={name}
          onChange={(e) => setName(e.target.value)}
        />

        <hr />

        <Input
          name='order'
          type='text'
          placeholder='Order'
          value={String(order)}
          onChange={(e) => setOrder(Number(e.target.value))}
        />

        <hr />

        <Select
          onChange={(e) => handleSelectChange(Number(e.target.value))}
          validOptions={
            availableAlbums.map(({id, name}) => ({id, value: name}))
          } />

        <hr />

        <ButtonWrapper>
          <Button
            type='button'
            color='#fefefe'
            onClick={(e) =>{refFile?.current?.click()}}
          >
            { fileName ? fileName: 'Choice a music file' }
          </Button>
        </ButtonWrapper>

        <FileWrapper>
          <Input
            name='file'
            type='file'
            placeholder='Music File'
            onChange={(e) => handleFileChange(e.target.files)}
            inputRef={refFile}
          />
        </FileWrapper>

        <ButtonWrapper>
          <Button
            type={'button'}
            backgroundColor={'#00d692'}
            color={'#f7f7f7'}
            disabled={!(fileName && name && album)}
            onClick={handleSubmit}
          >
            Save
          </Button>
        </ButtonWrapper>
      </Form>
    </Container>
  );
}

export default AddMusic;
