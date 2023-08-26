import React, { useState } from 'react'
import {
	TextField,
	Button,
	Container,
	AppBar,
	Toolbar,
	Typography,
} from '@mui/material'
import './App.css'
import DeveloperList from './components/DeveloperList'
import RepositoryInfo from './components/RepositoryInfo'
import DeveloperDialog from './components/DeveloperDialog'
import ErrorInfo from './components/ErrorInfo'
import Header from './components/Header'
import Body from './components/Body'

function App() {
	return (
		<Container>
			<Header logo="logo.jpg" name="TRACE" />
			<Body />
		</Container>
	)
}

export default App
