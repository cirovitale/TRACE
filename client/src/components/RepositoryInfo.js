import React from 'react'
import { Card, CardHeader, CardContent, Typography } from '@mui/material'

function RepositoryInfo({ repo }) {
	return (
		<Card>
			<CardHeader title="Repository's Info" />
			<CardContent>
				<Typography>Name: {repo.name}</Typography>
				<Typography>Description: {repo.description}</Typography>
			</CardContent>
		</Card>
	)
}

export default RepositoryInfo
