import { Card, CardContent, CardHeader, Typography } from '@mui/material'
import React from 'react'

const ErrorInfo = ({ error }) => {
	return (
		<Card>
			<CardHeader title={`${error.status}`} />
			<CardContent>
				<Typography>{error.error}</Typography>
			</CardContent>
		</Card>
	)
}

export default ErrorInfo
