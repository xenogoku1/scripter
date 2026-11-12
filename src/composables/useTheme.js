import { ref, onMounted } from 'vue'

const currentTheme = ref('default')

export function useTheme() {
  const setTheme = (themeName) => {
    currentTheme.value = themeName
    document.documentElement.setAttribute('data-theme', themeName)
    localStorage.setItem('scripter_theme', themeName)
  }

  onMounted(() => {
    const savedTheme = localStorage.getItem('scripter_theme') || 'default'
    setTheme(savedTheme)
  })

  return { currentTheme, setTheme }
}