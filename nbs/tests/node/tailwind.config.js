
module.exports = {
  content: ["./extracted_classes.html"],
  plugins: [require('daisyui')],
  daisyui: {
    themes: [
      {
        "mytheme": {
          "primary": "#a2d7db",
          "secondary": "#fede80",
          "accent": "#f0938e",
          "neutral": "#d8d8d8",
          "base-100": "#ebebeb",
          "info": "#0ea5e9",
          "success": "#22c55e",
          "warning": "#eab308",
          "error": "#ef4444",
          "--rounded-box": "1rem",
          "--rounded-btn": "0.5rem",
          "--rounded-badge": "1.9rem",
          "--animation-btn": "0.25s",
          "--animation-input": "0.2s",
          "--btn-focus-scale": "0.95",
          "--border-btn": "1px",
          "--tab-border": "1px",
          "--tab-radius": "0.5rem",
        },
      },
      "light", "dark"
    ],
  },
}
