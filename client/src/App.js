import React from 'react'
import { Container } from '@mui/material'
import './App.css'
import Header from './components/Header'
import Body from './components/Body'

function App() {
	return (
		<Container>
			<Header logo="logo.png" name="" />
			<Body loader="img/loader.gif" />
		</Container>
	)
}

export default App
