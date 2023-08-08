import React from 'react'
import { Card, CardHeader, CardContent, Typography } from '@mui/material'

function RepositoryInfo({ repo, dispersion }) {
	return (
		<Card>
			<CardHeader title="Repository's Info" />
			<CardContent>
				<Typography>Name: {repo.name}</Typography>
				<Typography>Description: {repo.description}</Typography>
				<Card>
					<CardContent>
						<Typography>Dispersion: </Typography>
						{Object.entries(dispersion).map(([key, value]) => (
							<Typography variant="body2">
								<strong>{key}:</strong> {value}
							</Typography>
						))}
					</CardContent>
				</Card>
			</CardContent>
		</Card>
	)
}

export default RepositoryInfo
