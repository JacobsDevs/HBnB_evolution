import React, { useState, useEffect } from 'react'

export default function Amenities() {

  const [data, setData] = useState([{}])
  useEffect(() => {
    fetch("/api/v1/amenities"
    ).then(
      res => res.json()
    ).then(
      data => {
        setData(data)
        console.log(data)
      }
    )
  }, [])

  return (
    <div>
      {data.map((x, i) => (
        <p key={i}>{x.name}
          <br />
          {x.id}</p>
      ))
      }
    </div >
  )
}

