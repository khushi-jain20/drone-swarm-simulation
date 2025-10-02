
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      animation: {
        'spin-slow': 'spin 20s linear infinite',
      },
      fontFamily: {
        'orbitron': ['"Orbitron"', 'sans-serif'],
        'mono': ['ui-monospace', 'SFMono-Regular']
      }
    },
  },
  plugins: [],
}