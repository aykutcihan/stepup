import { useLanguageStore } from '@/stores/languageStore'
import { translations } from '@/i18n/translations'

export function useTranslation() {
  const language = useLanguageStore((state) => state.language)
  return translations[language]
}
