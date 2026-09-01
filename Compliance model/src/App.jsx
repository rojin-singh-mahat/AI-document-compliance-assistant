import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [data, setData] = useState(null)

  useEffect(() => {
    async function fetchData() {
      const response = await fetch("http://localhost:8000")

      if (response.ok) {
        const result = await response.json()
        setData(result)
      }
    }

    fetchData()
  }, [])

  return (
    <>
      {data && <p>{data.message}</p>}
    </>
  )
}

export default App