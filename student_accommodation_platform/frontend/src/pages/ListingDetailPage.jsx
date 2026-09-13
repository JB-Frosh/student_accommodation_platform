import { useQuery } from "@tanstack/react-query";
import { Link, useParams } from "react-router-dom";
import { RatingStars } from "../components/RatingStars";
import { ScamWarningBanner } from "../components/ScamWarningBanner";
import { UtilityBadges } from "../components/UtilityBadges";
import { listingApi } from "../services/api";

export function ListingDetailPage() {
  const { id } = useParams();
  const listingQuery = useQuery({ queryKey: ["listing", id], queryFn: () => listingApi.detail(id) });
  const reviewsQuery = useQuery({ queryKey: ["reviews", id], queryFn: () => listingApi.reviews(id) });
  if (listingQuery.isLoading) return <div className="h-96 animate-pulse bg-line/60" />;
  if (listingQuery.isError) return <div className="border border-[#e9b8a8] bg-[#fff1ec] p-5 text-[#86402f]">{listingQuery.error.message}</div>;
  const listing = listingQuery.data; const reviews = reviewsQuery.data?.results || reviewsQuery.data || [];
  return <div className="space-y-8"><Link to="/" className="text-sm text-muted">← Back to listings</Link>{listing.scam_flag && <ScamWarningBanner />}<div className="grid gap-8 lg:grid-cols-[1.35fr_1fr]"><div className="grid gap-3 sm:grid-cols-2">{(listing.images?.length ? listing.images : [{ id: "placeholder" }]).map((image, index) => <div key={image.id} className={`min-h-64 bg-[linear-gradient(135deg,#b9c8ba,#e6c6ad)] bg-cover bg-center ${index === 0 ? "sm:col-span-2" : ""}`} style={image.image ? { backgroundImage: `url(${image.image})` } : undefined} />)}</div><div className="space-y-5"><p className="text-xs font-bold uppercase tracking-[.16em] text-coral">{listing.distance_from_campus} km from LASU Epe</p><h1 className="font-display text-5xl font-bold leading-none">{listing.title}</h1><p className="text-muted">{listing.address_text}</p><strong className="block font-display text-3xl">₦{Number(listing.price).toLocaleString("en-NG")} <small className="font-sans text-sm font-normal text-muted">/ month</small></strong><UtilityBadges listing={listing} /><p className="leading-relaxed text-muted">{listing.description || "A student accommodation listing with practical details for life around LASU Epe campus."}</p><div className="border-y border-line py-4"><p className="text-sm font-bold">Landlord</p><p className="mt-1 text-muted">{listing.landlord?.name} · {listing.landlord?.verified ? "Verified landlord" : "Verification pending"}</p></div></div></div><section className="max-w-2xl space-y-5"><h2 className="font-display text-2xl font-bold">Reviews <RatingStars value={listing.avg_rating} /></h2>{reviewsQuery.isLoading && <p className="text-muted">Loading reviews…</p>}{reviews.map((review) => <article key={review.id} className="border-t border-line py-4"><div className="flex justify-between"><strong>{review.reviewer_name}</strong><RatingStars value={review.rating} /></div><p className="mt-2 text-muted">{review.comment}</p></article>)}{!reviews.length && !reviewsQuery.isLoading && <p className="text-muted">No reviews yet. Be the first student to share what living here is like.</p>}</section></div>;
}
