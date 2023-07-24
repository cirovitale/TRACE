import React from 'react'
import {
	Dialog,
	DialogTitle,
	DialogContent,
	Typography,
	Avatar,
	Grid,
	Card,
	CardContent,
	Container,
} from '@mui/material'

function DeveloperDialog({ open, developer, onClose }) {
	return (
		<Dialog
			open={open}
			onClose={onClose}
			fullWidth
			maxWidth="sm"
			scroll="body"
		>
			{developer && (
				<Card>
					<DialogTitle variant="h3">
						<b>{`${developer.login}`}</b>
					</DialogTitle>
					<DialogContent>
						<Card className="dev-predict-result">
							<CardContent className="card-predict-result">
								<Container>
									<p>1</p>
									<p>1</p>
									<p>1</p>
								</Container>
							</CardContent>
						</Card>
						<Card className="dev-predict-result">
							<CardContent>
								<Grid container spacing={2}>
									<Grid item xs={12} sm={8}>
										<Typography variant="h5">
											Info Utente
										</Typography>
										<hr />
										<Typography variant="h6">
											ID: {developer.id}
										</Typography>
										<Typography variant="h6">
											Name: {developer.name || 'N/A'}
										</Typography>
										<Typography variant="h6">
											Email: {developer.email || 'N/A'}
										</Typography>
										<Typography variant="h6">
											Location:{' '}
											{developer.location || 'N/A'}
										</Typography>
										<Typography variant="h6">
											Bio: {developer.bio || 'N/A'}
										</Typography>
										<Typography variant="h6">
											Twitter:{' '}
											{developer.twitter_username ||
												'N/A'}
										</Typography>
										<Typography variant="h6">
											Company:{' '}
											{developer.company || 'N/A'}
										</Typography>
										<Typography variant="h6">
											Blog: {developer.blog || 'N/A'}
										</Typography>
										<Typography variant="h6">
											URL: {developer.html_url}
										</Typography>
										<Typography variant="h6">
											Twitter:{' '}
											{developer.twitter_username ||
												'N/A'}
										</Typography>
										<Typography variant="h6">
											Followers: {developer.followers}
										</Typography>
										<Typography variant="h6">
											Following: {developer.following}
										</Typography>
									</Grid>
									<Grid item xs={12} sm={4}>
										<Avatar
											alt={`${developer.login}`}
											src={developer.avatar_url}
											style={{
												width: '100%',
												height: 'auto',
											}}
										/>
									</Grid>
								</Grid>
							</CardContent>
						</Card>
						<br />
						<br />
						<Card>
							<CardContent>
								<Typography variant="h5">Info Prev</Typography>
								<hr />
								<Typography variant="h6">
									Modulo NAME-COUNTRY: N/A
								</Typography>
								<Typography variant="h6">
									Modulo CV-COUNTRY:{' '}
									{(developer.pdfs &&
										developer.pdfs.map((pdf) => (
											<Typography variant="h6">
												{pdf}
											</Typography>
										))) ||
										'N/A'}
								</Typography>
								<Typography variant="h6">
									Modulo COMMIT-COUNTRY: N/A
								</Typography>
								<Typography variant="h6">
									Location: {developer.location || 'N/A'}
								</Typography>
							</CardContent>
						</Card>
					</DialogContent>
				</Card>
			)}
		</Dialog>
	)
}

export default DeveloperDialog
