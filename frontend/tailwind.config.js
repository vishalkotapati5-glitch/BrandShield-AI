/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        navy: { 900: "#0b1230", 800: "#111b45", 700: "#1a2760" },
        violet: { 500: "#7c5cff", 600: "#6a47f0" },
      },
    },
  },
  plugins: [],
};
