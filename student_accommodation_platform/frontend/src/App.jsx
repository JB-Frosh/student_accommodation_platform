import { Link, NavLink, Route, Routes } from "react-router-dom";
import { FeedPage } from "./pages/FeedPage";
import { ListingDetailPage } from "./pages/ListingDetailPage";
import { RecommendationPage } from "./pages/RecommendationPage";
import { MapPage } from "./pages/MapPage";

function Header() {
  return <header className="sticky top-0 z-10 border-b border-line bg-cream/95 backdrop-blur">
    <div className="mx-auto flex max-w-7xl items-center justify-between px-5 py-4 lg:px-8">
      <Link to="/" className="flex items-center gap-2 font-bold"><span className="grid h-8 w-8 place-items-center rounded-full bg-coral font-display text-sm text-white">ck</span>Campus Keys</Link>
      <nav className="hidden items-center gap-7 text-sm text-muted md:flex"><NavLink to="/" className={({ isActive }) => isActive ? "font-bold text-ink" : ""}>Find a place</NavLink><NavLink to="/recommendations" className={({ isActive }) => isActive ? "font-bold text-ink" : ""}>Best for you</NavLink><NavLink to="/map" className={({ isActive }) => isActive ? "font-bold text-ink" : ""}>Map view</NavLink></nav>
      <button className="border border-ink px-3 py-2 text-sm">Sign in</button>
    </div>
  </header>;
}

export function App() {
  return <><Header /><main className="mx-auto max-w-7xl px-5 py-8 lg:px-8 lg:py-12"><Routes><Route path="/" element={<FeedPage />} /><Route path="/listings/:id" element={<ListingDetailPage />} /><Route path="/recommendations" element={<RecommendationPage />} /><Route path="/map" element={<MapPage />} /></Routes></main></>;
}
