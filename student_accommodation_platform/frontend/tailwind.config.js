/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#172524",
        sand: "#f5f4ef",
        cream: "#fffdf7",
        coral: "#d8603d",
        moss: "#2f6b5d",
        line: "#d9dfd7",
        muted: "#667774",
      },
      fontFamily: {
        display: ["Space Grotesk", "sans-serif"],
        sans: ["DM Sans", "sans-serif"],
      },
    },
  },
  plugins: [],
};
