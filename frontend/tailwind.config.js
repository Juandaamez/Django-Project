/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        display: ['"Space Grotesk"', '"IBM Plex Sans"', 'system-ui', 'sans-serif'],
        sans: ['"IBM Plex Sans"', 'system-ui', 'sans-serif'],
      },
      colors: {
        brand: {
          primary: '#32d5ff',
          secondary: '#a855f7',
          accent: '#fcd34d',
        },
      },
      boxShadow: {
        glow: '0 25px 60px -15px rgba(50, 213, 255, 0.45)',
      },
    },
  },
  plugins: [],
}
