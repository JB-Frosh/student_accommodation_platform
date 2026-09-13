export function RatingStars({ value = 0 }) {
  return <span className="tracking-wide text-coral" aria-label={`${value} out of 5 stars`}>
    {[1, 2, 3, 4, 5].map((star) => <span key={star}>{star <= Math.round(value) ? "★" : "☆"}</span>)}
  </span>;
}
