import React, { useState, useEffect } from 'react';
import { useHistory, useParams } from 'react-router-dom';

import api from '../../services/api';

import useAuthContext from '../../contexts/AuthContext';
import useToastContext from '../../contexts/ToastContext';

import Card from '../../components/Card';

import { Container, CardContainer } from './styles';

interface IBand {
	id: number;
	name: string;
	band_image: string;
}

interface IUrlParams {
	genre_id: string;
}

const Bands: React.FC = () => {
	const [bands, setBands] = useState<IBand[]>();
	const { genre_id } = useParams<IUrlParams>();

	const { signOut } = useAuthContext();
	const { addToast } = useToastContext();
	const history = useHistory();

	const navigateToAlbumPage = (band_id: number) => {
		history.push(`/albums/${band_id}`);
	}

	useEffect(() => {
		api.get(
			'/api/v1/band', {params: { genre_id }}
		).then(({ data }) => {
			setBands(() => {
				return data.results.map((band: IBand) => {
					return { ...band }
				}) as IBand[]
			});
		}).catch((error) => {
			if (error?.response?.status === 401) {
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
		});
	}, [genre_id, signOut, addToast]);

	const showCards = () => {
		return bands && bands.map(band => {
			return (
				<CardContainer
					key={band.id}
					onClick={() => navigateToAlbumPage(band.id)}
				>
					<Card
						description={band.name}
						image={band.band_image}
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

export default Bands;
