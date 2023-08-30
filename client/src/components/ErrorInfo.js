import { Alert, Card } from '@mui/material'
import React from 'react'

const ErrorInfo = ({ error }) => {
	return (
		<Card>
			<Alert sx={{ p: 2 }} severity="error">
				ERROR CODE: {error.status}
				<br />
				{error.error}
			</Alert>
		</Card>
	)
}

export default ErrorInfo
