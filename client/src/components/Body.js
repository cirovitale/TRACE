import React, { useState } from 'react'
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

function Body() {
	const [repositoryUrl, setRepositoryUrl] = useState('')
	const [developers, setDevelopers] = useState([])
	const [selectedDeveloper, setSelectedDeveloper] = useState(null)
	const [dialogOpen, setDialogOpen] = useState(false)
	const [error, setError] = useState(null)
	const [repo, setRepo] = useState({})
	// const [repoName, setRepoName] = useState()
	// const [repoOwner, setRepoOwner] = useState()

	const handleRepositorySubmit = () => {
		const repoOwner = 'carbon-language'
		const repoName = 'carbon-lang'
		setDevelopers([])
		setRepo({})

		fetch(`/repos/${repoOwner}/${repoName}`)
			.then((res) => res.json())
			.then((data) => {
				console.log(data)
				if (data.status == '403' || data.status == '404') {
					setError(data)
					return
				} else {
					setRepo(data)
					setError(undefined)
				}
				fetch(`/repos/${repoOwner}/${repoName}/contributors`)
					.then((res) => res.json())
					.then((data) => {
						console.log(data)
						if (data.status == '403') {
							console.log(data.status)
							setError(data)
							setDevelopers([])
						} else {
							setDevelopers(data)
							setError(undefined)
						}
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
		<Container>
			<Container maxWidth="sm" className="app-container">
				<div className="input-section">
					<TextField
						label="URL Repository GitHub"
						value={repositoryUrl}
						onChange={(e) => setRepositoryUrl(e.target.value)}
					/>
					<Button
						variant="contained"
						color="warning"
						onClick={handleRepositorySubmit}
					>
						Submit
					</Button>
				</div>

				{error && (
					<div className="error">
						<ErrorInfo error={error} />
					</div>
				)}

				{developers.length > 0 && (
					<div className="info-section">
						<RepositoryInfo repo={repo} />
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
		</Container>
	)
}

export default Body
