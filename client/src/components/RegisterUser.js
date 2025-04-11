import { useNavigate } from 'react-router'


export default function RegisterUser() {
  // useNavigate() is used to navigate to a different page when the rest of the
  // function is complete. 
  // NOTE: anything with use* must be declared at the top of your function
  let navigate = useNavigate()

  async function register(formData) {
    // Build the request
    const request = new Request("/api/v1/users", {
      headers: { "Content-Type": "application/json" },
      method: "post",
      body: `{ "first_name": "${formData.get('first_name')}", "last_name": "${formData.get('last_name')}", "email": "${formData.get('email')}", "password": "${formData.get('password')}"}`
    })
    // Fetch the request
    const data = await fetch(request)
      .then(
        // Extract the json object from the response
        (response) => response.json()
      );
    if (data) {
      // navigate is what we declared at the top that lets us move the browser to a new page.
      navigate(`/users/${data.id}`)
    }
  };

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
