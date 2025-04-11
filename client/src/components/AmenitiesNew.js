import React, { useState, useEffect } from 'react'

function CreateAmenity(formData) {
  const myHeaders = new Headers()
  myHeaders.append("Content-Type", "application/json")
  fetch("/api/v1/amenities", { method: "POST", headers: myHeaders, body: JSON.stringify({ name: formData.name, description: formData.description }) })
  console.log(formData)
};

export default function AmenitiesNew() {

  return (
    <form action={CreateAmenity}>
      <label>Amenity name</label>
      <input name="name" />
      <label>Amenity description</label>
      <input name="description" />
      <button type="submit">Create Amenity</button>
    </form>
  )
}
