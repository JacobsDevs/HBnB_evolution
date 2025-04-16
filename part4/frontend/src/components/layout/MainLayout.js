import Header from "./Header";
import Footer from "./Footer";
import { Outlet } from "react-router";
import "../../App.css"

export default function MainLayout() {
  return (
    <div className="App">
      <Header />
      <main className="main-content">
        <Outlet />
      </main>
      <Footer />
    </div>
  )
}
