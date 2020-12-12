import React, {useCallback, useState, useRef} from 'react';

import useAuthContext from '../../contexts/AuthContext';
import useToastContext from '../../contexts/ToastContext';

import Input from '../../components/Input';
import Button from '../../components/Button';

import api from '../../services/api'

import { 
  Container,
  Form,
  FileWrapper,
  ButtonWrapper
} from './styles'

const AddAlbum: React.FC = () => {
  const { signOut } = useAuthContext();
  const { addToast } = useToastContext();

  const [description, setDescription] = useState('');
  const [genreImage, setGenreImage] = useState('');
  const [imageName, setImageName] = useState('');

  const refImage = useRef<HTMLInputElement>(null);

  const handleFileChange = useCallback((files: FileList | null) => {
    if (!files?.length) {
      return;
    }

    const fileName = files.item(0)?.name as string;
    const fileReader = new FileReader();
    fileReader.readAsDataURL(files[0]);
    fileReader.onload = () => {
      setGenreImage(fileReader?.result as string);
      setImageName(fileName.split('.')[0]);
    }
  }, [])

  const handleSubmit = useCallback(() => {
    api.post(
      '/api/v1/genre',
      {
        description,
        genre_image: genreImage
      }
    ).then((response) => {
      addToast({
        title: 'New Genre',
        description: 'Genre saved',
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
        title: 'New Genre',
        description: response.data.error || 'try again later!',
        type: 'error'
      })
    })
  }, [addToast, description, genreImage, signOut])

  return (
    <Container>
      <Form>
        <Input
          name='description'
          type='text'
          placeholder='Description'
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />

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
            disabled={!(imageName && description)}
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
