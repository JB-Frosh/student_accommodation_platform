import { useQuery } from "@tanstack/react-query";
import { useSearchParams } from "react-router-dom";
import { ListingCard } from "../components/ListingCard";
import { MapView } from "../components/MapView";
import { listingApi } from "../services/api";

const fields = [
  ["price_max", "Max monthly budget", "number", "e.g. 300000"],
  ["distance_max", "Max distance (km)", "number", "e.g. 3"],
  ["min_rating", "Minimum rating", "number", "e.g. 3"],
];

export function FeedPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const params = Object.fromEntries(searchParams.entries());
  const query = useQuery({ queryKey: ["listings", params], queryFn: () => listingApi.list(params) });
  const listings = query.data?.results || query.data || [];
  const update = (key, value) => { const next = new URLSearchParams(searchParams); value ? next.set(key, value) : next.delete(key); setSearchParams(next); };
  return <div className="space-y-10">
    <section className="flex flex-col justify-between gap-6 border-b border-line pb-10 lg:flex-row lg:items-end"><div><p className="mb-3 text-xs font-bold uppercase tracking-[.16em] text-coral">LASU Epe Campus · Lagos</p><h1 className="max-w-2xl font-display text-5xl font-bold leading-[.95] tracking-tight md:text-7xl">A better place to<br /><em className="text-coral">come home to.</em></h1><p className="mt-5 max-w-lg text-muted">Compare real accommodation around campus by price, distance, facilities, and the details that shape student life.</p></div><div className="text-sm text-muted"><span className="mr-2 inline-block h-2 w-2 rounded-full bg-coral" />Campus centre<br /><strong className="text-ink">6.5900° N, 3.9960° E</strong></div></section>
    <section className="grid gap-8 lg:grid-cols-[250px_1fr]">
      <aside className="h-fit space-y-5 border border-line bg-cream p-5"><div className="flex items-center justify-between"><strong>Search homes</strong><span className="text-xs text-muted">{listings.length} found</span></div><input value={params.search || ""} onChange={(event) => update("search", event.target.value)} placeholder="Area, title, landmark" className="w-full border-b border-ink bg-transparent px-0 py-3 outline-none placeholder:text-muted" />
        {fields.map(([key, label, type, placeholder]) => <label key={key} className="grid gap-2 text-xs text-muted">{label}<input type={type} value={params[key] || ""} placeholder={placeholder} onChange={(event) => update(key, event.target.value)} className="border border-line bg-white p-2.5 text-sm text-ink outline-none focus:border-coral" /></label>)}
        <label className="grid gap-2 text-xs text-muted">Water<select value={params.water || ""} onChange={(event) => update("water", event.target.value)} className="border border-line bg-white p-2.5 text-sm text-ink"><option value="">Any water</option><option value="borehole">Borehole</option><option value="pipe_borne">Pipe-borne</option><option value="well">Well</option></select></label>
        <label className="grid gap-2 text-xs text-muted">Electricity<select value={params.electricity || ""} onChange={(event) => update("electricity", event.target.value)} className="border border-line bg-white p-2.5 text-sm text-ink"><option value="">Any power</option><option value="24hr">24 hours</option><option value="rationed">Rationed</option><option value="none">None</option></select></label>
        <label className="flex items-center gap-2 text-sm"><input type="checkbox" checked={params.internet === "true"} onChange={(event) => update("internet", event.target.checked ? "true" : "")} /> Internet available</label><button onClick={() => setSearchParams({})} className="text-left text-xs text-muted underline">Clear filters</button>
      </aside>
      <div className="space-y-5"><div className="h-64 overflow-hidden border border-line"><MapView listings={listings} compact /></div>{query.isLoading && <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">{[1, 2, 3].map((item) => <div key={item} className="h-80 animate-pulse bg-line/60" />)}</div>}{query.isError && <div className="border border-[#e9b8a8] bg-[#fff1ec] p-5 text-[#86402f]">{query.error.message}</div>}{!query.isLoading && !query.isError && <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">{listings.map((listing) => <ListingCard key={listing.id} listing={listing} />)}{!listings.length && <div className="border border-line bg-cream p-8 text-muted">No homes match those filters. Try widening your budget or campus radius.</div>}</div>}</div>
    </section>
  </div>;
}
