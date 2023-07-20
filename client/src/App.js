import React, { useState } from 'react'
import { TextField, Button, Container } from '@mui/material'
import './App.css'
import DeveloperList from './components/DeveloperList'
import RepositoryInfo from './components/RepositoryInfo'
import DeveloperDialog from './components/DeveloperDialog'

function App() {
	const [repositoryUrl, setRepositoryUrl] = useState('')
	const [developers, setDevelopers] = useState([])
	const [selectedDeveloper, setSelectedDeveloper] = useState(null)
	const [dialogOpen, setDialogOpen] = useState(false)

	const handleRepositorySubmit = () => {
		fetch('/repoUsers')
			.then((res) => res.json())
			.then((data) => {
				console.log(data)
				setDevelopers(data)
			})
			.catch()
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
				<TextField
					label="URL Repository GitHub"
					value={repositoryUrl}
					onChange={(e) => setRepositoryUrl(e.target.value)}
				/>
				<Button variant="contained" onClick={handleRepositorySubmit}>
					Invia
				</Button>
			</div>

			{developers.length > 0 && (
				<div className="info-section">
					<RepositoryInfo />
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

export default App
