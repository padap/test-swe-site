# SWE-MERA Leaderboard

## Новая версия (без Svelte, один HTML файл)

### Как запустить локально?

**Вариант 1: Простой HTTP-сервер (Python)**
```bash
cd demo-swe-mera
python3 -m http.server 8000
```
Откройте [http://localhost:8000/index-new.html](http://localhost:8000/index-new.html)

**Вариант 2: Простой HTTP-сервер (Node.js)**
```bash
cd demo-swe-mera
npx http-server -p 8000
```
Откройте [http://localhost:8000/index-new.html](http://localhost:8000/index-new.html)

**Вариант 3: Live Server (VS Code расширение)**
1. Установите расширение "Live Server" в VS Code
2. Откройте `index-new.html` в VS Code
3. Нажмите "Go Live" в статус-баре

### Преимущества новой версии

✅ **Один файл** — весь код в одном `index-new.html`  
✅ **Без зависимостей** — нет npm, нет Svelte, нет сборки  
✅ **Vanilla JavaScript** — простой, понятный код  
✅ **Быстрая загрузка** — никаких внешних библиотек  
✅ **Простая поддержка** — легко править и понимать  

### Структура нового файла

```
index-new.html
├── <style>      — все CSS стили встроены
├── <body>       — HTML структура
│   ├── Header   — шапка с навигацией
│   ├── Intro    — главная секция с логотипом
│   └── Main     — контент (описание + лидерборд)
└── <script>     — весь JavaScript код
    ├── I18N     — переключение языков (eng/ru)
    ├── Routing  — hash-based роутинг (#/, #/leaderboard)
    ├── Data     — загрузка и обработка JSON данных
    ├── Slider   — dual range слайдер для фильтра дат
    └── Table    — рендеринг таблицы лидерборда
```

### Функциональность

- ✅ Главная страница с описанием
- ✅ Страница лидерборда с таблицей
- ✅ Короткое описание на странице лидерборда (из `content/leaderboard.md`, поддерживает ENG/RU)
- ✅ Фильтр по диапазону дат (dual range slider)
- ✅ Сортировка по колонкам (pass@1, pass@6, n_task)
- ✅ Переключение языков (английский/русский)
- ✅ Адаптивный дизайн (мобильная версия)
- ✅ Красивые badges для топ-3 моделей

### Данные

Данные загружаются из файлов `src/data/sample*.json`. Формат файлов остался прежним:

```json
{
  "model": { 0: "model_name", ... },
  "date": { 0: 1735689600000, ... },
  "pass@1": { 0: 0.1699091401, ... },
  "pass@6": { 0: 0.8299091401, ... },
  "task_id": { 0: "task-0", ... }
}
```

### Как добавить новые данные?

1. Создайте файл `src/data/sampleXXX.json` (где XXX — номер, например 031)
2. Следуйте формату выше
3. Обновите диапазон в коде (строка ~792): `for (let i = 0; i <= 31; i++)`
4. Файл автоматически подгрузится

### Отличия от старой версии

| Старая версия (Svelte) | Новая версия (Vanilla JS) |
|------------------------|---------------------------|
| Svelte 5 + TypeScript | Plain JavaScript (ES6+) |
| 30+ файлов компонентов | 1 HTML файл |
| npm build (Vite) | Открывается напрямую |
| ~20MB node_modules | 0 зависимостей |
| Сложная структура | Простой линейный код |

### Deployment на GitHub Pages

```bash
# Переименовать новый файл
mv index-new.html index.html

# Закоммитить и запушить
git add index.html
git commit -m "Refactor: migrate to vanilla JS, single-file architecture"
git push origin main

# GitHub Pages автоматически обновится
```

---

## Старая версия (Svelte)

Для запуска старой версии:

```bash
npm i
npm run dev
```

Проект будет доступен по адресу [localhost:5173](http://localhost:5173/)

