/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["templates/*.html"],

    darkMode: 'class',
    
    theme: {
      extend: {
        // fontSize: {
        //     'sm': '0.6rem',    // Kleine Textgröße
        //     'base': '0.7rem',      // Standard-Textgröße
        //     'lg': '1rem',    // Große Textgröße
        //     'xl': '1.1rem',     // Sehr große Textgröße
        //     // Füge weitere Größen nach Bedarf hinzu
        //   },


/*         fontFamily: {
          'sans': ['Inter', 'ui-sans-serif', 'system-ui', '-apple-system', 'system-ui', 'Segoe UI', 'Roboto', 'Helvetica Neue', 'Arial', 'Noto Sans', 'sans-serif', 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Color Emoji'],
          'body': ['Inter', 'ui-sans-serif', 'system-ui', '-apple-system', 'system-ui', 'Segoe UI', 'Roboto', 'Helvetica Neue', 'Arial', 'Noto Sans', 'sans-serif', 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Color Emoji'],
          'mono': ['ui-monospace', 'SFMono-Regular', 'Menlo', 'Monaco', 'Consolas', 'Liberation Mono', 'Courier New', 'monospace']
        }, */

      },
    },
    plugins: [],
  }




  // tailwindcss -i styles\main.css -o static\css\style.css --watch