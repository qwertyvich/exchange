# Где менять название и изображения

Файлы из `frontend/public` доступны в браузере без префикса `public`. Например `frontend/public/img/TRY.svg` → `/img/TRY.svg`. Имена и регистр важны: Linux различает `TRY.svg` и `try.svg`.

| Что | Файл изображения | Где используется |
|---|---|---|
| Логотип режима 0 | `frontend/public/_next/static/media/logo-name.webp` | `frontend/src/components/Header0.vue` |
| Логотип режима 1 | `frontend/public/_next/static/media/logo-name.webp` | `frontend/src/components/Header1.vue` |
| Логотип режима 2 | `frontend/public/_next/static/media/logo-name.webp` | `frontend/src/components/Header2.vue` |
| Логотип в меню мобильной версии | Те же файлы | В каждом `Header0/1/2.vue` есть второй `<img>` внутри панели |
| Фон главной и области за шапкой | `frontend/public/_next/static/media/bg.png` (и прочие `bg*.png`) | `frontend/src/App.vue`, изображение с классом `appBackground` |
| Значок вкладки | `frontend/public/img/icon.png` | `frontend/index.html`, `rel="icon"` |
| Анимация первой загрузки | `frontend/public/img/loading.gif` | `frontend/src/App.vue` |
| Иконки криптовалют/банков | `frontend/public/img/bit.svg`, `ether.svg`, `tether_*.svg`, `sber.svg`, `sbp.svg` и др. | Массивы валют в `HomePage0/1/2.vue`; история — `ProfilePage.vue`; заявка — `TicketPage.vue` |
| Флаги/иностранные валюты | `frontend/public/img/TRY.svg`, `THB.svg`, `AED.svg` и др. | `HomePage2.vue`: путь строится по `deposit_wallets[id].symbol`; также история и заявка |
| Лента банков | `frontend/public/img/banks/` | `HomePage2.vue`, `hero-marquee` |
| Картинки инструкции | `frontend/public/img/inst-1.png` … `inst-4.png` | `frontend/src/pages/GuidePage.vue`, массив `steps` |
| Иконки мессенджеров | `frontend/public/img/telega.svg`, `whats.svg` | `GuidePage.vue` и страницы контактов |
| Запасная картинка | `frontend/public/img/placeholder.svg` | При отсутствии валютной иконки |

Проще всего заменить содержимое файла, сохранив имя. Для нового имени измените соответствующий `src`/`icon`; при смене логотипа проверьте оба вхождения в нужной шапке. Сейчас все три режима используют один `logo-name.webp`. Рядом лежат запасные `logo-name1.webp` и `logo-name2.webp`; чтобы использовать их, измените `src` в соответствующей шапке.

Название вкладки браузера и поисковый заголовок находятся в `frontend/index.html` в `<title>`. Тексты на страницах ищите в `frontend/src/pages` и `frontend/src/components`. Поиск всех упоминаний старого имени:

```sh
rg -n 'Palma|palma|Exchange' frontend/src frontend/index.html
rg -n 'logo-name|appBackground|/img/' frontend/src
```

Сайт здесь — Vue/Vite. Папка `_next` содержит сохранённые статические материалы старой вёрстки; отдельного Next.js-сервера нет и он не нужен.

После замены картинки в dev-режиме обновите страницу. В статической сборке пересоберите frontend:

```sh
docker compose -f docker-compose.prod.yml up -d --build frontend
```

Если браузер держит старую картинку, обновите страницу с очисткой кэша либо поменяйте имя файла/версию query string. Публичные изображения кэшируются на час, собранные JS/CSS имеют хеш в имени. Не подменяйте настоящие изображения файлами `Zone.Identifier`: это ненужные метаданные Windows, а не картинки.
