import React, { useState, useEffect } from 'react'

function register(formData) {
  const request = new Request("/api/v1/users", {
    headers: { "Content-Type": "application/json" },
    method: "post",
    body: `{ "first_name": "${formData.get('first_name')}", "last_name": "${formData.get('last_name')}", "email": "${formData.get('email')}", "password": "${formData.get('password')}"}`
  })
  fetch(request)
  console.log(formData)
};

export default function RegisterUser() {
  return (
    <form action={register}>
      <label>First Name</label>
      <input name="first_name" />
      <label>Last Name</label>
      <input name="last_name" />
      <label>Email</label>
      <input name="email" />
      <label>Password</label>
      <input name="password" type='password' />
      <button type="submit">login</button>
    </form>
  )
}
