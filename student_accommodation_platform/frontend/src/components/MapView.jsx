import { Circle, MapContainer, Marker, Popup, TileLayer } from "react-leaflet";
import { Link } from "react-router-dom";
import "leaflet/dist/leaflet.css";

const campus = [6.59, 3.996];

export function MapView({ listings = [], compact = false }) {
  return <MapContainer center={campus} zoom={14} scrollWheelZoom={!compact} className={compact ? "h-72 w-full" : "h-[460px] w-full"}>
    <TileLayer attribution='© OpenStreetMap contributors' url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
    {[1, 2].map((radius) => <Circle key={radius} center={campus} radius={radius * 1000} pathOptions={{ color: radius === 1 ? "#d8603d" : "#2f6b5d", fillOpacity: 0.04 }} />)}
    <Circle center={campus} radius={80} pathOptions={{ color: "#172524", fillColor: "#d8603d", fillOpacity: 0.8 }} />
    {listings.map((listing) => <Marker key={listing.id} position={[listing.latitude, listing.longitude]}>
      <Popup><strong>{listing.title}</strong><br />₦{Number(listing.price).toLocaleString("en-NG")} / month<br /><Link to={`/listings/${listing.id}`}>View listing</Link></Popup>
    </Marker>)}
  </MapContainer>;
}
