import { Link } from "react-router-dom";
import { RatingStars } from "./RatingStars";
import { ScamWarningBanner } from "./ScamWarningBanner";
import { UtilityBadges } from "./UtilityBadges";

const money = (value) => `₦${Number(value).toLocaleString("en-NG")}`;

export function ListingCard({ listing, score }) {
  const photo = listing.images?.[0]?.image;
  return <article className="overflow-hidden border border-line bg-cream transition hover:-translate-y-1 hover:shadow-lg">
    <Link to={`/listings/${listing.id}`} className="block">
      <div className="relative h-44 bg-[linear-gradient(135deg,#b9c8ba,#e6c6ad)] bg-cover bg-center" style={photo ? { backgroundImage: `url(${photo})` } : undefined}>
        <span className="absolute bottom-3 left-3 bg-ink/90 px-2.5 py-1 text-xs text-white">{listing.distance_from_campus} km to campus</span>
      </div>
    </Link>
    <div className="space-y-3 p-4">
      {listing.scam_flag && <ScamWarningBanner />}
      <div className="flex items-start justify-between gap-3 text-xs text-muted"><span>{listing.rooms} room{listing.rooms === 1 ? "" : "s"}</span>{score !== undefined && <span className="font-bold text-moss">{Math.round(score * 100)}% match</span>}</div>
      <Link to={`/listings/${listing.id}`}><h3 className="font-display text-xl font-semibold leading-tight">{listing.title}</h3></Link>
      <p className="text-sm text-muted">{listing.address_text}</p>
      <div className="flex items-center justify-between"><strong className="font-display text-xl">{money(listing.price)} <small className="font-sans text-xs font-normal text-muted">/ month</small></strong><span className="text-sm"><RatingStars value={listing.avg_rating} /></span></div>
      <UtilityBadges listing={listing} />
    </div>
  </article>;
}
