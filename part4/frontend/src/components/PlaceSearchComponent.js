import useScript from '../hooks/useScript'
import { useState, useEffect, useRef, createRef } from 'react'
import {
  APIProvider,
  ControlPosition,
  MapControl,
  Map,
  AdvancedMarker,
  Pin,
  InfoWindow,
  useMap,
  useMapsLibrary,
  useAdvancedMarkerRef
} from '@vis.gl/react-google-maps'

export default function PlaceSearch(props) {
  const position = { lat: -25.27, lng: 133.77 }
  const [selectedPlace, setSelectedPlace] = useState(null);
  const [selectedCoord, setSelectedCoord] = useState(null)
  const [markerRef, marker] = useAdvancedMarkerRef();

  return (
    <APIProvider apiKey={process.env.REACT_APP_GOOGLE_KEY}>
      <div style={{ height: "500px" }}>
        <Map mapId={'69dd77c833e7557b'} defaultCenter={position} defaultZoom={4.2} disableDefaultUI={true}>
          <AdvancedMarker ref={markerRef} position={null} />
        </Map>
        <MapControl position={ControlPosition.TOP}>
          <div>
            <PlaceAutocomplete onPlaceSelect={setSelectedPlace} />
          </div>
        </MapControl>
        <MapHandler place={selectedPlace} marker={marker} />
        <Coorder marker={marker} props={props} />
      </div>
    </APIProvider >
  );
};

const Coorder = ({ marker, props }) => {
  const [coords, setCoords] = useState(null)

  const getLocation = e => {
    e.preventDefault()
    if (!marker) return;

    let coord = [marker.position.uC, marker.position.vC]
    props.data.latitude = coord[0]
    props.data.longitude = coord[1]
    document.getElementById(props['latId']).value = Number(coord[0])
    document.getElementById(props['longId']).value = Number(coord[1])
    const event = new Event('input', { bubbles: true })
    document.getElementById(props['latId']).dispatchEvent(event)
    document.getElementById(props['longId']).dispatchEvent(event)
  }
  return (
    <button onClick={getLocation}>Hi There</button>
  )
}

const MapHandler = ({ place, marker }) => {
  const map = useMap();

  useEffect(() => {
    if (!map || !place || !marker) return;

    if (place.geometry?.viewport) {
      map.fitBounds(place.geometry?.viewport);
    }

    marker.position = place.geometry?.location;
  }, [map, place, marker]);
  return null;
};

const PlaceAutocomplete = ({ onPlaceSelect }) => {
  const [placeAutocomplete, setPlaceAutocomplete] = useState(null);
  const inputRef = useRef(null);
  const places = useMapsLibrary('places');

  useEffect(() => {
    if (!places || !inputRef.current) return;

    const options = {
      fields: ['geometry', 'name', 'formatted_address'],
    };

    setPlaceAutocomplete(new places.Autocomplete(inputRef.current, options));
  }, [places]);
  useEffect(() => {
    if (!placeAutocomplete) return;

    placeAutocomplete.addListener('place_changed', () => {
      onPlaceSelect(placeAutocomplete.getPlace());
    });
  }, [onPlaceSelect, placeAutocomplete]);
  return (
    <div className="autocomplete-containter">
      <input ref={inputRef} />
    </div>
  );
};
