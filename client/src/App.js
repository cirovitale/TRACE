import './App.css'
import { useState, useEffect } from 'react'

function App() {
	const [data, setData] = useState()

	useEffect(() => {
		fetch('/test')
			.then((res) => res.json())
			.then((data) => {
				setData(data)
			})
	}, [])

	return (
		<div className="App">
			{data == undefined ? <p>Loading...</p> : <p>{data.name}</p>}
		</div>
	)
}

export default App
