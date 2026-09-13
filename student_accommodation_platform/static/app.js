const campus = [6.5900, 3.9960];
const state = { listings: [], map: null, markers: [], sort: "-created_at" };

const api = async (path, options = {}) => {
  const response = await fetch(path, options);
  const body = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(body.detail || body.error || "Request failed");
  return body;
};

const money = (value) => `₦${Number(value).toLocaleString("en-NG")}`;
const imageUrl = (listing) => listing.images?.[0]?.image || "";

function setupMap() {
  if (!window.L) return;
  state.map = L.map("map", { scrollWheelZoom: false }).setView(campus, 14);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "© OpenStreetMap contributors",
  }).addTo(state.map);
  L.circle(campus, { radius: 300, color: "#d8603d", fillColor: "#d8603d", fillOpacity: 0.12 }).addTo(state.map)
    .bindTooltip("LASU Epe campus");
}

function updateMap(listings) {
  if (!state.map) return;
  state.markers.forEach((marker) => marker.remove());
  state.markers = listings.map((listing) => L.marker([listing.latitude, listing.longitude])
    .addTo(state.map)
    .bindPopup(`<strong>${listing.title}</strong><br>${money(listing.price)} / month`));
  if (listings.length) state.map.fitBounds(listings.map((listing) => [listing.latitude, listing.longitude]), { padding: [24, 24], maxZoom: 15 });
}

function renderListings(listings) {
  const grid = document.querySelector("#listing-grid");
  document.querySelector("#result-count").textContent = `${listings.length} home${listings.length === 1 ? "" : "s"}`;
  document.querySelector("#result-label").textContent = listings.length ? "Homes near LASU Epe" : "No homes match those filters";
  grid.innerHTML = listings.length ? listings.map((listing) => {
    const photo = imageUrl(listing);
    return `<article class="listing-card">
      <div class="listing-photo ${photo ? "has-image" : ""}" ${photo ? `style="background-image:url('${photo}')"` : ""}><span>${listing.distance_from_campus} km to campus</span></div>
      <div class="listing-body"><div class="listing-meta"><span>${listing.rooms} room${listing.rooms === 1 ? "" : "s"}</span><span>${listing.scam_flag ? "Review carefully" : "Checked listing"}</span></div>
      <h3>${listing.title}</h3><p class="address">${listing.address_text}</p><strong class="price">${money(listing.price)} <small>/ month</small></strong>
      <div class="amenities"><span>${listing.water_availability.replace("_", " ")}</span><span>${listing.electricity_availability}</span><span>${listing.internet_availability ? "Wi-Fi" : "No Wi-Fi"}</span></div></div>
    </article>`;
  }).join("") : `<div class="empty-state"><strong>Nothing here yet.</strong><p>Try widening your budget or distance from campus.</p></div>`;
  updateMap(listings);
}

async function loadListings() {
  const params = new URLSearchParams();
  const search = document.querySelector("#search").value.trim();
  const budget = document.querySelector("#price-max").value;
  const distance = document.querySelector("#distance-max").value;
  const water = document.querySelector("#water").value;
  const electricity = document.querySelector("#electricity").value;
  if (search) params.set("search", search);
  if (budget) params.set("price_max", budget);
  if (distance) params.set("distance_max", distance);
  if (water) params.set("water", water);
  if (electricity) params.set("electricity", electricity);
  if (document.querySelector("#internet").checked) params.set("internet", "true");
  params.set("ordering", state.sort);
  const data = await api(`/api/listings/?${params}`);
  state.listings = data.results || data;
  renderListings(state.listings);
}

function setupModes() {
  document.querySelectorAll(".mode-button").forEach((button) => button.addEventListener("click", () => {
    document.querySelectorAll(".mode-button").forEach((item) => item.classList.toggle("active", item === button));
    document.querySelector("#discover-view").classList.toggle("hidden", button.dataset.mode !== "discover");
    document.querySelector("#host-view").classList.toggle("hidden", button.dataset.mode !== "host");
    if (button.dataset.mode === "discover" && state.map) setTimeout(() => state.map.invalidateSize(), 50);
  }));
}

function setupLogin() {
  const dialog = document.querySelector("#login-dialog");
  document.querySelector("#login-button").addEventListener("click", () => dialog.showModal());
  document.querySelector("#login-form").addEventListener("submit", (event) => {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const token = btoa(`${form.get("username")}:${form.get("password")}`);
    sessionStorage.setItem("campusKeysAuth", `Basic ${token}`);
    dialog.close();
    document.querySelector("#login-button").textContent = "Signed in";
  });
}

async function publishListing(event) {
  event.preventDefault();
  const status = document.querySelector("#form-status");
  const form = new FormData(event.currentTarget);
  const auth = sessionStorage.getItem("campusKeysAuth");
  if (!auth) { status.textContent = "Sign in before publishing."; return; }
  const payload = Object.fromEntries(form.entries());
  payload.internet_availability = form.has("internet_availability");
  delete payload.images;
  try {
    const listing = await api("/api/listings/", { method: "POST", headers: { "Content-Type": "application/json", Authorization: auth }, body: JSON.stringify(payload) });
    const files = document.querySelector("#images").files;
    for (const image of files) {
      const upload = new FormData(); upload.append("listing_id", listing.id); upload.append("image", image);
      await api("/api/listing-images/", { method: "POST", headers: { Authorization: auth }, body: upload });
    }
    status.textContent = "Published. Students can now find this home.";
    event.currentTarget.reset();
    await loadListings();
  } catch (error) { status.textContent = error.message; }
}

document.addEventListener("DOMContentLoaded", () => {
  setupMap(); setupModes(); setupLogin();
  document.querySelector("#apply-filters").addEventListener("click", loadListings);
  document.querySelector("#reset-filters").addEventListener("click", () => { document.querySelector("#discover-view").querySelectorAll("input, select").forEach((item) => { if (item.type === "checkbox") item.checked = false; else item.value = ""; }); loadListings(); });
  document.querySelector("#sort-button").addEventListener("click", () => { state.sort = state.sort === "-created_at" ? "price" : "-created_at"; document.querySelector("#sort-button").firstChild.textContent = state.sort === "price" ? "Lowest price " : "Newest first "; loadListings(); });
  document.querySelector("#listing-form").addEventListener("submit", publishListing);
  loadListings().catch((error) => { document.querySelector("#listing-grid").innerHTML = `<div class="empty-state">${error.message}</div>`; });
});
