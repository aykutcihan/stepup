import { create } from 'zustand'

export type Language = 'en' | 'nl'

interface LanguageState {
  language: Language
  setLanguage: (language: Language) => void
}

const STORAGE_KEY = 'stepup-language'

function getInitialLanguage(): Language {
  const stored = localStorage.getItem(STORAGE_KEY)
  if (stored === 'en' || stored === 'nl') return stored
  return 'en'
}

export const useLanguageStore = create<LanguageState>((set) => ({
  language: getInitialLanguage(),
  setLanguage: (language) => {
    localStorage.setItem(STORAGE_KEY, language)
    set({ language })
  },
}))
