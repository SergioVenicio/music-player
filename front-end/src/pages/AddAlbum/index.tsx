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

interface IBand {
  id: number
  name: string
}
const AddAlbum: React.FC = () => {
  const { signOut } = useAuthContext();
  const { addToast } = useToastContext();

  const [name, setName] = useState('');
  const [releaseDate, setReleaseDate] = useState('');
  const [band, setBand] = useState<IBand>();
  const [availableBands, setAvailableBands] = useState<IBand[]>([]);
  const [coverImage, setCoverImage] = useState('');
  const [imageName, setImageName] = useState('');

  const refImage = useRef<HTMLInputElement>(null);

  const getBands = useCallback(async (page: Number) => {
    try {
      const response = await api.get(`/api/v1/band?page=${page}`);
      return response.data;
    } catch ({response}) {
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
        const data = await getBands(page);
        if (data?.results) {
          setAvailableBands((bands) => [
            ...bands,
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
  }, [getBands]);

  const handleFileChange = useCallback((files: FileList | null) => {
    if (!files?.length) {
      return;
    }

    const fileName = files.item(0)?.name as string;
    const fileReader = new FileReader();
    fileReader.readAsDataURL(files[0]);
    fileReader.onload = () => {
      setCoverImage(fileReader?.result as string);
      setImageName(fileName.split('.')[0]);
    }
  }, [])

  const handleSelectChange = useCallback((value: number) => {
    const choicedBand = availableBands.filter((band) => {
      return band.id === value ? band: false
    })

    if (choicedBand.length > 0) {
      setBand(choicedBand[0])
    }
  }, [availableBands])

  const handleSubmit = useCallback(() => {
    api.post(
      '/api/v1/album',
      {
        name,
        band_id: band?.id,
        release_date: releaseDate,
        cover_image: coverImage
      }
    ).then((response) => {
      addToast({
        title: 'New Album',
        description: 'Album Saved',
        type: 'success'
      })
    }).catch(({ response }) => {
      if (response.status === 401) {
        signOut();
        addToast({
          title: 'Session Expired',
          type: 'error'
        });
        return;
      }
      addToast({
        title: 'New Album',
        description: response.data.error || 'try again later!',
        type: 'error'
      })
    })
  }, [addToast, name, band, coverImage, releaseDate, signOut])

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
          name='release_date'
          type='text'
          placeholder='Release Date'
          value={releaseDate}
          onChange={(e) => setReleaseDate(e.target.value)}
        />

        <hr />

        <Select
          onChange={(e) => handleSelectChange(Number(e.target.value))}
          validOptions={
            availableBands.map(({id, name}) => ({id, value: name}))
          } />

        <hr />

        <ButtonWrapper>
          <Button
            type='button'
            color='#fefefe'
            onClick={(e) =>{refImage?.current?.click()}}
          >
            { imageName ? imageName: 'Choice a image' }
          </Button>
        </ButtonWrapper>

        <FileWrapper>
          <Input
            name='genre_image'
            type='file'
            placeholder='Genre Image'
            onChange={(e) => handleFileChange(e.target.files)}
            inputRef={refImage}
          />
        </FileWrapper>

        <ButtonWrapper>
          <Button
            type={'button'}
            backgroundColor={'#00d692'}
            color={'#f7f7f7'}
            disabled={!(imageName && name && releaseDate && band)}
            onClick={handleSubmit}
          >
            Save
          </Button>
        </ButtonWrapper>
      </Form>
    </Container>
  );
}

export default AddAlbum;
