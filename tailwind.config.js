/** @type {import('tailwindcss').Config} */
// tailwind.config.js
module.exports = {
  content: [
    // project-level templates
    './templates/**/*.html',
    // app-specific templates
    './blog/templates/**/*.html',
    // any JS you write that contains Tailwind classes
    './static/js/**/*.js',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}


