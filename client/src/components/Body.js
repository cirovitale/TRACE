import React, { useEffect, useState, CSSProperties } from 'react'
import {
	TextField,
	Button,
	Container,
	AppBar,
	Toolbar,
	Typography,
} from '@mui/material'
import '../App.css'
import DeveloperList from './DeveloperList'
import RepositoryInfo from './RepositoryInfo'
import DeveloperDialog from './DeveloperDialog'
import ErrorInfo from './ErrorInfo'
import HashLoader from 'react-spinners/HashLoader'
// BeatLoader ClimbingBoxLoader ClockLoader GridLoader HashLoader PulseLoader RingLoader ScaleLoader

function Body() {
	const [repositoryUrl, setRepositoryUrl] = useState('')
	const [developers, setDevelopers] = useState([])
	const [selectedDeveloper, setSelectedDeveloper] = useState(null)
	const [dialogOpen, setDialogOpen] = useState(false)
	const [error, setError] = useState(undefined)
	const [repo, setRepo] = useState({})
	const [dispersion, setDispersion] = useState({})
	const [shannonIndex, setShannonIndex] = useState(0)
	const [chartData, setChartData] = useState({})
	const [processing, setProcessing] = useState(false)
	const [alert, setAlert] = useState(false)
	const [readme, setReadme] = useState(false)
	// const [repoName, setRepoName] = useState()
	// const [repoOwner, setRepoOwner] = useState()

	useEffect(() => {
		setDevelopers([])
		setError(undefined)
		setAlert(false)
		setProcessing(false)
		setRepo({})
	}, [])

	const override = {
		margin: '0 auto',
		// marginTop: '100',
		// color: '#ed6c02',
	}

	const isValidGitHubRepoFormat = (url) => {
		// Input Format:   <<  OWNER/NAME  >>
		const pattern = /^[^\/]+\/[^\/]+$/
		return pattern.test(url)
	}

	const handleRepositorySubmit = () => {
		setProcessing(true)
		setDevelopers([])
		setRepo({})
		setError(undefined)

		if (!isValidGitHubRepoFormat(repositoryUrl)) {
			setError({
				error: 'Invalid GitHub Repository format. Expected format: OWNER/NAME.',
				status: '442',
			})
			setProcessing(false)
			return
		}

		// Extract repo owner and name from URL
		const [repoOwner, repoName] = repositoryUrl.split('/')

		// Test GitHub Repos
		// const repoOwner = 'cirovitale'
		// const repoName = 'Zyphyk-Sport'
		// const repoOwner = 'Hikki00'
		// const repoName = 'Raptor-AI'
		// const repoOwner = 'cheshire-cat-ai'
		// const repoName = 'core'
		// const repoOwner = 'carbon-language'
		// const repoName = 'carbon-lang'

		// Test PDF
		// const repoOwner = 'carsonRadtke'
		// const repoName = 'carsonRadtke'

		// Test Google Docs
		// const repoOwner = 'prabhatexit0'
		// const repoName = 'astrofolio'

		setDevelopers([])
		setRepo({})

		fetch(`/repos/${repoOwner}/${repoName}`)
			.then((res) => res.json())
			.then((data) => {
				console.log(data)
				if (data.status == '403' || data.status == '404') {
					setError(data)
					setProcessing(false)
					return
				} else {
					setRepo(data)
					setError(undefined)
				}
				fetch(`/repos/${repoOwner}/${repoName}/readme`)
					.then((res) => res.json())
					.then((data) => {
						console.log(data)
						if (data.status == '403') {
							console.log(data.status)
							setError(data)
							setProcessing(false)
							return
						} else {
							setReadme(data)
							console.log('************** ' + data)
							console.log()
						}
					})
					.catch((e) => {})
				fetch(`/repos/${repoOwner}/${repoName}/contributors`)
					.then((res) => res.json())
					.then((data) => {
						console.log(data)
						if (data.status == '403') {
							console.log(data.status)
							setError(data)
							setDevelopers([])
							setProcessing(false)
							return
						} else {
							setAlert(data.alert)
							console.log(data.alert)
							setDevelopers(data.contributors)
							setDispersion(data.culturalDispersion)
							const chartData = [
								['Country', 'Count'],
								...Object.entries(
									data?.culturalDispersion.countryDisp || {}
								).sort((x, y) => y[1] - x[1]),
							]

							setChartData(chartData)
							setError(undefined)
						}
						setProcessing(false)
					})
					.catch((e) => {})
			})
			.catch((e) => {})
	}

	const handleDeveloperClick = (developer) => {
		setSelectedDeveloper(developer)
		setDialogOpen(true)
	}

	const handleDialogClose = () => {
		setDialogOpen(false)
	}

	return (
		<Container maxWidth="sm" className="app-container">
			<div className="input-section">
				<Typography sx={{ mb: 2 }}>
					Enter OWNER/NAME of the repo to analyze:
				</Typography>
				<TextField
					label="OWNER/NAME"
					value={repositoryUrl}
					onChange={(e) => setRepositoryUrl(e.target.value)}
					error={!!error}
					helperText={error?.error}
				/>
				<Button
					disabled={processing}
					variant="contained"
					color="warning"
					onClick={handleRepositorySubmit}
				>
					Submit
				</Button>
			</div>
			<div style={{ marginTop: 50 }}>
				<HashLoader
					color="#ed6c02"
					loading={processing}
					cssOverride={override}
					size={150}
					aria-label="Loading Spinner"
					data-testid="loader"
				/>
			</div>

			{error && (
				<div className="error">
					<ErrorInfo error={error} />
				</div>
			)}

			{developers && developers.length > 0 && (
				<div className="info-section">
					<RepositoryInfo
						repo={repo}
						dispersion={dispersion}
						chartData={chartData}
						alert={alert}
						readme={readme}
					/>
					<DeveloperList
						developers={developers}
						onDeveloperClick={handleDeveloperClick}
					/>
				</div>
			)}

			<DeveloperDialog
				open={dialogOpen}
				developer={selectedDeveloper}
				onClose={handleDialogClose}
			/>
		</Container>
	)
}

export default Body
