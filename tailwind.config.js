/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',  // Look for Tailwind classes in your HTML templates
    './django_horizons/templates/**/*.html',  // Look for Tailwind classes in your HTML templates
    './home/templates/**/*.html',             // Include templates in the home app
    './blog/templates/**/*.html',             // Include templates in the blog app
    './static/js/**/*.js', 
    './static/js/**/*.js',
       // Optionally include JavaScript files if needed
  ],
  theme: {
    extend: {},
  },
  plugins: ['daisyui'],
}

