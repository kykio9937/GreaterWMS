import Vue from 'vue'
import VueI18n from 'vue-i18n'
import messages from 'src/i18n'
import { LocalStorage } from 'quasar'

Vue.use(VueI18n)

const defaultLang = 'zh-hans'
let lang = LocalStorage.getItem('lang')

if (!LocalStorage.has('lang') || !lang || lang === 'en-US') {
  LocalStorage.set('lang', defaultLang)
  lang = defaultLang
}

const i18n = new VueI18n({
  locale: lang,
  fallbackLocale: defaultLang,
  messages
})

export default ({ app }) => {
  app.i18n = i18n
}

export { i18n }
