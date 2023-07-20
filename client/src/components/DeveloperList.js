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
							key={developer.id}
							onClick={() => onDeveloperClick(developer)}
						>
							<ListItemAvatar>
								<Avatar
									alt={`${developer.name} ${developer.surname}`}
									src={developer.avatarUrl}
								/>
							</ListItemAvatar>
							<ListItemText
								primary={`${developer.name} ${developer.surname}`}
								secondary={`Estimated Country: ${developer.nationality}`}
							/>
						</ListItem>
					))}
				</List>
			</CardContent>
		</Card>
	)
}

export default DeveloperList
