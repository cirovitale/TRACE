import React from 'react'
import {
	Card,
	CardHeader,
	CardContent,
	List,
	ListItem,
	ListItemAvatar,
	Avatar,
	ListItemText,
} from '@mui/material'

function DeveloperList({ developers, onDeveloperClick }) {
	return (
		<Card className="developer-card">
			<CardHeader title="Developers List" />
			<CardContent>
				<List>
					{developers.map((developer) => (
						<ListItem
							button
							key={developer.login}
							onClick={() => onDeveloperClick(developer)}
						>
							<ListItemAvatar>
								<Avatar
									alt={`${developer.login}`}
									src={developer.avatar_url}
								/>
							</ListItemAvatar>
							<ListItemText
								primary={`${developer.login}` || 'N/A'}
								secondary={
									`Estimated Country: ${
										developer.nationality || 'N/A'
									}` || 'N/A'
								}
							/>
						</ListItem>
					))}
				</List>
			</CardContent>
		</Card>
	)
}

export default DeveloperList
