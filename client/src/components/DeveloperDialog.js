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
} from '@mui/material'
import Tooltip from '@mui/material/Tooltip'
import IconButton from '@mui/material/IconButton'
import InfoIcon from '@mui/icons-material/Info'
import ReactCountryFlag from 'react-country-flag'

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
								<Grid container spacing={2}>
									<Grid item xs={12} sm={12}>
										<Typography variant="h5">
											Estimated Country
										</Typography>
										<hr />
										<Typography variant="h6">
											{(developer.prediction
												.estimatedCountry && (
												<ReactCountryFlag
													className="emojiFlag"
													countryCode={
														developer.prediction
															.estimatedCountry
													}
													style={{
														fontSize: '5em',
													}}
													title="IT"
													svg
												/>
											)) ||
												'N/A'}
										</Typography>
									</Grid>
								</Grid>
							</CardContent>
						</Card>
						<Card className="dev-predict-result">
							<CardContent>
								<Grid container spacing={2}>
									<Grid item xs={12} sm={8}>
										<Typography variant="h5">
											User Info
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
											Blog:{' '}
											{(developer.blog &&
												developer.blog != '' && (
													<a
														href={developer.blog}
														target="_blank"
													>
														{' '}
														{developer.blog}
													</a>
												)) ||
												'N/A'}
										</Typography>
										<Typography variant="h6">
											URL:{' '}
											<a
												href={developer.html_url}
												target="_blank"
											>
												{developer.html_url}
											</a>
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
						<Card>
							<CardContent>
								<Typography variant="h5">
									Prediction Details from Modules
								</Typography>
								<hr />
								<Typography variant="h6">
									USERNAME-COUNTRY
									<Tooltip
										title={
											(developer.prediction.username &&
												developer.prediction.username.isoPredicted.toUpperCase() !=
													'NULL' &&
												developer.prediction.username
													.isoPredicted != '' &&
												developer.prediction.username
													.reasons) ||
											'N/A'
										}
									>
										<IconButton>
											<InfoIcon />
										</IconButton>
									</Tooltip>
									:{' '}
									{(developer.prediction.username &&
										developer.prediction.username.isoPredicted.toUpperCase() !=
											'NULL' &&
										developer.prediction.username
											.isoPredicted != '' &&
										developer.prediction.username
											.isoPredicted) ||
										'N/A'}
								</Typography>
								<Typography variant="h6">
									NAME-COUNTRY:{' '}
									{(developer.prediction.name &&
										developer.prediction.name.toUpperCase() !=
											'NULL' &&
										developer.prediction.name != '' &&
										developer.prediction.name) ||
										'N/A'}
								</Typography>
								<Typography variant="h6">
									CV-COUNTRY
									{(developer.prediction.pdfs != null &&
										developer.prediction.pdfs.length != 0 &&
										developer.prediction.pdfs.map((pdf) => (
											<>
												<Tooltip
													title={
														<>
															<a
																href={pdf.url}
																target="_blank"
															>
																{pdf.url}
															</a>{' '}
															{
																JSON.parse(
																	pdf.isoPredicted
																).reasons
															}
														</>
													}
												>
													<IconButton>
														<InfoIcon />
													</IconButton>
												</Tooltip>
												:{' '}
												{(JSON.parse(
													pdf.isoPredicted
												).isoPredicted.toUpperCase() !=
													'NULL' &&
													JSON.parse(pdf.isoPredicted)
														.isoPredicted) ||
													'N/A'}
											</>
										))) ||
										': N/A'}
								</Typography>
								<Typography variant="h6">
									COMMIT-COUNTRY
									<Tooltip
										title={
											(developer.prediction.commits &&
												developer.prediction.commits
													.commits &&
												developer.prediction.commits.commits.map(
													(commit, count) =>
														'*** << COMMIT ' +
														(parseInt(count) + 1) +
														': ' +
														commit.commit.commit
															.message +
														'>> {language detected: ' +
														commit.isoDetected +
														'} ***'
												)) ||
											'N/A'
										}
									>
										<IconButton>
											<InfoIcon />
										</IconButton>
									</Tooltip>
									:{' '}
									{(developer.prediction.commits &&
										developer.prediction.commits
											.isoDetected) ||
										'N/A'}
								</Typography>
								<Typography variant="h6">
									LOCATION-COUNTRY
									<Tooltip
										title={developer.location || 'N/A'}
									>
										<IconButton>
											<InfoIcon />
										</IconButton>
									</Tooltip>
									:{' '}
									{(developer.prediction.location &&
										developer.prediction.location) ||
										'N/A'}
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
