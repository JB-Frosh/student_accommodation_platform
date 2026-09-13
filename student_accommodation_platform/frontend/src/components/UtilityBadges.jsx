const labels = {
  electricity: { "24hr": "24h power", rationed: "Rationed power", none: "No power" },
  water: { pipe_borne: "Pipe-borne", borehole: "Borehole", well: "Well", none: "No water" },
};

export function UtilityBadges({ listing }) {
  return <div className="flex flex-wrap gap-2 text-xs text-muted">
    <span className="rounded-full bg-sand px-2.5 py-1">⚡ {labels.electricity[listing.electricity_availability] || listing.electricity_availability}</span>
    <span className="rounded-full bg-sand px-2.5 py-1">◌ {labels.water[listing.water_availability] || listing.water_availability}</span>
    {listing.internet_availability && <span className="rounded-full bg-sand px-2.5 py-1">Wi-Fi</span>}
  </div>;
}
