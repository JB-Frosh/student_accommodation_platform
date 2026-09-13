import { useQuery } from "@tanstack/react-query";
import { MapView } from "../components/MapView";
import { listingApi } from "../services/api";

export function MapPage() {
  const query = useQuery({ queryKey: ["map-listings"], queryFn: () => listingApi.list({}) });
  const listings = query.data?.results || query.data || [];
  return <div className="space-y-7"><div><p className="mb-3 text-xs font-bold uppercase tracking-[.16em] text-coral">Explore the neighbourhood</p><h1 className="font-display text-5xl font-bold">Campus, in context.</h1><p className="mt-3 text-muted">The rings show one and two kilometres from the LASU Epe campus centre.</p></div><div className="overflow-hidden border border-line"><MapView listings={listings} /></div></div>;
}
