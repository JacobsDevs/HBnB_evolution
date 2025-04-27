import React from "react";
import "./PlaceCard.css"
import { IoInformationCircleOutline } from "react-icons/io5";
import { useNavigate } from "react-router-dom";

export default function PlaceCard (props) {
  const title = props.title;
  const description = props.description;
  const price = props.price;
  const id = props.id;
  const navigate = useNavigate();

    return (
    <>
    <section className="card">
      <div className="card_blur"></div>

      <div className="card_container container">
        <article className="card_description">
          <img src="/HouseImage.jpg" alt="House" className="card_img"/>
          <div className="card_shadow"></div>
          <h2 className="card_title">{title}</h2>

          <div className="card_clip">
            <IoInformationCircleOutline size={20} />
          </div>

          <div className="info_data">
            <h2 className="info_title">{title}</h2>
            <p className="info_description">{description}</p>
            <h3 className="info_price">${price}</h3>
            <button className="info_button" onClick={() => navigate(`/places/${id}`)}>Details</button>
          </div>
        </article>
      </div>
    </section>
    </>
    )
}



//           <div className="place-stats">
//             {/* Calculate and display average rating */}
//             <span className="stat">
//               <i className="fas fa-star"></i>
//               {place.reviews?.length > 0
//                 ? (place.reviews.reduce((sum, r) => sum + r.rating, 0) / place.reviews.length).toFixed(1)
//                 : 'No ratings'}
//             </span>
//             <span className="stat">
//               <i className="fas fa-comment"></i>
//               {place.reviews?.length || 0} reviews
//             </span>
//           </div>