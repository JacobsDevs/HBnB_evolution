import React from "react";
import "./PlaceCard.css"
import { IoInformationCircleOutline } from "react-icons/io5";

export default function PlaceCard ({title, description, price, amenities, onClick}) {

    return (
    <>
    <section className="card">
      <div className="card_blur"></div>

      <div className="card_container container">
        <article className="card_description">
          <img src="/HouseImage.jpg" alt="House" className="card_img"/>
          <div className="card_shadow"></div>
          <h2 className="card_title">SAKURA{title}</h2>

          <div className="card_clip">
            <IoInformationCircleOutline size={20} />
          </div>

          <div className="info_data">
            <h2 className="info_title">SAKURA{title}</h2>
            <p className="info_description">Bautifull House near the beach, in the middle of the city, with astonishing views over the mountains.{description}</p>
            <h3 className="info_price">$600{price}</h3>
            <button className="info_button">Book</button>
          </div>
        </article>
      </div>
    </section>
    </>
    )
}