import React, { useEffect, useState } from 'react'
import {
	Card,
	CardHeader,
	CardContent,
	Typography,
	Grid,
	Alert,
} from '@mui/material'
import { Chart } from 'react-google-charts'
import moment from 'moment'

function RepositoryInfo({ repo, dispersion, chartData, alert, readme }) {
	const [chartOption, setChartOption] = useState({})

	useEffect(() => {
		setChartOption({ title: 'Distribution of Developers' })

		// const data = [
		// 	['Country', 'Count'],
		// 	...Object.entries(dispersion.countryDisp),
		// ]
		// setChartData(data)
	}, [])

	return (
		<Card>
			<CardHeader title="Repository Info" />
			<CardContent>
				<Typography>
					Name:{' '}
					<a href={repo.html_url} target="_blank">
						{' '}
						{repo.full_name || repo.name || 'N/A'}{' '}
					</a>
				</Typography>
				<Typography>
					Description: {repo.description || 'N/A'}
				</Typography>
				<Typography>
					README:{' '}
					<a
						href={(readme && readme.html_url) || '#'}
						target="_blank"
					>
						{readme.name || 'N/A'}
					</a>{' '}
				</Typography>
				<Typography>
					Stars: {repo.stargazers_count || 'N/A'}{' '}
				</Typography>
				<Typography>
					License: {(repo.license && repo.license.name) || 'N/A'}{' '}
				</Typography>
				<Typography>
					Latest Update:{' '}
					{moment(repo.updated_at).format('YYYY-MM-DD HH:mm:ss') ||
						'N/A'}{' '}
				</Typography>
				<Typography>
					WebSite:{' '}
					{(repo.homepage && (
						<a href={repo.homepage} target="_blank">
							{repo.homepage}
						</a>
					)) ||
						'N/A'}{' '}
				</Typography>
				<Card sx={{ mt: 4 }}>
					<CardContent>
						{alert && (
							<Alert severity="warning">
								Attention! The number of failed predictions
								(with result "N/A") is greater than 30% of the
								total contributors, the result may contain
								noise.
							</Alert>
						)}
						<Typography sx={{ mt: 3 }}>
							Shannon Index: {dispersion?.shannonIndex.toFixed(2)}
						</Typography>
						<Typography>
							Percent Dispersion:{' '}
							{dispersion?.percentCultDisp.toFixed(2)} %
						</Typography>
						{chartData && (
							<Chart
								chartType="PieChart"
								data={chartData}
								options={chartOption}
								width={'100%'}
								height={'300px'}
							/>
						)}
						<Typography>Country Counter: </Typography>
						<Grid container spacing={2}>
							{Object.entries(dispersion.countryDisp)
								.sort((x, y) => y[1] - x[1])
								.map(([key, value], index) => (
									<Grid item xs={4} key={index}>
										<Typography variant="body2">
											<strong>{key}:</strong> {value}
										</Typography>
									</Grid>
								))}
						</Grid>
					</CardContent>
				</Card>
			</CardContent>
		</Card>
	)
}

export default RepositoryInfo
