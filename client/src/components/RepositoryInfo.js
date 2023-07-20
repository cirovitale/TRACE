import React from 'react'
import { Card, CardHeader, CardContent, Typography } from '@mui/material'

function RepositoryInfo() {
	return (
		<Card>
			<CardHeader title="Repository's Info" />
			<CardContent>
				<Typography>Name: RepositoryXYZ</Typography>
				<Typography>Description: Descrizione del repository</Typography>
				<Typography>Contributors: 100</Typography>
			</CardContent>
		</Card>
	)
}

export default RepositoryInfo
