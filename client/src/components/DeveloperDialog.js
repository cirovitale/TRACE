import React from 'react'
import { Dialog, DialogTitle, DialogContent, Typography } from '@mui/material'

function DeveloperDialog({ open, developer, onClose }) {
	return (
		<Dialog open={open} onClose={onClose}>
			{developer && (
				<>
					<DialogTitle>{`${developer.name} ${developer.surname}`}</DialogTitle>
					<DialogContent>
						<Typography>ID: {developer.id}</Typography>
						<Typography>
							Country: {developer.nationality}
						</Typography>
					</DialogContent>
				</>
			)}
		</Dialog>
	)
}

export default DeveloperDialog
