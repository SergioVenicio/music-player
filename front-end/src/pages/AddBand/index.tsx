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

interface IGenre {
  id: number
  description: string
}
const AddBand: React.FC = () => {
  const { signOut } = useAuthContext();
  const { addToast } = useToastContext();

  const [name, setName] = useState('');
  const [genre, setGenre] = useState<IGenre>();
  const [availableGenres, setAvailableGenres] = useState<IGenre[]>([]);
  const [bandImage, setBandImage] = useState('');
  const [imageName, setImageName] = useState('');

  const refImage = useRef<HTMLInputElement>(null);

  const getGenre = useCallback(async (page: Number) => {
    try {
      const response = await api.get(`/api/v1/genre?page=${page}`);
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
    const fetchGenres = async () => {
      var page = 1;
      while (true) {
        const data = await getGenre(page);
        if (data?.results) {
          setAvailableGenres((genres) => [
            ...genres,
            ...data.results
          ])
        }

        if (data?.next == null) {
          break;
        }

        page++;
      }
    }
    fetchGenres()
  }, [getGenre]);

  const handleFileChange = useCallback((files: FileList | null) => {
    if (!files?.length) {
      return;
    }

    const fileName = files.item(0)?.name as string;
    const fileReader = new FileReader();
    fileReader.readAsDataURL(files[0]);
    fileReader.onload = () => {
      setBandImage(fileReader?.result as string);
      setImageName(fileName.split('.')[0]);
    }
  }, [])

  const handleSelectChange = useCallback((value: number) => {
    const choicedGenre = availableGenres.filter((genre) => {
      return genre.id === value ? genre: false
    })

    if (choicedGenre.length > 0) {
      setGenre(choicedGenre[0])
    }
  }, [availableGenres])

  const handleSubmit = useCallback(() => {
    api.post(
      '/api/v1/band',
      {
        name,
        genre_id: genre?.id,
        band_image: bandImage
      }
    ).then((response) => {
      addToast({
        title: 'New Band',
        description: 'Band saved',
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
        title: 'New Band',
        description: response.data.error || 'try again later!',
        type: 'error'
      })
    })
  }, [addToast, name, genre, bandImage, signOut])

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

        <Select
          onChange={(e) => handleSelectChange(Number(e.target.value))}
          validOptions={
            availableGenres.map(({id, description}) => ({id, value: description}))
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
            disabled={!(imageName && name && genre)}
            onClick={handleSubmit}
          >
            Save
          </Button>
        </ButtonWrapper>
      </Form>
    </Container>
  );
}

export default AddBand;
