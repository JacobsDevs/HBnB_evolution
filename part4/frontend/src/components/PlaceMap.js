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

export default function PlaceMap(coord) {
  const position = { lat: coord['lat'], lng: coord['long'] }
  const [selectedPlace, setSelectedPlace] = useState(null);
  const [selectedCoord, setSelectedCoord] = useState(null)
  const [markerRef, marker] = useAdvancedMarkerRef();

  return (
    <APIProvider apiKey={process.env.REACT_APP_GOOGLE_KEY}>
      <div style={{ height: "500px" }}>
        <Map mapId={'69dd77c833e7557b'} defaultCenter={position} defaultZoom={15} disableDefaultUI={true}>
          <AdvancedMarker ref={markerRef} position={position} />
        </Map>
        <MapHandler place={selectedPlace} marker={marker} />
      </div>
    </APIProvider >
  );
};

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
