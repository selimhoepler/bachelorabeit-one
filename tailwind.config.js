/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["templates/*.html"],
    theme: {
      extend: {
        // fontSize: {
        //     'sm': '0.6rem',    // Kleine Textgröße
        //     'base': '0.7rem',      // Standard-Textgröße
        //     'lg': '1rem',    // Große Textgröße
        //     'xl': '1.1rem',     // Sehr große Textgröße
        //     // Füge weitere Größen nach Bedarf hinzu
        //   },


      },
    },
    plugins: [],
  }




  // tailwindcss -i styles\main.css -o static\css\style.css --watch