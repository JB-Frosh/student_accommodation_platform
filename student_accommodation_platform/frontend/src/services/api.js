const api = async (path, options = {}) => {
  const response = await fetch(path, options);
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data.detail || data.error || "We could not load that right now.");
  return data;
};

export const listingApi = {
  list: (params) => api(`/api/listings/?${new URLSearchParams(params)}`),
  detail: (id) => api(`/api/listings/${id}/`),
  reviews: (id) => api(`/api/reviews/?listing=${id}`),
  recommendation: (params) => api(`/api/intelligence/recommendations/?${new URLSearchParams(params)}`),
  predictionStatus: () => api("/api/intelligence/prediction/"),
};

export const landlordApi = {
  detail: (id) => api(`/api/landlords/${id}/`),
  listings: (id) => api(`/api/listings/?search=${encodeURIComponent(id)}`),
};
