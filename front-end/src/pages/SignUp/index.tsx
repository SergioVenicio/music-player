import React, { useState, useCallback } from 'react';
import { FaUserPlus } from 'react-icons/fa';

import api from '../../services/api'

import { useHistory } from 'react-router-dom';
import useToastContext from '../../contexts/ToastContext';

import Logo from '../../components/Logo';
import Input from '../../components/Input';
import Button from '../../components/Button';

import { Container, Form, FormWrapper, FormHeader, FormButtons } from './styles'

const SignIn: React.FC = () =>{
  const history = useHistory();
  const { addToast } = useToastContext();

	const [email, setEmail] = useState<string>('');
  const [name, setName] = useState<string>('');
  const [lastName, setLastName] = useState<string>('');
	const [password, setPassword] = useState<string>('');
	const [pwdConfirm, setPwdConfirm] = useState<string>('');

  const disableForm = useCallback(() => {
    const pwdIsValid = !!(password.length > 6) && password === pwdConfirm;
    const userIsValid = !!(name.length > 0 && lastName.length > 0 && email.length > 0);

    return !(userIsValid && pwdIsValid);
  }, [password, pwdConfirm, name, lastName, email]);

  const handleSubmit = useCallback(async () => {
    const user = {
      name,
      last_name: lastName,
      email,
      password,
    }

    try {
      await api.post('/api/v1/user', {...user});
      history.push('signin');
      addToast({
        type: 'success',
        title: 'SignUp with success'
      });
    } catch ({ response }) {
      for (const [field, errors] of Object.entries(response.data)) {
        addToast({
          type: 'error',
          title: field,
          description: String(errors)
        })
      }
    }
  }, [name, lastName, email, password, addToast, history]);

	return (
		<Container>
			<FormWrapper>
				<FormHeader>
					<Logo />
				</FormHeader>
				<Form>
					<Input
						name="name"
						type="text"
						placeholder="Name"
						value={name}
            onChange={e => setName(e.target.value)}
					/>
          <hr/>
					<Input
						name="last_name"
						type="text"
            placeholder="Last name"
						value={lastName}
            onChange={e => setLastName(e.target.value)}
					/>
          <hr/>
					<Input
						name="email"
						type="email"
						placeholder="Email"
						value={email}
            onChange={e => setEmail(e.target.value)}
					/>
					<hr/>
					<Input
						name="password"
						type="Password"
						placeholder="password"
						value={password}
            onChange={e => setPassword(e.target.value)}
					/>
          <hr/>
					<Input
						name="password-confirmation"
						type="password"
						placeholder="Confirm your password"
						value={pwdConfirm}
            onChange={e => setPwdConfirm(e.target.value)}
					/>
				</Form>
				<FormButtons>
						<Button
              backgroundColor={'#4BBF73'}
              onClick={() => handleSubmit()}
              disabled={disableForm()}
						>
							<FaUserPlus />
						</Button>
				</FormButtons>
			</FormWrapper>
		</Container>
	)
}

export default SignIn;
