import React, { useState } from 'react';
import { FaRegPaperPlane, FaUserPlus } from 'react-icons/fa';

import useAuthContext from "../../contexts/AuthContext";

import Logo from '../../components/Logo';
import Input from '../../components/Input';
import Button from '../../components/Button';

import { Container, Form, FormWrapper, FormHeader, FormButtons } from './styles'

const SignIn: React.FC = () =>{
    const { signIn } = useAuthContext();
    const [email, setEmail] = useState<string>('');
    const [password, setPassword] = useState<string>('');

    const handleSign = async () => {
        await signIn({
            email: email as string,
            password: password as string,
        });
    }

    const handleEmailChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setEmail(e.target.value);
    }

    const handlePasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setPassword(e.target.value);
    }

    return (
        <Container>
            <FormWrapper>
                <FormHeader>
                    <Logo />
                </FormHeader>
                <Form>
                    <Input
                        name="email"
                        type="email"
                        placeholder="email"
                        value={email}
                        onChange={handleEmailChange}
                    />
                    <hr/>
                    <Input
                        name="password"
                        type="password"
                        placeholder="password"
                        value={password}
                        onChange={handlePasswordChange}
                    />
                </Form>
                <FormButtons>
                    <Button
                        onClick={handleSign}
                    >
                        <FaRegPaperPlane />
                    </Button>
                    <Button
                        backgroundColor={'#4BBF73'}
                    >
                        <FaUserPlus />
                    </Button>
                </FormButtons>
            </FormWrapper>
        </Container>
    )
}

export default SignIn;
