import Quasar from 'quasar'
import { LocalStorage } from 'quasar'

export default async () => {
  const defaultLang = 'zh-hans'
  let langIso = LocalStorage.getItem('lang')

  if (!LocalStorage.has('lang') || !langIso || langIso === 'en-US') {
    LocalStorage.set('lang', defaultLang)
    langIso = defaultLang
  }

  try {
    await import(
      /* webpackInclude: /(zh-hans|en-US)\.js$/ */
      `quasar/lang/${langIso}`
      )
      .then(lang => {
        Quasar.lang.set(lang.default)
      })
  }
  catch (err) {
    // Requested Quasar Language Pack does not exist,
    // let's not break the app, so catching error
  }
}
