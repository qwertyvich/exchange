# Где менять название и изображения

Файлы из `frontend/public` доступны в браузере без префикса `public`. Например `frontend/public/img/TRY.svg` → `/img/TRY.svg`. Имена и регистр важны: Linux различает `TRY.svg` и `try.svg`.

| Что | Файл изображения | Где используется |
|---|---|---|
| Название Casper Exchange, толщина шрифта и размеры логотипа всех режимов | Текст и стили в `frontend/src/components/BrandLogo.vue` | Все `Header0/1/2.vue`, включая мобильное меню |
| Тело призрака | `frontend/public/brand/casper-ghost.webp` | `CasperFigure.vue`, `BrandLogo.vue`, `CasperMascot.vue` |
| Отдельные солнцезащитные очки | `frontend/public/brand/casper-sunglasses.svg` | `CasperFigure.vue` |
| Коричневый чемодан в правой руке персонажа (слева для зрителя) | `frontend/public/brand/casper-suitcase.svg` | `CasperFigure.vue` |
| Фон главной и области за шапкой | `frontend/public/_next/static/media/bg.png` (и прочие `bg*.png`) | `frontend/src/App.vue`, изображение с классом `appBackground` |
| Значок вкладки | `frontend/public/brand/casper-favicon.svg` | `frontend/index.html`, `rel="icon"` |
| Призрак во время первой загрузки | Те же файлы `brand/casper-*` | `CasperFigure.vue` и `.casperLoader` в `App.vue` |
| Иконки криптовалют/банков | `frontend/public/img/bit.svg`, `ether.svg`, `tether_*.svg`, `sber.svg`, `sbp.svg` и др. | Массивы валют в `HomePage0/1/2.vue`; история — `ProfilePage.vue`; заявка — `TicketPage.vue` |
| Флаги/иностранные валюты | `frontend/public/img/TRY.svg`, `THB.svg`, `AED.svg` и др. | `HomePage2.vue`: путь строится по `deposit_wallets[id].symbol`; также история и заявка |
| Лента банков | `frontend/public/img/banks/` | `HomePage2.vue`, `hero-marquee` |
| Картинки инструкции | `frontend/public/img/inst-1.png` … `inst-4.png` | `frontend/src/pages/GuidePage.vue`, массив `steps` |
| Иконки мессенджеров | `frontend/public/img/telega.svg`, `whats.svg` | `GuidePage.vue` и страницы контактов |
| Запасная картинка | `frontend/public/img/placeholder.svg` | При отсутствии валютной иконки |

Логотип общий: изменение `BrandLogo.vue` и `CasperFigure.vue` сразу применяется ко всем трём режимам и мобильному меню. Шапки используют один класс `siteBrandBar glassNavigationSurface`; цвет стекла задаётся в `frontend/src/styles/glass-motion.css`. Старые растровые логотипы Palma сохранены в `_next/static/media`, но шапки их больше не загружают.

Цикл призрака задаётся в `frontend/src/lib/casperTimeline.js`: 10 с левитации, 1,5 с выхода влево, 2 с отсутствия, 0,7 с появления в точке 1, 4 с выглядывания, 0,5 с ухода, 2 с отсутствия, 0,7 с появления в точке 2, 7 с выглядывания, 1,5 с ухода, 4 с отсутствия и 1 с возвращения к логотипу. Всего 34,9 с. Координаты зависят от положения заголовка и поля «Получаете» и обновляются при прокрутке и изменении размера окна. Очки и чемодан остаются в логотипе, пока тело летает. В мобильном меню отображается полный статичный логотип, цикл приостановлен; при системном уменьшении движения используется статичная версия.

Исходник PNG, способ подготовки и точный запрос генерации: [design/casper/ASSET.md](../design/casper/ASSET.md). В браузер отправляется оптимизированная WebP-версия 384×384, около 19 КБ.

Название вкладки браузера и поисковый заголовок находятся в `frontend/index.html` в `<title>`. Тексты на страницах ищите в `frontend/src/pages` и `frontend/src/components`. Поиск всех упоминаний старого имени:

```sh
rg -n 'Casper|Exchange' frontend/src frontend/index.html
rg -n 'casper-|appBackground|/img/' frontend/src
```

Сайт здесь — Vue/Vite. Папка `_next` содержит сохранённые статические материалы старой вёрстки; отдельного Next.js-сервера нет и он не нужен.

После замены картинки в dev-режиме обновите страницу. В статической сборке пересоберите frontend:

```sh
docker compose -f docker-compose.prod.yml up -d --build frontend
```

Если браузер держит старую картинку, обновите страницу с очисткой кэша либо поменяйте имя файла/версию query string. Публичные изображения кэшируются на час, собранные JS/CSS имеют хеш в имени. Не подменяйте настоящие изображения файлами `Zone.Identifier`: это ненужные метаданные Windows, а не картинки.
