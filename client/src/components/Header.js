import { AppBar, Container, Toolbar, Typography } from '@mui/material'
import React from 'react'

function Header({ logo, name }) {
	return (
		<Container>
			<AppBar
				className="appBar"
				position="static"
				style={{ backgroundColor: '#671912' }}
			>
				<Toolbar className="toolbar">
					<img src={logo} className="logo" alt="logo" />
					<Typography variant="h3" className="text">
						{name}
					</Typography>
				</Toolbar>
			</AppBar>
		</Container>
	)
}

export default Header
