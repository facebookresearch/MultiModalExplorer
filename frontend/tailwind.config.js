/** @type {import('tailwindcss').Config} */
// import DaisyUIPlugin from "daisyui/plugin";
import daisyui from "daisyui";

export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {},
  },
  plugins: [daisyui],
  daisyui: {
    themes: ["dark"],
  },
};
