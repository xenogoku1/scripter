import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'

// Applies saved theme from localStorage on app load
const savedTheme = localStorage.getItem('scripter_theme') || 'default'
document.documentElement.setAttribute('data-theme', savedTheme)

const app = createApp(App)
app.use(router)

app.mount('#app')
